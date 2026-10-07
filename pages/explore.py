"""explore.py - search and browse all places."""
import tkinter as tk

from .common import (COLORS, FONTS, PAGE_PAD, PLACES, card_grid, clear_frame, header,
                     make_button, scrollable)


class ExplorePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS['bg'])
        self.app = app
        # Text typed in the search box; other pages can set it before showing Explore.
        self.search_var = tk.StringVar()
        self.refresh()

    def refresh(self):
        clear_frame(self)
        header(self, self.app, 'Explore')
        outer, content = scrollable(self)
        outer.pack(fill='both', expand=True)

        # Top row: title on the left; Filters button, search box and Search button on the right
        top = tk.Frame(content, bg=COLORS['bg'])
        top.pack(fill='x', padx=PAGE_PAD, pady=18)
        tk.Label(top, text='Explore Bhutan', font=FONTS['title'], bg=COLORS['bg']).pack(side='left')
        make_button(top, 'Filters', lambda: self.app.show_page('Filters'), False).pack(side='right')
        entry = tk.Entry(top, textvariable=self.search_var, width=35, font=FONTS['body'])
        entry.pack(side='right', ipady=7, padx=8)
        entry.bind('<Return>', lambda e: self.refresh())
        make_button(top, 'Search', self.refresh, True).pack(side='right')

        # Results
        results = self.filtered_places()
        tk.Label(content, text=f'{len(results)} places found', font=FONTS['small'],
                 bg=COLORS['bg'], fg=COLORS['muted']).pack(anchor='w', padx=PAGE_PAD)
        card_grid(content, self.app, results).pack(fill='x', padx=PAGE_PAD - 7, pady=10)

        if not results:
            tk.Label(content, text='No places found. Try a different search.', font=FONTS['body'],
                     bg=COLORS['bg'], fg=COLORS['muted']).pack(pady=50)

    def filtered_places(self):
        """Places whose name, district or category contains the search text."""
        query = self.search_var.get().strip().lower()
        if not query:
            return PLACES
        return [p for p in PLACES
                if query in p['name'].lower()
                or query in p['location'].lower()
                or query in p['type'].lower()]
