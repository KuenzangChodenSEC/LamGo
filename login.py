import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re


# ---------------- DATABASE ----------------
def create_database():
    conn = sqlite3.connect("lamgo_users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("LamGo - Login")
root.geometry("950x600")
root.resizable(False, False)
root.configure(bg="#F5F8F3")

create_database()


# ---------------- COLORS ----------------
GREEN = "#176B4D"
DARK_GREEN = "#105239"
LIGHT_GREEN = "#EAF3EC"
WHITE = "#FFFFFF"
TEXT = "#26352D"
GRAY = "#7A857F"
BORDER = "#D7DED9"


# ---------------- FUNCTIONS ----------------
def clear_frame():
    for widget in form_frame.winfo_children():
        widget.destroy()


def show_login():
    clear_frame()

    title = tk.Label(
        form_frame,
        text="Welcome Back",
        font=("Arial", 25, "bold"),
        fg=TEXT,
        bg=WHITE
    )
    title.pack(anchor="w", pady=(10, 5))

    subtitle = tk.Label(
        form_frame,
        text="Log in to continue your journey with LamGo.",
        font=("Arial", 11),
        fg=GRAY,
        bg=WHITE
    )
    subtitle.pack(anchor="w", pady=(0, 30))

    # Email
    tk.Label(
        form_frame,
        text="Email or Phone",
        font=("Arial", 10, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(anchor="w")

    email_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        bd=1,
        relief="solid",
        highlightthickness=0
    )
    email_entry.pack(fill="x", ipady=10, pady=(7, 18))

    # Password
    tk.Label(
        form_frame,
        text="Password",
        font=("Arial", 10, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(anchor="w")

    password_frame = tk.Frame(form_frame, bg=WHITE)
    password_frame.pack(fill="x", pady=(7, 10))

    password_entry = tk.Entry(
        password_frame,
        font=("Arial", 11),
        show="•",
        bd=1,
        relief="solid"
    )
    password_entry.pack(side="left", fill="x", expand=True, ipady=10)

    def show_password():
        if password_entry.cget("show") == "":
            password_entry.config(show="•")
            eye_button.config(text="Show")
        else:
            password_entry.config(show="")
            eye_button.config(text="Hide")

    eye_button = tk.Button(
        password_frame,
        text="Show",
        command=show_password,
        bg=WHITE,
        fg=GREEN,
        bd=0,
        font=("Arial", 9, "bold"),
        cursor="hand2"
    )
    eye_button.pack(side="right", padx=5)

    # Remember + Forgot
    options = tk.Frame(form_frame, bg=WHITE)
    options.pack(fill="x", pady=(0, 20))

    remember_var = tk.BooleanVar()

    tk.Checkbutton(
        options,
        text="Remember me",
        variable=remember_var,
        bg=WHITE,
        fg=GRAY,
        activebackground=WHITE,
        font=("Arial", 9),
        selectcolor=WHITE
    ).pack(side="left")

    forgot_button = tk.Button(
        options,
        text="Forgot password?",
        bg=WHITE,
        fg=GREEN,
        bd=0,
        font=("Arial", 9, "bold"),
        cursor="hand2",
        command=lambda: messagebox.showinfo(
            "Forgot Password",
            "Password reset feature will be added here."
        )
    )
    forgot_button.pack(side="right")

    # Login button
    def login():
        email = email_entry.get().strip()
        password = password_entry.get()

        if not email or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your email and password."
            )
            return

        conn = sqlite3.connect("lamgo_users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo(
                "Login Successful",
                f"Welcome back, {user[1]}!"
            )
            # Here you can open your LamGo Home/Dashboard
            # Example:
            # root.destroy()
            # open_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect email or password."
            )

    tk.Button(
        form_frame,
        text="Log In",
        command=login,
        bg=GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        font=("Arial", 11, "bold"),
        bd=0,
        cursor="hand2"
    ).pack(fill="x", ipady=10)

    # Sign up text
    bottom = tk.Frame(form_frame, bg=WHITE)
    bottom.pack(pady=25)

    tk.Label(
        bottom,
        text="Don't have an account?",
        font=("Arial", 9),
        fg=GRAY,
        bg=WHITE
    ).pack(side="left")

    tk.Button(
        bottom,
        text="Sign Up",
        command=show_signup,
        font=("Arial", 9, "bold"),
        fg=GREEN,
        bg=WHITE,
        bd=0,
        cursor="hand2"
    ).pack(side="left", padx=5)


def show_signup():
    clear_frame()

    title = tk.Label(
        form_frame,
        text="Create Account",
        font=("Arial", 25, "bold"),
        fg=TEXT,
        bg=WHITE
    )
    title.pack(anchor="w", pady=(10, 5))

    subtitle = tk.Label(
        form_frame,
        text="Create an account and start exploring Bhutan.",
        font=("Arial", 11),
        fg=GRAY,
        bg=WHITE
    )
    subtitle.pack(anchor="w", pady=(0, 25))

    # Name
    tk.Label(
        form_frame,
        text="Full Name",
        font=("Arial", 10, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(anchor="w")

    name_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        bd=1,
        relief="solid"
    )
    name_entry.pack(fill="x", ipady=9, pady=(6, 15))

    # Email
    tk.Label(
        form_frame,
        text="Email",
        font=("Arial", 10, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(anchor="w")

    email_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        bd=1,
        relief="solid"
    )
    email_entry.pack(fill="x", ipady=9, pady=(6, 15))

    # Password
    tk.Label(
        form_frame,
        text="Password",
        font=("Arial", 10, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(anchor="w")

    password_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        show="•",
        bd=1,
        relief="solid"
    )
    password_entry.pack(fill="x", ipady=9, pady=(6, 15))

    # Confirm password
    tk.Label(
        form_frame,
        text="Confirm Password",
        font=("Arial", 10, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(anchor="w")

    confirm_entry = tk.Entry(
        form_frame,
        font=("Arial", 11),
        show="•",
        bd=1,
        relief="solid"
    )
    confirm_entry.pack(fill="x", ipady=9, pady=(6, 20))

    # Sign up function
    def signup():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if not name or not email or not password or not confirm:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        # Email validation
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return

        if len(password) < 6:
            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )
            return

        try:
            conn = sqlite3.connect("lamgo_users.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Account Created",
                "Your LamGo account has been created successfully!"
            )

            show_login()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Account Exists",
                "An account with this email already exists."
            )

    tk.Button(
        form_frame,
        text="Create Account",
        command=signup,
        bg=GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        font=("Arial", 11, "bold"),
        bd=0,
        cursor="hand2"
    ).pack(fill="x", ipady=10)

    # Login link
    bottom = tk.Frame(form_frame, bg=WHITE)
    bottom.pack(pady=20)

    tk.Label(
        bottom,
        text="Already have an account?",
        font=("Arial", 9),
        fg=GRAY,
        bg=WHITE
    ).pack(side="left")

    tk.Button(
        bottom,
        text="Log In",
        command=show_login,
        font=("Arial", 9, "bold"),
        fg=GREEN,
        bg=WHITE,
        bd=0,
        cursor="hand2"
    ).pack(side="left", padx=5)


# ---------------- LEFT SIDE ----------------
left_frame = tk.Frame(
    root,
    bg=GREEN,
    width=440,
    height=600
)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

# Logo
logo = tk.Label(
    left_frame,
    text="🏔  LamGo",
    font=("Arial", 24, "bold"),
    bg=GREEN,
    fg=WHITE
)
logo.pack(anchor="w", padx=40, pady=(45, 20))

# Main heading
heading = tk.Label(
    left_frame,
    text="Discover Bhutan,\nOne Place at a Time.",
    font=("Arial", 27, "bold"),
    bg=GREEN,
    fg=WHITE,
    justify="left"
)
heading.pack(anchor="w", padx=40, pady=(70, 15))

description = tk.Label(
    left_frame,
    text="Explore breathtaking places, rich culture,\nand unforgettable experiences across Bhutan.",
    font=("Arial", 11),
    bg=GREEN,
    fg="#E5F1EA",
    justify="left"
)
description.pack(anchor="w", padx=40)

# Decorative text
quote = tk.Label(
    left_frame,
    text="“Your next adventure\nis just a click away.”",
    font=("Arial", 14, "italic"),
    bg=GREEN,
    fg=WHITE,
    justify="left"
)
quote.pack(anchor="w", padx=40, pady=(100, 10))


# ---------------- RIGHT SIDE ----------------
right_frame = tk.Frame(
    root,
    bg=WHITE,
    width=510,
    height=600
)
right_frame.pack(side="right", fill="both", expand=True)
right_frame.pack_propagate(False)


# Login / Sign Up tabs
tabs = tk.Frame(right_frame, bg=WHITE)
tabs.pack(fill="x", padx=55, pady=(35, 0))

login_tab = tk.Button(
    tabs,
    text="Log In",
    command=show_login,
    bg=WHITE,
    fg=GREEN,
    font=("Arial", 10, "bold"),
    bd=0,
    cursor="hand2"
)
login_tab.pack(side="left", padx=(0, 25))

signup_tab = tk.Button(
    tabs,
    text="Sign Up",
    command=show_signup,
    bg=WHITE,
    fg=GRAY,
    font=("Arial", 10),
    bd=0,
    cursor="hand2"
)
signup_tab.pack(side="left")


# Form
form_frame = tk.Frame(
    right_frame,
    bg=WHITE
)
form_frame.pack(
    fill="both",
    expand=True,
    padx=55,
    pady=(15, 20)
)


# Start with Login
show_login()

root.mainloop()