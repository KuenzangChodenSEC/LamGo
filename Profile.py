import tkinter as tk
from tkinter import font

# ---------- Window ----------
WIN_W, WIN_H = 1040, 660

# ---------- Colors ----------
BG = "#F5F7F4"
WHITE = "#FFFFFF"
GREEN = "#3E7C59"
DARK = "#26312B"
GRAY = "#8A9088"
LIGHT_GRAY = "#EEF1ED"
BORDER = "#E4E8E1"
YELLOW = "#F5A623"

# ---------- Data ----------
PLACES = [
    {"name": "Tiger's Nest",    "loc": "Paro",     "rating": "4.9", "color": "#6E8B5C"},
    {"name": "Punakha Dzong",   "loc": "Punakha",  "rating": "4.8", "color": "#A6764F"},
    {"name": "Phobjikha Valley","loc": "Wangdue",  "rating": "4.8", "color": "#8FA9C4"},
    {"name": "Dochula Pass",    "loc": "Thimphu",  "rating": "4.7", "color": "#C7B7DC"},
    {"name": "Haa Valley",      "loc": "Haa",      "rating": "4.6", "color": "#7FAE8E"},
    {"name": "Bumthang",        "loc": "Bumthang", "rating": "4.7", "color": "#9BB89A"},
]

MENU = [
    ("📍", "My Visited Places"),
    ("📝", "My Posts"),
    ("🔔", "Notifications"),
    ("⚙", "Settings"),
    ("↪", "Logout"),
]

NAV_LINKS = ["Discover", "Explore", "Saved", "Profile"]

COLLECTIONS = [
    ("🚩", "Must Visit", "8 places"),
    ("🌲", "Nature & Hiking", "6 places"),
    ("🏛", "Cultural Sites", "5 places"),
]


