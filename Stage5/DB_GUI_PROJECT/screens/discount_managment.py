import tkinter as tk
from tkinter import messagebox, ttk
from db import connect
from datetime import datetime

BG_COLOR = "#f8fafc"
FORM_BG = "#ffffff"
LABEL_FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 20, "bold")
SUBTITLE_FONT = ("Segoe UI", 14, "bold")
BTN_FONT = ("Segoe UI", 10, "bold")
BTN_COLOR = "#3b82f6"
BTN_TEXT_COLOR = "white"
ENTRY_WIDTH = 40

def add_discount(discountrate, startdate, enddate, storeid, productid):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO discount (discountrate, startdate, enddate, storeid, productid)
            VALUES (%s, %s, %s, %s, %s)
        """, (discountrate, startdate, enddate, storeid, productid))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "ההנחה נוספה בהצלחה")
    except Exception as e:
        messagebox.showerror("שגיאה בהוספה", str(e))

def update_discount(discountid, discountrate, startdate, enddate, storeid, productid):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE discount SET
                discountrate=%s,
                startdate=%s,
                enddate=%s,
                storeid=%s,
                productid=%s
            WHERE discountid=%s
        """, (discountrate, startdate, enddate, storeid, productid, discountid))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "ההנחה עודכנה בהצלחה")
    except Exception as e:
        messagebox.showerror("שגיאה בעדכון", str(e))

def delete_discount(discountid):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM discount WHERE discountid=%s", (discountid,))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("הצלחה", "ההנחה נמחקה")
    except Exception as e:
        messagebox.showerror("שגיאה במחיקה", str(e))

