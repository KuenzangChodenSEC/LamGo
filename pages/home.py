"""home.py - Home page: search banner, popular places, categories and quick links."""
import tkinter as tk

from .common import (COLORS, FONTS, PAGE_PAD, PLACES, autowrap, card_grid, clear_frame,
                     header, image_banner, make_button, place_image_path, rounded_card, scrollable)


class HomePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS['bg'])
        self.app = app
        self.refresh()

    def refresh(self):
        """Rebuild the whole page (called whenever it is shown)."""
        clear_frame(self)
        header(self, self.app, 'Home')
        outer, content = scrollable(self)
        outer.pack(fill='both', expand=True)

        self.build_hero(content)

        self.section_title(content, 'Popular Places')
        # Two rows of cards; the number of columns depends on the window width.
        card_grid(content, self.app, PLACES, max_rows=2).pack(fill='x', padx=PAGE_PAD - 7)

        self.build_categories(content)
        self.build_quick_access(content)

    # ------------------------------------------------------------------
    def section_title(self, parent, text):
        tk.Label(parent, text=text, font=FONTS['heading'], bg=COLORS['bg']).pack(
            anchor='w', padx=PAGE_PAD, pady=(16, 8))

    def build_hero(self, content):
        """Green banner: heading + search box on the left, picture on the right."""
        bg = COLORS['green_dark']
        hero = tk.Frame(content, bg=bg, height=320)
        hero.pack(fill='x', padx=PAGE_PAD, pady=24)
        hero.pack_propagate(False)

        # Left 58%: text and search
        left = tk.Frame(hero, bg=bg)
        left.place(relx=0, rely=0, relwidth=.58, relheight=1)
        text_box = tk.Frame(left, bg=bg)
        text_box.pack(fill='x', padx=50, pady=(55, 0))

        tk.Label(text_box, text='Where will you go next?', font=('Segoe UI', 32, 'bold'),
                 fg='white', bg=bg).pack(anchor='w')
        description = tk.Label(
            text_box, text='Search any place in Bhutan and see its details, weather, photos, location and reviews.',
            font=('Segoe UI', 12), fg='#DDEFE4', bg=bg, justify='left', anchor='w')
        description.pack(fill='x', pady=14)
        autowrap(description)

        row = tk.Frame(text_box, bg=bg)
        row.pack(fill='x')
        search_box = tk.Entry(row, font=('Segoe UI', 12))
        search_box.pack(side='left', fill='x', expand=True, ipady=9)

        def search():
            self.app.show_page('Explore', search=search_box.get())

        search_box.bind('<Return>', lambda e: search())
        make_button(row, 'Search', search, True).pack(side='left', padx=8)

        # Right 42%: picture of the first (most famous) place
        picture = image_banner(hero, path=place_image_path(PLACES[0]))
        picture.place(relx=.58, rely=0, relwidth=.42, relheight=1)

    def build_categories(self, content):
        """Row of category buttons that open Explore filtered by that category."""
        self.section_title(content, 'Explore by Category')
        card = rounded_card(content)
        card.pack(fill='x', padx=PAGE_PAD, pady=(0, 20))
        categories = [('⛰️', 'Mountains'), ('🏯', 'Cultural Sites'),
                      ('🌿', 'Nature & Hiking'), ('🏙️', 'Cities')]
        for icon, name in categories:
            tk.Button(card, text=f'{icon}\n{name}', bg='white', fg=COLORS['text'], bd=0,
                      font=FONTS['small'], cursor='hand2', padx=20, pady=8,
                      command=lambda q=name: self.app.show_page('Explore', search=q)
                      ).pack(side='left', expand=True)

    def build_quick_access(self, content):
        """Shortcut buttons to the other pages."""
        self.section_title(content, 'Quick Access')
        card = rounded_card(content)
        card.pack(fill='x', padx=PAGE_PAD, pady=(0, 30))
        shortcuts = [('📌 Saved Places', 'Saved Places'), ('📝 My Posts', 'My Posts'),
                     ('⭐ Reviews', 'Reviews'), ('📍 Location', 'Location'),
                     ('🔔 Notifications', 'Notifications')]
        for text, page in shortcuts:
            make_button(card, text, lambda p=page: self.app.show_page(p), False).pack(
                side='left', expand=True, padx=5)
