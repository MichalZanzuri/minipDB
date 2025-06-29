# utils.py
import tkinter as tk
import datetime

def add_datetime_label(window):
    datetime_label = tk.Label(window, font=("Arial", 10), fg="gray")
    datetime_label.pack(side=tk.TOP, pady=5)

    def update_datetime():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datetime_label.config(text=now)
        datetime_label.after(1000, update_datetime)

    update_datetime()
