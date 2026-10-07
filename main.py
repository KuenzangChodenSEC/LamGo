"""
main.py - starting point of the LamGo desktop app.

Run with:   python main.py

The app is one window (LamGoApp) that holds every page stacked on top of each other.
`show_page(name)` raises the requested page to the front.
"""
import json
import os
import tkinter as tk

from pages.common import COLORS, show_dialog
from pages.auth import AuthPage
from pages.collection import CollectionPage
from pages.create_post import CreatePostPage
from pages.explore import ExplorePage
from pages.filters import FiltersPage
from pages.home import HomePage
from pages.location import LocationPage
from pages.my_posts import MyPostsPage
from pages.notifications import NotificationsPage
from pages.place_details import PlaceDetailsPage
from pages.profile import ProfilePage
from pages.reviews import ReviewsPage
from pages.saved_places import SavedPlacesPage

LOGIN_PAGE = 'Login / Sign Up'


class LamGoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('LamGo - Discover Bhutan')
        self.minsize(1100, 700)
        self.configure(bg=COLORS['bg'])
        self.start_maximized()

        # ----- Data shared by all pages -----
        self.current_user = {}          # name, email, photo of the logged-in user
        self.selected_place = None      # place currently open in Place Details / Reviews
        self.saved_places = []          # names of saved places
        self.posts = []                 # posts and reviews written by users
        self.notifications = ['Welcome to LamGo!',
                              'Explore Bhutan and save places you want to visit.']

        # ----- Page container -----
        # All pages live in the same grid cell; the cell grows with the window.
        self.container = tk.Frame(self, bg=COLORS['bg'])
        self.container.pack(fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # ----- Navigation state -----
        self.frames = {}                # page name -> page widget
        self.history = []               # pages visited before the current one (for the back arrow)
        self.current_page = None
        self._navigating = False        # True while going "back" so history is not recorded

        self.register_pages()
        self.show_page(LOGIN_PAGE, record=False)    # the login page is always shown first

    # ------------------------------------------------------------------
    # Window / page setup
    # ------------------------------------------------------------------
    def start_maximized(self):
        """Open the window filling the whole desktop (Windows, Linux and macOS)."""
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{width}x{height}+0+0')      # fallback: full screen size
        try:
            self.state('zoomed')                    # Windows / macOS
        except tk.TclError:
            try:
                self.attributes('-zoomed', True)    # Linux
            except tk.TclError:
                pass

    def register_pages(self):
        """Create every page once and stack them in the container."""
        pages = {
            'Home': HomePage,
            'Explore': ExplorePage,
            'Place Details': PlaceDetailsPage,
            'Reviews': ReviewsPage,
            'Create Post': CreatePostPage,
            'Profile': ProfilePage,
            LOGIN_PAGE: AuthPage,
            'Notifications': NotificationsPage,
            'Filters': FiltersPage,
            'Location': LocationPage,
            'Saved Places': SavedPlacesPage,
            'My Posts': MyPostsPage,
            # These three use the same class; the name decides which places are listed.
            'Most Visited': CollectionPage,
            'Nature & Hiking': CollectionPage,
            'Cultural Sites': CollectionPage,
        }
        for name, page_class in pages.items():
            if page_class is CollectionPage:
                frame = page_class(self.container, self, collection_name=name)
            else:
                frame = page_class(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def show_page(self, page_name, place=None, record=True, search=None):
        """
        Bring a page to the front.

        place   - optionally select a place first (for Place Details / Reviews)
        record  - remember the page we are leaving so the back arrow works
        search  - pre-fill the Explore search box
        """
        if page_name not in self.frames:
            return
        if place:
            self.selected_place = place
        if search is not None and page_name == 'Explore':
            self.frames['Explore'].search_var.set(search)

        leaving = self.current_page
        should_record = (record and leaving and leaving != page_name
                         and not self._navigating and leaving != LOGIN_PAGE)
        if should_record:
            self.history.append(leaving)
        self.current_page = page_name

        frame = self.frames[page_name]
        if hasattr(frame, 'refresh'):
            frame.refresh()                         # rebuild the page with the latest data
        frame.tkraise()

    def go_back(self):
        """Go to the previous page (or Home when there is no history)."""
        if self.history:
            previous = self.history.pop()
            self._navigating = True
            self.show_page(previous, record=False)
            self._navigating = False
        else:
            self.show_page('Home', record=False)

    def open_place(self, place):
        """Open the details page of a place."""
        self.selected_place = place
        self.show_page('Place Details')

    # ------------------------------------------------------------------
    # Account actions
    # ------------------------------------------------------------------
    def log_in(self, user):
        """Start a session for `user` and go straight to the Home page."""
        self.current_user = user
        self.history = []
        self.show_page('Home', record=False)

    def logout(self):
        self.current_user = {}
        self.history = []
        self.show_page(LOGIN_PAGE, record=False)

    def save_current_user(self):
        """Write the current user's name / email / photo back to users.json."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
        try:
            users = {}
            if os.path.exists(path):
                with open(path, encoding='utf-8') as file:
                    users = json.load(file)

            email = self.current_user.get('email', '').lower()
            # Find the existing record (the email may have been edited, so match on the old key).
            old_key = next((key for key, value in users.items()
                            if value.get('email', key).lower() == email), None)
            record = {'name': self.current_user.get('name', ''),
                      'email': email,
                      'photo': self.current_user.get('photo', '')}
            if old_key:
                record['password'] = users[old_key].get('password', '')
                users.pop(old_key)
            users[email] = record

            with open(path, 'w', encoding='utf-8') as file:
                json.dump(users, file, indent=4)
        except Exception:
            pass        # saving the profile is optional; never crash the app because of it

    # ------------------------------------------------------------------
    # Saved places
    # ------------------------------------------------------------------
    def toggle_saved(self, place):
        """Save or un-save a place, then refresh the pages that show saved places."""
        name = place['name']
        if name in self.saved_places:
            self.saved_places.remove(name)
            show_dialog(self, 'Saved Places', f'{name} removed.', 'info')
        else:
            self.saved_places.append(name)
            show_dialog(self, 'Saved Places', f'{name} saved.', 'success')

        for page_name in ['Home', 'Explore', 'Place Details', 'Profile', 'Saved Places']:
            page = self.frames.get(page_name)
            if page is not None and hasattr(page, 'refresh'):
                page.refresh()


if __name__ == '__main__':
    app = LamGoApp()
    app.mainloop()
