"""location.py - shows the selected place and opens it in Google Maps."""
import tkinter as tk

from .common import (COLORS, FONTS, PAGE_PAD, PLACES, autowrap, clear_frame, header,
                     make_button, open_map, rounded_card, scrollable)


class LocationPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS['bg'])
        self.app = app
        self.refresh()

    def refresh(self):
        clear_frame(self)
        header(self, self.app, 'Location')
        outer, content = scrollable(self)
        outer.pack(fill='both', expand=True)
        place = self.app.selected_place or PLACES[0]

        box = rounded_card(content)
        box.pack(fill='x', padx=PAGE_PAD, pady=35)
        tk.Label(box, text='📍 Place Location', font=FONTS['title'], bg='white').pack(anchor='w')

        details = (f"Selected place: {place['name']}\nArea: {place['location']}, Bhutan\n"
                   f"Weather: {place['weather']}\nBest time: {place['best']}")
        tk.Label(box, text=details, font=FONTS['body'], bg='white', justify='left').pack(anchor='w', pady=18)

        make_button(box, 'Open Live Map Location', lambda: open_map(place), True).pack(anchor='w')

        note = tk.Label(
            box, font=FONTS['small'], bg='white', fg=COLORS['muted'], justify='left', anchor='w',
            text='The map button opens the place location in Google Maps. A desktop Tkinter app '
                 'cannot directly provide phone-style GPS without a GPS device or browser service.')
        note.pack(fill='x', pady=18)
        autowrap(note)