def load_discounts(tree):
    # ניקוי הטבלה
    for item in tree.get_children():
        tree.delete(item)

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT d.discountid, p.product_name, s.storelocation, d.discountrate, d.startdate, d.enddate
            FROM discount d
            JOIN product p ON d.productid = p.product_id
            JOIN store s ON d.storeid = s.storeid
            ORDER BY d.discountid
        """)

        for row in cur.fetchall():
            # בדיקה אם ההנחה פעילה
            start_date = datetime.strptime(str(row[4]), "%Y-%m-%d")
            end_date = datetime.strptime(str(row[5]), "%Y-%m-%d")
            today = datetime.now()

            status = "פעילה" if start_date <= today <= end_date else "לא פעילה"
            status_color = "green" if status == "פעילה" else "red"

            tree.insert("", tk.END, values=(
                row[0],  # מספר הנחה
                row[1],  # שם מוצר
                row[2],  # מיקום סניף
                f"{row[3]:.1f}%",  # אחוז הנחה
                row[4],  # תאריך התחלה
                row[5],  # תאריך סיום
                status   # סטטוס
            ), tags=(status_color,))

        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("שגיאה בטעינת ההנחות", str(e))

def open_discount_screen():
    window = tk.Toplevel()
    window.title("ניהול הנחות")
    window.geometry("1200x600")
    window.configure(bg=BG_COLOR)

    # תאריך ושעה
    def update_datetime():
        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M:%S")
        datetime_label.config(text=f"📅 {date_str} | 🕐 {time_str}")
        window.after(1000, update_datetime)

    datetime_frame = tk.Frame(window, bg=BG_COLOR)
    datetime_frame.pack(anchor="nw", padx=20, pady=10)

    datetime_label = tk.Label(
        datetime_frame,
        text="",
        font=("Segoe UI", 10, "bold"),
        fg="#4f46e5",
        bg=BG_COLOR
    )
    datetime_label.pack()
    update_datetime()

    selected_discount_id = tk.StringVar()

    # כותרת ראשית
    title_frame = tk.Frame(window, bg=BG_COLOR)
    title_frame.pack(pady=(10, 20))

    tk.Label(title_frame, text="ניהול הנחות", font=TITLE_FONT, bg=BG_COLOR, fg="#1e293b").pack()

    # מסגרת טופס מעוצבת
    form_container = tk.Frame(window, bg=BG_COLOR)
    form_container.pack(pady=(0, 15), padx=50, fill=tk.X)

    # מסגרת טופס עם עיצוב מודרני
    form_frame = tk.Frame(form_container, bg=FORM_BG, relief="solid", bd=2)
    form_frame.pack(fill=tk.X)

    # כותרת טופס עם רקע צבעוני
    header_frame = tk.Frame(form_frame, bg="#3b82f6", height=50)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="💰 הוספה/עריכת הנחה",
        font=("Segoe UI", 16, "bold"),
        bg="#3b82f6",
        fg="white"
    ).pack(expand=True)

    # גוף הטופס
    body_frame = tk.Frame(form_frame, bg=FORM_BG)
    body_frame.pack(fill=tk.X, padx=30, pady=15)

    # יצירת שורות בעיצוב רשת
    def create_modern_field(parent, label_text, icon, row, column=0, colspan=1):
        field_frame = tk.Frame(parent, bg=FORM_BG)
        field_frame.grid(row=row, column=column, columnspan=colspan, sticky="ew", padx=15, pady=8)

        # תווית עם אייקון
        label_frame = tk.Frame(field_frame, bg=FORM_BG)
        label_frame.pack(anchor="e", pady=(0, 5))

        tk.Label(
            label_frame,
            text=f"{icon} {label_text}",
            font=("Segoe UI", 11, "bold"),
            bg=FORM_BG,
            fg="#374151"
        ).pack(side=tk.RIGHT)

        # שדה קלט עם עיצוב מודרני
        entry = tk.Entry(
            field_frame,
            width=25,
            justify='center',
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            bg="#f9fafb",
            fg="#374151",
            insertbackground="#3b82f6"
        )
        entry.pack(anchor="e", ipady=5)

        # אפקטי focus
        def on_focus_in(event):
            entry.config(bg="#e0f2fe", bd=2, relief="solid")

        def on_focus_out(event):
            entry.config(bg="#f9fafb", bd=1, relief="solid")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    # קונפיגורציה של עמודות הרשת
    body_frame.grid_columnconfigure(0, weight=1)
    body_frame.grid_columnconfigure(1, weight=1)

    # שדות הטופס בעיצוב רשת
    entry_rate = create_modern_field(body_frame, "שיעור הנחה (%)", "📊", 0, 0)
    entry_start = create_modern_field(body_frame, "תאריך התחלה", "📅", 0, 1)
    entry_end = create_modern_field(body_frame, "תאריך סיום", "📅", 1, 0)
    entry_store = create_modern_field(body_frame, "מספר סניף", "🏪", 1, 1)
    entry_product = create_modern_field(body_frame, "מספר מוצר", "📦", 2, 0)

    # פעולות
    def on_add():
        try:
            add_discount(float(entry_rate.get()), entry_start.get(), entry_end.get(),
                         int(entry_store.get()), int(entry_product.get()))
            load_discounts(tree)
            clear_form()
        except ValueError:
            messagebox.showerror("שגיאה", "נא למלא את כל השדות כנדרש")

    def on_update():
        if not selected_discount_id.get():
            messagebox.showerror("שגיאה", "בחרי הנחה לעדכון")
            return
        try:
            update_discount(int(selected_discount_id.get()), float(entry_rate.get()),
                            entry_start.get(), entry_end.get(), int(entry_store.get()), int(entry_product.get()))
            load_discounts(tree)
            clear_form()
        except ValueError:
            messagebox.showerror("שגיאה", "נא למלא את כל השדות כנדרש")

    def on_delete():
        if not selected_discount_id.get():
            messagebox.showerror("שגיאה", "בחרי הנחה למחיקה")
            return
        if messagebox.askyesno("אישור מחיקה", "האם אתה בטוח שברצונך למחוק הנחה זו?"):
            delete_discount(int(selected_discount_id.get()))
            load_discounts(tree)
            clear_form()

    def clear_form():
        entry_rate.delete(0, tk.END)
        entry_start.delete(0, tk.END)
        entry_end.delete(0, tk.END)
        entry_store.delete(0, tk.END)
        entry_product.delete(0, tk.END)
        selected_discount_id.set("")

    def create_modern_button(parent, text, icon, command, color=BTN_COLOR, width=18):
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
            bd=0,
            activebackground=color,
            activeforeground="white"
        )

        # אפקטי hover מתקדמים
        def on_enter(e):
            if color == BTN_COLOR:
                btn.config(bg="#2563eb")
            elif color == "#ef4444":
                btn.config(bg="#dc2626")
            elif color == "#10b981":
                btn.config(bg="#059669")
            else:
                btn.config(bg="#4b5563")

        def on_leave(e):
            btn.config(bg=color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # מסגרת כפתורים מעוצבת
    buttons_container = tk.Frame(form_frame, bg=FORM_BG)
    buttons_container.pack(fill=tk.X, pady=15)

    # רקע צבעוני לכפתורים
    buttons_bg = tk.Frame(buttons_container, bg="#f1f5f9", relief="solid", bd=1)
    buttons_bg.pack(fill=tk.X, padx=30)

    action_frame = tk.Frame(buttons_bg, bg="#f1f5f9")
    action_frame.pack(pady=15)

    # שורה ראשונה של כפתורים
    top_buttons = tk.Frame(action_frame, bg="#f1f5f9")
    top_buttons.pack(pady=(0, 10))

    create_modern_button(top_buttons, "הוסף הנחה", "➕", on_add, BTN_COLOR).pack(side=tk.RIGHT, padx=8)
    create_modern_button(top_buttons, "עדכן הנחה", "✏️", on_update, "#10b981").pack(side=tk.RIGHT, padx=8)

    # שורה שנייה של כפתורים
    bottom_buttons = tk.Frame(action_frame, bg="#f1f5f9")
    bottom_buttons.pack()

    create_modern_button(bottom_buttons, "מחק הנחה", "🗑️", on_delete, "#ef4444").pack(side=tk.RIGHT, padx=8)
    create_modern_button(bottom_buttons, "נקה טופס", "🧹", clear_form, "#6b7280").pack(side=tk.RIGHT, padx=8)

    # כותרת רשימת הנחות
    list_title_frame = tk.Frame(window, bg=BG_COLOR)
    list_title_frame.pack(pady=(20, 10))

    tk.Label(list_title_frame, text="הנחות קיימות:", font=SUBTITLE_FONT, bg=BG_COLOR, fg="#1e293b").pack()

    # מסגרת הטבלה
    table_frame = tk.Frame(window, bg=BG_COLOR)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))

    # יצירת הטבלה
    columns = ("מספר", "מוצר", "סניף", "הנחה", "תחילה", "סיום", "סטטוס")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # הגדרת עמודות
    tree.heading("מספר", text="מספר הנחה")
    tree.heading("מוצר", text="שם מוצר")
    tree.heading("סניף", text="מיקום סניף")
    tree.heading("הנחה", text="אחוז הנחה")
    tree.heading("תחילה", text="תאריך התחלה")
    tree.heading("סיום", text="תאריך סיום")
    tree.heading("סטטוס", text="סטטוס")

    # רוחב עמודות
    tree.column("מספר", width=80, anchor="center")
    tree.column("מוצר", width=200, anchor="e")
    tree.column("סניף", width=150, anchor="e")
    tree.column("הנחה", width=100, anchor="center")
    tree.column("תחילה", width=120, anchor="center")
    tree.column("סיום", width=120, anchor="center")
    tree.column("סטטוס", width=100, anchor="center")

    # צבעים לסטטוס
    tree.tag_configure("green", foreground="green", font=("Segoe UI", 10, "bold"))
    tree.tag_configure("red", foreground="red", font=("Segoe UI", 10, "bold"))

    # גלילה
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # בחירה בטבלה
    def on_select(event):
        try:
            selected_item = tree.selection()[0]
            values = tree.item(selected_item, "values")
            discount_id = values[0]
            selected_discount_id.set(discount_id)

            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM discount WHERE discountid=%s", (discount_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                entry_rate.delete(0, tk.END)
                entry_rate.insert(0, str(row[1]))
                entry_start.delete(0, tk.END)
                entry_start.insert(0, str(row[2]))
                entry_end.delete(0, tk.END)
                entry_end.insert(0, str(row[3]))
                entry_store.delete(0, tk.END)
                entry_store.insert(0, str(row[4]))
                entry_product.delete(0, tk.END)
                entry_product.insert(0, str(row[5]))

        except IndexError:
            pass  # אין בחירה
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    tree.bind("<<TreeviewSelect>>", on_select)
    load_discounts(tree)
