"""notifications.py - list of app messages with a 'Mark All as Read' button."""
import tkinter as tk

from .common import (COLORS, FONTS, PAGE_PAD, clear_frame, header, make_button,
                     rounded_card, scrollable)


class NotificationsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS['bg'])
        self.app = app
        self.refresh()

    def refresh(self):
        clear_frame(self)
        header(self, self.app, 'Notifications')
        outer, content = scrollable(self)
        outer.pack(fill='both', expand=True)

        box = rounded_card(content)
        box.pack(fill='x', padx=PAGE_PAD, pady=30)
        tk.Label(box, text='Notifications', font=FONTS['title'], bg='white').pack(anchor='w')

        for message in self.app.notifications:
            row = tk.Frame(box, bg='white', pady=12)
            row.pack(fill='x')
            tk.Label(row, text='🔔', font=('Segoe UI Emoji', 20), bg='white').pack(side='left', padx=8)
            tk.Label(row, text=message, font=FONTS['body'], bg='white').pack(side='left')

        if not self.app.notifications:
            tk.Label(box, text='No new notifications.', font=FONTS['body'], bg='white',
                     fg=COLORS['muted']).pack(pady=25)

        make_button(box, 'Mark All as Read', self.mark_read, False).pack(anchor='e', pady=12)

    def mark_read(self):
        """Clear all notifications."""
        self.app.notifications.clear()
        self.refresh()
