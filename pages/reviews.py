"""reviews.py - ratings and visitor reviews for the selected place."""
import tkinter as tk
from tkinter import simpledialog

from .common import (COLORS, FONTS, PAGE_PAD, PLACES, clear_frame, header, make_button,
                     rounded_card, scrollable, show_dialog)

# Example reviews shown for every place: (name, text, rating label)
SAMPLE_REVIEWS = [
    ('Tashi', 'Beautiful place and amazing views.', '5 stars'),
    ('Pema', 'Peaceful and worth visiting.', '5 stars'),
    ('Sonam', 'The journey was enjoyable.', '4 stars'),
]


class ReviewsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS['bg'])
        self.app = app
        self.refresh()

    def current_place(self):
        return self.app.selected_place or PLACES[0]

    def refresh(self):
        clear_frame(self)
        header(self, self.app, 'Reviews')
        outer, content = scrollable(self)
        outer.pack(fill='both', expand=True)
        place = self.current_place()

        tk.Label(content, text='Reviews & Ratings', font=FONTS['title'], bg=COLORS['bg']).pack(
            anchor='w', padx=PAGE_PAD, pady=(20, 4))
        tk.Label(content, text=place['name'], font=FONTS['subheading'], bg=COLORS['bg'],
                 fg=COLORS['muted']).pack(anchor='w', padx=PAGE_PAD, pady=(0, 12))

        # Summary: big rating number, stars and the "Write a Review" button
        summary = rounded_card(content)
        summary.pack(fill='x', padx=PAGE_PAD)
        tk.Label(summary, text=str(place['rating']), font=('Segoe UI', 38, 'bold'),
                 bg='white').pack(side='left', padx=20)
        tk.Label(summary, text=f"★★★★★\n{place['reviews']} visitor ratings", font=FONTS['body'],
                 fg=COLORS['gold'], bg='white').pack(side='left')
        make_button(summary, 'Write a Review', self.write_review, True).pack(side='right', padx=10)

        # List of reviews
        box = rounded_card(content)
        box.pack(fill='x', padx=PAGE_PAD, pady=16)
        tk.Label(box, text='Visitor Reviews', font=FONTS['heading'], bg='white').pack(anchor='w')
        for name, text, rating in SAMPLE_REVIEWS:
            self.add_review_row(box, name, text, rating)
        self.add_user_reviews(box, place)

    def add_review_row(self, box, name, text, rating):
        """One sample review: avatar, name + text, rating on the right."""
        row = tk.Frame(box, bg='white', pady=10)
        row.pack(fill='x')
        tk.Label(row, text='👤', font=('Segoe UI Emoji', 22), bg='white').pack(side='left', padx=8)
        middle = tk.Frame(row, bg='white')
        middle.pack(side='left', fill='x', expand=True)
        tk.Label(middle, text=name, font=FONTS['subheading'], bg='white').pack(anchor='w')
        tk.Label(middle, text=text, font=FONTS['body'], bg='white', fg=COLORS['muted']).pack(anchor='w')
        tk.Label(row, text=rating, font=FONTS['small'], fg=COLORS['gold'], bg='white').pack(side='right')

    def add_user_reviews(self, box, place):
        """Reviews written by the current user for this place."""
        reviews = [p for p in self.app.posts if p.get('place') == place['name'] and p.get('text')]
        for post in reviews:
            row = tk.Frame(box, bg='#F8FAF8', pady=8)
            row.pack(fill='x', pady=3)
            tk.Label(row, text=self.app.current_user.get('name', 'You'),
                     font=FONTS['subheading'], bg='#F8FAF8').pack(anchor='w')
            stars = '★' * post.get('rating', 0) if post.get('rating') else 'No rating'
            tk.Label(row, text=stars + '\n' + post['text'], font=FONTS['body'], bg='#F8FAF8',
                     justify='left').pack(anchor='w')

    def write_review(self):
        """Ask for review text and store it as a 5-star review of the current place."""
        text = simpledialog.askstring('Write a Review', 'Write your review:', parent=self)
        if text:
            self.app.posts.append({'place': self.current_place()['name'], 'text': text,
                                   'rating': 5, 'photo': ''})
            show_dialog(self, 'Review Added', 'Your review was added.', 'success')
            self.refresh()
