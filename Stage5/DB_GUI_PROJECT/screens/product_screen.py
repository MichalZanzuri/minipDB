import tkinter as tk
from tkinter import messagebox, ttk
from db import connect
import datetime
from datetime import datetime as dt

# פונקציות לשליפת סטטיסטיקות
def get_total_products():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM product")
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_low_stock_count():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM product WHERE amount < minamount")
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_inventory_value():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT SUM(price * amount) FROM product")
    total = cur.fetchone()[0] or 0
    conn.close()
    return total

def get_average_price():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT AVG(price) FROM product")
    avg = cur.fetchone()[0] or 0
    conn.close()
    return avg

# פעולות CRUD
def add_product(data):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO product (
                product_name, minamount, price, category, amount,
                added_date, gender, color, productsize, last_updated
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["product_name"], data["minamount"], data["price"], data["category"],
            data["amount"], data["added_date"], data["gender"], data["color"],
            data["productsize"], data["last_updated"]
        ))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "המוצר נוסף בהצלחה!")
    except Exception as e:
        messagebox.showerror("שגיאה", str(e))

def update_product(product_id, data):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE product SET
                product_name=%s, minamount=%s, price=%s, category=%s,
                amount=%s, gender=%s, color=%s, productsize=%s, last_updated=%s
            WHERE product_id=%s
        """, (
            data["product_name"], data["minamount"], data["price"], data["category"],
            data["amount"], data["gender"], data["color"], data["productsize"],
            datetime.date.today(), product_id
        ))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "המוצר עודכן בהצלחה!")
    except Exception as e:
        messagebox.showerror("שגיאה", str(e))

def delete_product(product_id):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "המוצר נמחק!")
    except Exception as e:
        messagebox.showerror("שגיאה", str(e))

def open_product_screen():
    window = tk.Toplevel()
    window.title("ניהול מוצרים")
    window.geometry("1200x700")
    window.configure(bg="#f5f7fb")

    # תאריך ושעה
    def update_datetime():
        now = dt.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M:%S")
        datetime_label.config(text=f"📅 {date_str} | 🕐 {time_str}")
        window.after(1000, update_datetime)

    datetime_frame = tk.Frame(window, bg="#f5f7fb")
    datetime_frame.pack(anchor="nw", padx=20, pady=10)

    datetime_label = tk.Label(
        datetime_frame,
        text="",
        font=("Segoe UI", 10, "bold"),
        fg="#4f46e5",
        bg="#f5f7fb"
    )
    datetime_label.pack()
    update_datetime()

    selected_product_id = tk.StringVar()
    entries = {}

    # 🔵 כותרת
    tk.Label(window, text="ניהול מוצרים", font=("Segoe UI", 24, "bold"), bg="#f5f7fb", fg="#1e1e2f").pack(pady=20)

    # 🔲 כרטיסי מידע
    def create_card(parent, title, value, bg_color):
        card = tk.Frame(parent, bg=bg_color, width=220, height=90)
        card.pack_propagate(False)
        card.pack(side="right", padx=10)
        tk.Label(card, text=title, font=("Segoe UI", 12), bg=bg_color, anchor="e").pack(anchor="e", padx=10, pady=(10, 0))
        tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg=bg_color, anchor="e").pack(anchor="e", padx=10)

    stat_frame = tk.Frame(window, bg="#f5f7fb")
    stat_frame.pack(pady=10)

    create_card(stat_frame, "סה\"כ מוצרים", str(get_total_products()), "#e3f2fd")
    create_card(stat_frame, "שווי מלאי", f"₪{get_inventory_value():,.2f}", "#e8f5e9")
    create_card(stat_frame, "מלאי נמוך", str(get_low_stock_count()), "#fff8e1")
    create_card(stat_frame, "מחיר ממוצע", f"₪{get_average_price():,.2f}", "#f3e8ff")

    # 🔍 סינון
    filter_frame = tk.Frame(window, bg="#f5f7fb")
    filter_frame.pack(pady=10)
    ttk.Entry(filter_frame, width=30).pack(side="right", padx=5)
    ttk.Combobox(filter_frame, values=["כל הקטגוריות"]).pack(side="right", padx=5)
    ttk.Combobox(filter_frame, values=["כל המוצרים"]).pack(side="right", padx=5)

    # 📋 טופס מעוצב
    form_container = tk.Frame(window, bg="#f5f7fb")
    form_container.pack(pady=20, padx=40, fill=tk.X)

    # מסגרת טופס עם עיצוב מודרני
    form_frame = tk.Frame(form_container, bg="white", relief="solid", bd=2)
    form_frame.pack(fill=tk.X)

    # כותרת טופס עם רקע צבעוני
    header_frame = tk.Frame(form_frame, bg="#3b82f6", height=50)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="📦 הוספה/עריכת מוצר",
        font=("Segoe UI", 16, "bold"),
        bg="#3b82f6",
        fg="white"
    ).pack(expand=True)

    # גוף הטופס
    body_frame = tk.Frame(form_frame, bg="white")
    body_frame.pack(fill=tk.X, padx=30, pady=20)

    # יצירת שדות בעיצוב רשת
    def create_modern_field(parent, label_text, icon, field_key, row, column=0):
        field_frame = tk.Frame(parent, bg="white")
        field_frame.grid(row=row, column=column, sticky="ew", padx=15, pady=10)

        # תווית עם אייקון
        label_frame = tk.Frame(field_frame, bg="white")
        label_frame.pack(anchor="e", pady=(0, 5))

        tk.Label(
            label_frame,
            text=f"{icon} {label_text}",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(side=tk.RIGHT)

        # שדה קלט עם עיצוב מודרני
        entry = tk.Entry(
            field_frame,
            width=22,
            justify='center',
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            bg="#f9fafb",
            fg="#374151",
            insertbackground="#3b82f6"
        )
        entry.pack(anchor="e", ipady=6)

        # אפקטי focus
        def on_focus_in(event):
            entry.config(bg="#e0f2fe", bd=2, relief="solid")

        def on_focus_out(event):
            entry.config(bg="#f9fafb", bd=1, relief="solid")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entries[field_key] = entry
        return entry

    # קונפיגורציה של עמודות הרשת
    body_frame.grid_columnconfigure(0, weight=1)
    body_frame.grid_columnconfigure(1, weight=1)
    body_frame.grid_columnconfigure(2, weight=1)

    # שדות הטופס בעיצוב רשת 3 עמודות
    fields = [
        ("שם מוצר", "📦", "product_name", 0, 0),
        ("כמות מינימלית", "📊", "minamount", 0, 1),
        ("מחיר", "💰", "price", 0, 2),
        ("קטגוריה", "🏷️", "category", 1, 0),
        ("כמות במלאי", "📈", "amount", 1, 1),
        ("מין", "👤", "gender", 1, 2),
        ("צבע", "🎨", "color", 2, 0),
        ("מידה", "📏", "productsize", 2, 1)
    ]

    for label_text, icon, field_key, row, col in fields:
        create_modern_field(body_frame, label_text, icon, field_key, row, col)

    def collect_data():
        return {
            "product_name": entries["product_name"].get(),
            "minamount": int(entries["minamount"].get()),
            "price": float(entries["price"].get()),
            "category": entries["category"].get(),
            "amount": int(entries["amount"].get()),
            "gender": entries["gender"].get(),
            "color": entries["color"].get(),
            "productsize": entries["productsize"].get(),
            "added_date": datetime.date.today(),
            "last_updated": datetime.date.today()
        }

    def clear_form():
        for entry in entries.values():
            entry.delete(0, tk.END)
        selected_product_id.set("")

    def on_add_product():
        try:
            data = collect_data()
            add_product(data)
            load_products()
            clear_form()
        except ValueError:
            messagebox.showerror("שגיאה", "ודא שכל השדות המספריים נכונים")

    def on_update_product():
        if not selected_product_id.get():
            messagebox.showerror("שגיאה", "בחרי מוצר לעדכון מהרשימה")
            return
        try:
            data = collect_data()
            update_product(selected_product_id.get(), data)
            load_products()
            clear_form()
        except ValueError:
            messagebox.showerror("שגיאה", "ודא שכל השדות המספריים נכונים")

    def on_delete_product():
        if not selected_product_id.get():
            messagebox.showerror("שגיאה", "בחרי מוצר למחיקה מהרשימה")
            return
        if messagebox.askyesno("אישור מחיקה", "האם למחוק את המוצר?"):
            delete_product(selected_product_id.get())
            load_products()
            clear_form()

    def create_modern_button(parent, text, icon, command, color="#3b82f6", width=18):
        btn = tk.Button(
            parent,
            text=f"{icon} {text}",
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg="white",
            width=width,
            height=2,
            relief="flat",
            cursor="hand2",
            bd=0
        )

        # אפקטי hover
        def on_enter(e):
            if color == "#3b82f6":
                btn.config(bg="#2563eb")
            elif color == "#10b981":
                btn.config(bg="#059669")
            elif color == "#ef4444":
                btn.config(bg="#dc2626")
            else:
                btn.config(bg="#4b5563")

        def on_leave(e):
            btn.config(bg=color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # מסגרת כפתורים מעוצבת
    buttons_container = tk.Frame(form_frame, bg="white")
    buttons_container.pack(fill=tk.X, pady=20)

    # רקע צבעוני לכפתורים
    buttons_bg = tk.Frame(buttons_container, bg="#f1f5f9", relief="solid", bd=1)
    buttons_bg.pack(fill=tk.X, padx=30)

    action_frame = tk.Frame(buttons_bg, bg="#f1f5f9")
    action_frame.pack(pady=15)

    # כפתורים בשורה אחת
    create_modern_button(action_frame, "הוסף מוצר", "➕", on_add_product, "#3b82f6").pack(side=tk.RIGHT, padx=8)
    create_modern_button(action_frame, "עדכן מוצר", "✏️", on_update_product, "#10b981").pack(side=tk.RIGHT, padx=8)
    create_modern_button(action_frame, "מחק מוצר", "🗑️", on_delete_product, "#ef4444").pack(side=tk.RIGHT, padx=8)
    create_modern_button(action_frame, "נקה טופס", "🧹", clear_form, "#6b7280").pack(side=tk.RIGHT, padx=8)

    # רשימת מוצרים
    list_container = tk.Frame(window, bg="#f5f7fb")
    list_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))

    tk.Label(list_container, text="רשימת מוצרים:", font=("Segoe UI", 14, "bold"), bg="#f5f7fb", fg="#1e293b").pack(anchor="e", pady=(0, 10))

    listbox = tk.Listbox(list_container, width=100, font=("Segoe UI", 10), height=8)
    listbox.pack(pady=5, fill=tk.BOTH, expand=True)

    def on_select(event):
        try:
            selected = listbox.get(listbox.curselection())
            product_id = selected.split("|")[0].strip("# ").strip()
            selected_product_id.set(product_id)

            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()

            col_names = [
                "product_id", "minamount", "price", "category", "amount",
                "added_date", "product_name", "gender", "color", "productsize", "last_updated"
            ]
            row_dict = dict(zip(col_names, row))
            for key in entries:
                entries[key].delete(0, tk.END)
                entries[key].insert(0, str(row_dict[key]))

        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    listbox.bind("<<ListboxSelect>>", on_select)

    def load_products():
        listbox.delete(0, tk.END)
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("""
                SELECT product_id, product_name, price, category, amount
                FROM product
                ORDER BY product_id DESC
            """)
            for row in cur.fetchall():
                listbox.insert(tk.END, f"#{row[0]} | {row[1]} | ₪{row[2]} | {row[3]} | מלאי: {row[4]}")
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    # כפתור רענון
    refresh_frame = tk.Frame(list_container, bg="#f5f7fb")
    refresh_frame.pack(pady=10)

    create_modern_button(refresh_frame, "רענן רשימה", "🔄", load_products, "#6366f1", 20).pack()

    load_products()
