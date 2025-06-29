import tkinter as tk
from tkinter import messagebox, ttk
from db import connect
from datetime import datetime

def get_store_stats():
    try:
        conn = connect()
        cur = conn.cursor()

        stats = {}

        cur.execute("SELECT COUNT(*) FROM sale")
        stats["total_sales"] = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(totalprice), 0) FROM sale")
        stats["total_revenue"] = float(cur.fetchone()[0])

        cur.execute("SELECT COUNT(*) FROM product WHERE amount < minamount")
        stats["low_stock"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(DISTINCT customerid) FROM sale")
        stats["unique_customers"] = cur.fetchone()[0]

        cur.execute("""
            SELECT p.product_name, SUM(sp.quantity) AS total_sold
            FROM saleproduct sp
            JOIN product p ON sp.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY total_sold DESC
            LIMIT 1
        """)
        result = cur.fetchone()
        if result:
            stats["top_product"] = f"{result[0]} ({result[1]} יחידות)"
        else:
            stats["top_product"] = "אין עדיין נתונים"

        cur.close()
        conn.close()
        return stats
    except Exception as e:
        return {"error": str(e)}

# --- מסכי רשימות מעוצבים ---

def show_low_stock_products():
    win = tk.Toplevel()
    win.title("מוצרים עם מלאי נמוך")
    win.attributes('-fullscreen', True)
    win.configure(bg="#f8fafc")

    # יציאה ממסך מלא
    def exit_fullscreen(event):
        win.attributes('-fullscreen', False)
        win.geometry("900x600")

    win.bind('<Escape>', exit_fullscreen)

    # כותרת
    tk.Label(
        win,
        text="⚠️ מוצרים עם מלאי נמוך",
        font=("Segoe UI", 24, "bold"),
        bg="#f8fafc",
        fg="#dc2626"
    ).pack(pady=20)

    # מסגרת הטבלה
    table_frame = tk.Frame(win, bg="white", relief="solid", bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

    columns = ("מספר", "שם מוצר", "כמות נוכחית", "כמות מינימלית", "חסר")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT product_id, product_name, amount, minamount 
            FROM product 
            WHERE amount < minamount
            ORDER BY product_name
        """)
        rows = cur.fetchall()
        for row in rows:
            shortage = row[3] - row[2]
            tree.insert("", tk.END, values=(
                row[0], row[1], row[2], row[3], shortage
            ))
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("שגיאה", str(e))

def show_all_sales():
    win = tk.Toplevel()
    win.title("רשימת מכירות")
    win.attributes('-fullscreen', True)
    win.configure(bg="#f8fafc")

    def exit_fullscreen(event):
        win.attributes('-fullscreen', False)
        win.geometry("1000x600")

    win.bind('<Escape>', exit_fullscreen)

    # כותרת
    tk.Label(
        win,
        text="🛒 רשימת כל המכירות",
        font=("Segoe UI", 24, "bold"),
        bg="#f8fafc",
        fg="#10b981"
    ).pack(pady=20)

    table_frame = tk.Frame(win, bg="white", relief="solid", bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

    columns = ("מספר מכירה", "תאריך", "סכום", "ID לקוח", "שם לקוח")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

    tree.heading("מספר מכירה", text="מספר מכירה")
    tree.heading("תאריך", text="תאריך")
    tree.heading("סכום", text="סכום (₪)")
    tree.heading("ID לקוח", text="ID לקוח")
    tree.heading("שם לקוח", text="שם לקוח")

    tree.column("מספר מכירה", width=120, anchor="center")
    tree.column("תאריך", width=120, anchor="center")
    tree.column("סכום", width=120, anchor="center")
    tree.column("ID לקוח", width=100, anchor="center")
    tree.column("שם לקוח", width=200, anchor="e")

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.saleid, s.saledate, s.totalprice, c.personid, c.fullname
            FROM sale s
            JOIN customer c ON s.customerid = c.personid
            ORDER BY s.saledate DESC
        """)
        for row in cur.fetchall():
            tree.insert("", tk.END, values=(
                row[0], row[1], f"{row[2]:,.0f}", row[3], row[4]
            ))
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("שגיאה", str(e))

def show_customers_with_sales():
    win = tk.Toplevel()
    win.title("לקוחות עם רכישות")
    win.attributes('-fullscreen', True)
    win.configure(bg="#f8fafc")

    def exit_fullscreen(event):
        win.attributes('-fullscreen', False)
        win.geometry("900x600")

    win.bind('<Escape>', exit_fullscreen)

    # כותרת
    tk.Label(
        win,
        text="👥 לקוחות ורכישותיהם",
        font=("Segoe UI", 24, "bold"),
        bg="#f8fafc",
        fg="#8b5cf6"
    ).pack(pady=20)

    table_frame = tk.Frame(win, bg="white", relief="solid", bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

    columns = ("שם לקוח", "ID לקוח", "מספר רכישות", "סה\"כ הוצאות")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

    for col in columns:
        tree.heading(col, text=col)

    tree.column("שם לקוח", width=200, anchor="e")
    tree.column("ID לקוח", width=100, anchor="center")
    tree.column("מספר רכישות", width=150, anchor="center")
    tree.column("סה\"כ הוצאות", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.fullname, c.personid, COUNT(s.saleid) AS purchase_count, COALESCE(SUM(s.totalprice),0) AS total_spent
            FROM customer c
            LEFT JOIN sale s ON s.customerid = c.personid
            GROUP BY c.fullname, c.personid
            ORDER BY total_spent DESC
        """)
        for row in cur.fetchall():
            tree.insert("", tk.END, values=(
                row[0], row[1], row[2], f"₪{row[3]:,.0f}"
            ))
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("שגיאה", str(e))

# --- מסך סטטיסטיקות ראשי מעוצב ---

def open_stats_screen():
    window = tk.Toplevel()
    window.title("סטטיסטיקות חנות")
    window.attributes('-fullscreen', True)
    window.configure(bg="#f8fafc")

    # יציאה ממסך מלא
    def exit_fullscreen(event):
        window.attributes('-fullscreen', False)
        window.geometry("1200x700")

    def toggle_fullscreen(event):
        is_fullscreen = window.attributes('-fullscreen')
        window.attributes('-fullscreen', not is_fullscreen)

    window.bind('<Escape>', exit_fullscreen)
    window.bind('<F11>', toggle_fullscreen)

    # תאריך ושעה
    def update_datetime():
        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M:%S")
        datetime_label.config(text=f"📅 {date_str} | 🕐 {time_str}")
        window.after(1000, update_datetime)

    datetime_frame = tk.Frame(window, bg="#f8fafc")
    datetime_frame.pack(anchor="nw", padx=20, pady=10)

    datetime_label = tk.Label(
        datetime_frame,
        text="",
        font=("Segoe UI", 12, "bold"),
        fg="#4f46e5",
        bg="#f8fafc"
    )
    datetime_label.pack()
    update_datetime()

    # כפתור יציאה ממסך מלא
    exit_frame = tk.Frame(window, bg="#f8fafc")
    exit_frame.pack(anchor="ne", padx=20, pady=10)

    exit_btn = tk.Button(
        exit_frame,
        text="❌ יציאה ממסך מלא (ESC)",
        command=lambda: exit_fullscreen(None),
        font=("Segoe UI", 10),
        bg="#ef4444",
        fg="white",
        relief="flat",
        cursor="hand2"
    )
    exit_btn.pack()

    # כותרת ראשית
    title_frame = tk.Frame(window, bg="#f8fafc")
    title_frame.pack(pady=(10, 40))

    tk.Label(
        title_frame,
        text="📊 סטטיסטיקות החנות",
        font=("Segoe UI", 32, "bold"),
        bg="#f8fafc",
        fg="#1e293b"
    ).pack()

    # מסגרת כרטיסי סטטיסטיקות
    stats_container = tk.Frame(window, bg="#f8fafc")
    stats_container.pack(pady=30, padx=60)

    def create_interactive_card(parent, title, value, icon, bg_color, click_command=None, row=0, col=0):
        card = tk.Frame(parent, bg=bg_color, width=300, height=150, relief="solid", bd=2, cursor="hand2" if click_command else "arrow")
        card.grid_propagate(False)
        card.grid(row=row, column=col, padx=20, pady=20)

        if click_command:
            card.bind("<Button-1>", lambda e: click_command())

        # אייקון
        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 28),
            bg=bg_color,
            fg="#1e293b"
        )
        icon_label.pack(pady=(20, 10))

        if click_command:
            icon_label.bind("<Button-1>", lambda e: click_command())

        # כותרת
        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=bg_color,
            fg="#374151"
        )
        title_label.pack(pady=(0, 5))

        if click_command:
            title_label.bind("<Button-1>", lambda e: click_command())

        # ערך
        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg=bg_color,
            fg="#1e293b"
        )
        value_label.pack(pady=(0, 10))

        if click_command:
            value_label.bind("<Button-1>", lambda e: click_command())
            # הוספת סימן שאפשר ללחוץ
            click_hint = tk.Label(
                card,
                text="👆 לחץ לפרטים",
                font=("Segoe UI", 9),
                bg=bg_color,
                fg="#6b7280"
            )
            click_hint.pack()
            click_hint.bind("<Button-1>", lambda e: click_command())

        return value_label

    # רשת כרטיסים
    stats_grid = tk.Frame(stats_container, bg="#f8fafc")
    stats_grid.pack()

    # משתנים לכרטיסים
    card_labels = {}

    def refresh_stats():
        stats = get_store_stats()
        if "error" in stats:
            messagebox.showerror("שגיאה", stats["error"])
            return

        # עדכון כרטיסים
        if "total_sales" in card_labels:
            for widget in stats_grid.winfo_children():
                widget.destroy()

        card_labels["total_sales"] = create_interactive_card(
            stats_grid, "סה\"כ מכירות", str(stats['total_sales']),
            "🛒", "#dbeafe", show_all_sales, 0, 0
        )

        card_labels["total_revenue"] = create_interactive_card(
            stats_grid, "הכנסות כוללות", f"₪{stats['total_revenue']:,.0f}",
            "💰", "#dcfce7", None, 0, 1
        )

        card_labels["low_stock"] = create_interactive_card(
            stats_grid, "מלאי נמוך", str(stats['low_stock']),
            "⚠️", "#fef3c7", show_low_stock_products, 1, 0
        )

        card_labels["unique_customers"] = create_interactive_card(
            stats_grid, "לקוחות ייחודיים", str(stats['unique_customers']),
            "👥", "#f3e8ff", show_customers_with_sales, 1, 1
        )

    # כרטיס מוצר הכי נמכר
    top_product_frame = tk.Frame(window, bg="#f8fafc")
    top_product_frame.pack(pady=30)

    top_product_card = tk.Frame(top_product_frame, bg="#e0f2fe", width=600, height=100, relief="solid", bd=2)
    top_product_card.pack_propagate(False)
    top_product_card.pack()

    tk.Label(
        top_product_card,
        text="🏆 המוצר הכי נמכר",
        font=("Segoe UI", 14, "bold"),
        bg="#e0f2fe",
        fg="#374151"
    ).pack(pady=(15, 5))

    top_product_label = tk.Label(
        top_product_card,
        text="",
        font=("Segoe UI", 16, "bold"),
        bg="#e0f2fe",
        fg="#1e293b"
    )
    top_product_label.pack()

    def update_top_product():
        stats = get_store_stats()
        if "error" not in stats:
            top_product_label.config(text=stats['top_product'])

    # כפתור רענון מעוצב
    refresh_frame = tk.Frame(window, bg="#f8fafc")
    refresh_frame.pack(pady=30)

    def refresh_all():
        refresh_stats()
        update_top_product()

    refresh_btn = tk.Button(
        refresh_frame,
        text="🔄 רענן נתונים",
        command=refresh_all,
        font=("Segoe UI", 14, "bold"),
        bg="#6366f1",
        fg="white",
        width=20,
        height=2,
        relief="flat",
        cursor="hand2",
        bd=0
    )
    refresh_btn.pack()

    # אפקט hover
    def on_enter(e):
        refresh_btn.config(bg="#4f46e5")

    def on_leave(e):
        refresh_btn.config(bg="#6366f1")

    refresh_btn.bind("<Enter>", on_enter)
    refresh_btn.bind("<Leave>", on_leave)

    # טעינה ראשונית
    refresh_all()
