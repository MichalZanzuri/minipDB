import tkinter as tk
from tkinter import messagebox, ttk
from db import connect
import datetime
from datetime import datetime as dt

def add_sale(saledate, totalprice, customerid):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sale (saledate, totalprice, customerid)
            VALUES (%s, %s, %s)
        """, (saledate, totalprice, customerid))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "המכירה נוספה בהצלחה!")
    except Exception as e:
        messagebox.showerror("שגיאה בהוספת מכירה", str(e))

def update_sale(sale_id, new_total):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("UPDATE sale SET totalprice = %s WHERE saleid = %s", (new_total, sale_id))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "סכום המכירה עודכן!")
    except Exception as e:
        messagebox.showerror("שגיאה", str(e))

def get_sales_statistics():
    """שליפת סטטיסטיקות מכירות"""
    try:
        conn = connect()
        cur = conn.cursor()

        # סה"כ מכירות
        cur.execute("SELECT COUNT(*) FROM sale")
        total_sales = cur.fetchone()[0]

        # סה"כ הכנסות
        cur.execute("SELECT SUM(totalprice) FROM sale")
        total_revenue = cur.fetchone()[0] or 0

        # ממוצע מכירה
        cur.execute("SELECT AVG(totalprice) FROM sale")
        avg_sale = cur.fetchone()[0] or 0

        # מכירות היום
        cur.execute("SELECT COUNT(*) FROM sale WHERE saledate = %s", (datetime.date.today(),))
        today_sales = cur.fetchone()[0]

        cur.close()
        conn.close()
        return total_sales, total_revenue, avg_sale, today_sales
    except Exception:
        return 0, 0, 0, 0

def open_sale_screen():
    window = tk.Toplevel()
    window.title("ניהול מכירות")
    window.geometry("900x600")
    window.configure(bg="#f8fafc")

    # תאריך ושעה
    def update_datetime():
        now = dt.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M:%S")
        datetime_label.config(text=f"📅 {date_str} | 🕐 {time_str}")
        window.after(1000, update_datetime)

    datetime_frame = tk.Frame(window, bg="#f8fafc")
    datetime_frame.pack(anchor="nw", padx=20, pady=10)

    datetime_label = tk.Label(
        datetime_frame,
        text="",
        font=("Segoe UI", 10, "bold"),
        fg="#4f46e5",
        bg="#f8fafc"
    )
    datetime_label.pack()
    update_datetime()

    selected_sale_id = tk.StringVar()

    # כותרת ראשית
    title_frame = tk.Frame(window, bg="#f8fafc")
    title_frame.pack(pady=(10, 20))

    tk.Label(
        title_frame,
        text="🛒 ניהול מכירות",
        font=("Segoe UI", 24, "bold"),
        bg="#f8fafc",
        fg="#1e293b"
    ).pack()

    # כרטיסי סטטיסטיקות
    def create_stat_card(parent, title, value, icon, bg_color):
        card = tk.Frame(parent, bg=bg_color, width=180, height=80, relief="solid", bd=1)
        card.pack_propagate(False)
        card.pack(side="right", padx=8, pady=5)

        # מסגרת עליונה לאייקון וכותרת
        top_frame = tk.Frame(card, bg=bg_color)
        top_frame.pack(fill=tk.X, pady=(8, 2))

        # אייקון
        tk.Label(
            top_frame,
            text=icon,
            font=("Segoe UI", 16),
            bg=bg_color,
            fg="#1e293b"
        ).pack(side=tk.RIGHT, padx=5)

        # כותרת
        tk.Label(
            top_frame,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=bg_color,
            fg="#374151"
        ).pack(side=tk.RIGHT)

        # ערך
        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 14, "bold"),
            bg=bg_color,
            fg="#1e293b"
        ).pack(pady=(0, 8))

        return card

    def update_stats():
        """עדכון סטטיסטיקות"""
        total_sales, total_revenue, avg_sale, today_sales = get_sales_statistics()

        # ניקוי כרטיסים קיימים
        for widget in stats_frame.winfo_children():
            widget.destroy()

        create_stat_card(stats_frame, "סה\"כ מכירות", str(total_sales), "📊", "#dbeafe")
        create_stat_card(stats_frame, "סה\"כ הכנסות", f"₪{total_revenue:,.0f}", "💰", "#dcfce7")
        create_stat_card(stats_frame, "ממוצע מכירה", f"₪{avg_sale:,.0f}", "📈", "#fef3c7")
        create_stat_card(stats_frame, "מכירות היום", str(today_sales), "📅", "#f3e8ff")

    # מסגרת סטטיסטיקות
    stats_frame = tk.Frame(window, bg="#f8fafc")
    stats_frame.pack(pady=10)
    update_stats()

    # מסגרת טופס מעוצבת
    form_container = tk.Frame(window, bg="#f8fafc")
    form_container.pack(pady=15, padx=40, fill=tk.X)

    form_frame = tk.Frame(form_container, bg="white", relief="solid", bd=2)
    form_frame.pack(fill=tk.X)

    # כותרת טופס
    header_frame = tk.Frame(form_frame, bg="#10b981", height=50)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="💳 הוספה/עריכת מכירה",
        font=("Segoe UI", 16, "bold"),
        bg="#10b981",
        fg="white"
    ).pack(expand=True)

    # גוף הטופס
    body_frame = tk.Frame(form_frame, bg="white")
    body_frame.pack(fill=tk.X, padx=40, pady=15)

    def create_modern_field(parent, label_text, icon, row, column=0):
        field_frame = tk.Frame(parent, bg="white")
        field_frame.grid(row=row, column=column, sticky="ew", padx=15, pady=8)

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

        # שדה קלט
        entry = tk.Entry(
            field_frame,
            width=20,
            justify='center',
            font=("Segoe UI", 11),
            relief="solid",
            bd=2,
            bg="#f9fafb",
            fg="#374151",
            insertbackground="#10b981"
        )
        entry.pack(anchor="e", ipady=6)

        # אפקטי focus
        def on_focus_in(event):
            entry.config(bg="#dcfce7", bd=2, relief="solid")

        def on_focus_out(event):
            entry.config(bg="#f9fafb", bd=2, relief="solid")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    # קונפיגורציה של הרשת
    body_frame.grid_columnconfigure(0, weight=1)
    body_frame.grid_columnconfigure(1, weight=1)

    # שדות הטופס בשתי עמודות
    entry_total = create_modern_field(body_frame, "סכום כולל (₪)", "💰", 0, 0)
    entry_customer = create_modern_field(body_frame, "קוד לקוח", "👤", 0, 1)

    def clear_form():
        entry_total.delete(0, tk.END)
        entry_customer.delete(0, tk.END)
        selected_sale_id.set("")

    def on_add_sale():
        try:
            data = {
                "sale_date": datetime.date.today(),
                "total_price": float(entry_total.get()),
                "customer_id": int(entry_customer.get())
            }
            add_sale(data["sale_date"], data["total_price"], data["customer_id"])
            clear_form()
            load_sales()
            update_stats()
        except ValueError:
            messagebox.showerror("שגיאה", "ודא שסכום ולקוח הם מספרים")

    def on_update_sale():
        if not selected_sale_id.get():
            messagebox.showerror("שגיאה", "בחר מכירה לעדכון")
            return
        try:
            new_total = float(entry_total.get())
            update_sale(selected_sale_id.get(), new_total)
            load_sales()
            update_stats()
            clear_form()
        except ValueError:
            messagebox.showerror("שגיאה", "סכום חייב להיות מספר")

    def create_modern_button(parent, text, icon, command, color="#10b981", width=18):
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
            if color == "#10b981":
                btn.config(bg="#059669")
            elif color == "#3b82f6":
                btn.config(bg="#2563eb")
            elif color == "#6b7280":
                btn.config(bg="#4b5563")

        def on_leave(e):
            btn.config(bg=color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # מסגרת כפתורים
    buttons_container = tk.Frame(form_frame, bg="white")
    buttons_container.pack(fill=tk.X, pady=15)

    buttons_bg = tk.Frame(buttons_container, bg="#f1f5f9", relief="solid", bd=1)
    buttons_bg.pack(fill=tk.X, padx=40)

    action_frame = tk.Frame(buttons_bg, bg="#f1f5f9")
    action_frame.pack(pady=12)

    # כפתורים
    create_modern_button(action_frame, "הוסף מכירה", "➕", on_add_sale, "#10b981").pack(side=tk.RIGHT, padx=8)
    create_modern_button(action_frame, "עדכן סכום", "✏️", on_update_sale, "#3b82f6").pack(side=tk.RIGHT, padx=8)
    create_modern_button(action_frame, "נקה טופס", "🧹", clear_form, "#6b7280").pack(side=tk.RIGHT, padx=8)

    # מסגרת רשימת מכירות
    list_container = tk.Frame(window, bg="#f8fafc")
    list_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))

    # כותרת רשימה
    tk.Label(
        list_container,
        text="📋 רשימת מכירות:",
        font=("Segoe UI", 14, "bold"),
        bg="#f8fafc",
        fg="#1e293b"
    ).pack(anchor="e", pady=(0, 10))

    # טבלת מכירות
    table_frame = tk.Frame(list_container, bg="white", relief="solid", bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True)

    # עמודות הטבלה
    columns = ("מספר", "תאריך", "סכום", "לקוח")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # הגדרת עמודות
    tree.heading("מספר", text="מספר מכירה")
    tree.heading("תאריך", text="תאריך")
    tree.heading("סכום", text="סכום (₪)")
    tree.heading("לקוח", text="קוד לקוח")

    # רוחב עמודות
    tree.column("מספר", width=100, anchor="center")
    tree.column("תאריך", width=120, anchor="center")
    tree.column("סכום", width=120, anchor="center")
    tree.column("לקוח", width=100, anchor="center")

    # גלילה
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_select(event):
        try:
            selected_item = tree.selection()[0]
            values = tree.item(selected_item, "values")
            sale_id = values[0]
            selected_sale_id.set(sale_id)

            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM sale WHERE saleid = %s", (sale_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                entry_total.delete(0, tk.END)
                entry_total.insert(0, str(row[2]))
                entry_customer.delete(0, tk.END)
                entry_customer.insert(0, str(row[3]))

        except IndexError:
            pass
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    tree.bind("<<TreeviewSelect>>", on_select)

    def load_sales():
        # ניקוי הטבלה
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("""
                SELECT saleid, saledate, totalprice, customerid
                FROM sale
                ORDER BY saleid DESC
            """)
            for row in cur.fetchall():
                tree.insert("", tk.END, values=(
                    row[0],  # מספר מכירה
                    row[1],  # תאריך
                    f"{row[2]:,.0f}",  # סכום עם פסיקים
                    row[3]   # קוד לקוח
                ))
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    # כפתור רענון
    refresh_frame = tk.Frame(list_container, bg="#f8fafc")
    refresh_frame.pack(pady=10)

    def refresh_all():
        load_sales()
        update_stats()

    create_modern_button(refresh_frame, "רענן נתונים", "🔄", refresh_all, "#6366f1", 20).pack()

    # טעינה ראשונית
    load_sales()