def round_rect(canvas, x1, y1, x2, y2, r=16, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class ProfileApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LamGo - My Profile")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.logo_font = font.Font(family="Helvetica", size=13, weight="bold")
        self.nav_font = font.Font(family="Helvetica", size=10)
        self.name_font = font.Font(family="Helvetica", size=13, weight="bold")
        self.bold_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.reg_font = font.Font(family="Helvetica", size=10)
        self.small_font = font.Font(family="Helvetica", size=8)
        self.tab_font = font.Font(family="Helvetica", size=11, weight="bold")
        self.tab_font_inactive = font.Font(family="Helvetica", size=11)

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, width=WIN_W, height=WIN_H)
        self.canvas.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):
        c = self.canvas

        # ================= Top bar =================
        c.create_rectangle(0, 0, WIN_W, 55, fill=WHITE, outline="")
        c.create_line(0, 55, WIN_W, 55, fill=BORDER)

        c.create_text(25, 27, text="🏔 LamGo", font=self.logo_font, fill=GREEN, anchor="w")

        nx = 140
        for i, link in enumerate(NAV_LINKS):
            color = DARK if i == 0 else GRAY
            c.create_text(nx, 27, text=link, font=self.nav_font, fill=color, anchor="w")
            nx += 70

        round_rect(c, 430, 14, 700, 41, r=13, fill=LIGHT_GRAY, outline="")
        c.create_text(450, 27, text="🔍  Where do you want to go?", font=self.small_font,
                      fill=GRAY, anchor="w")

        c.create_text(950, 27, text="🔔", font=("Helvetica", 13))
        c.create_oval(990, 12, 1018, 40, fill="#D9B08C", outline="")
        c.create_text(1004, 26, text="🙂", font=("Helvetica", 11))

        # ================= Left sidebar =================
        SX1, SX2 = 20, 250
        round_rect(c, SX1, 75, SX2, 215, r=14, fill=WHITE, outline=BORDER)
        c.create_oval(SX1 + 25, 95, SX1 + 75, 145, fill="#D9B08C", outline="")
        c.create_text(SX1 + 50, 120, text="🙂", font=("Helvetica", 18))
        c.create_text(SX1 + 20, 158, text="Tashi Yangzem", font=self.name_font, anchor="w")

        stats = [("12", "Places visited"), ("8", "Reviews"), ("15", "Photos")]
        for i, (num, label) in enumerate(stats):
            x = SX1 + 45 + i * 65
            c.create_text(x, 185, text=num, font=self.bold_font)
            c.create_text(x, 200, text=label, font=self.small_font, fill=GRAY)

        menu_y = 235
        for icon, label in MENU:
            round_rect(c, SX1, menu_y, SX2, menu_y + 42, r=10, fill=WHITE, outline="")
            c.create_text(SX1 + 20, menu_y + 21, text=icon, font=("Helvetica", 12))
            c.create_text(SX1 + 45, menu_y + 21, text=label, font=self.reg_font, anchor="w")
            c.create_text(SX2 - 15, menu_y + 21, text="›", font=("Helvetica", 12), fill=GRAY)
            menu_y += 46

        # ================= Right content =================
        RX1, RX2 = 275, 1020

        # Tabs
        c.create_text(RX1, 82, text="My Saved Places", font=self.tab_font, fill=DARK, anchor="w")
        c.create_line(RX1, 100, RX1 + 118, 100, fill=GREEN, width=2)
        c.create_text(RX1 + 150, 82, text="My Visited Places", font=self.tab_font_inactive,
                      fill=GRAY, anchor="w")

        # Grid of place cards
        card_w, card_h, gap = 232, 150, 20
        start_x, start_y = RX1, 118

        for idx, place in enumerate(PLACES):
            row, col = divmod(idx, 3)
            x1 = start_x + col * (card_w + gap)
            y1 = start_y + row * (card_h + gap)
            x2, y2 = x1 + card_w, y1 + card_h

            round_rect(c, x1, y1, x2, y2, r=12, fill=WHITE, outline=BORDER)
            round_rect(c, x1 + 6, y1 + 6, x2 - 6, y1 + 100, r=10, fill=place["color"], outline="")
            c.create_oval(x2 - 32, y1 + 12, x2 - 14, y1 + 30, fill=WHITE, outline="")
            c.create_text(x2 - 23, y1 + 21, text="🔖", font=("Helvetica", 8))

            c.create_text(x1 + 16, y1 + 116, text=place["name"], font=self.bold_font, anchor="w")
            c.create_text(x1 + 16, y1 + 132, text=place["loc"], font=self.small_font,
                          fill=GRAY, anchor="w")
            c.create_text(x2 - 45, y1 + 132, text=f"★ {place['rating']}",
                          font=self.small_font, fill=YELLOW, anchor="w")

        # My Collections
        coll_y = start_y + 2 * (card_h + gap) + 18
        c.create_text(RX1, coll_y, text="My Collections", font=self.tab_font, fill=DARK, anchor="w")

        coll_card_w = (RX2 - RX1 - 2 * gap) / 3
        coll_y1 = coll_y + 20
        coll_y2 = coll_y1 + 70
        for i, (icon, title, count) in enumerate(COLLECTIONS):
            x1 = RX1 + i * (coll_card_w + gap)
            x2 = x1 + coll_card_w
            round_rect(c, x1, coll_y1, x2, coll_y2, r=12, fill=WHITE, outline=BORDER)
            c.create_text(x1 + 20, (coll_y1 + coll_y2) / 2, text=icon, font=("Helvetica", 14))
            c.create_text(x1 + 50, (coll_y1 + coll_y2) / 2 - 8, text=title,
                          font=self.bold_font, anchor="w")
            c.create_text(x1 + 50, (coll_y1 + coll_y2) / 2 + 10, text=count,
                          font=self.small_font, fill=GRAY, anchor="w")


if __name__ == "__main__":
    app = ProfileApp()
    app.mainloop()