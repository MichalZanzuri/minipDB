import tkinter as tk
from tkinter import ttk, messagebox
from db import connect
from datetime import datetime

class QueryProcedureScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("שאילתות ופרוצדורות")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f8fafc")

        # תאריך ושעה
        self.setup_datetime()

        self.queries = {
            "סה\"כ מכירות ללקוח": {
                "type": "function",
                "call": "SELECT get_total_sales_for_customer(%s) AS total_sales",
                "params": [("customerid", int)],
                "icon": "💰",
                "description": "מחשב את סך המכירות ללקוח ספציפי"
            },
            "הנחות פעילות לפי חנות": {
                "type": "procedure",
                "call": "SELECT * FROM get_active_discounts_by_store(%s)",
                "params": [("storeid", int)],
                "icon": "🏪",
                "description": "מציג הנחות פעילות בסניף מסוים"
            },
            "עדכון מלאי מוצר": {
                "type": "procedure_update",
                "call": "CALL update_product_stock(%s, %s)",
                "params": [("productid", int), ("amount_change", int)],
                "icon": "📦",
                "description": "מעדכן כמות מלאי של מוצר"
            },
            "רשימת מוצרים": {
                "type": "query",
                "call": "SELECT * FROM product ORDER BY product_name LIMIT 10",
                "params": [],
                "icon": "📋",
                "description": "מציג 10 מוצרים ראשונים לפי סדר אלפביתי"
            }
        }

        self.create_widgets()

    def setup_datetime(self):
        """הגדרת תאריך ושעה"""
        def update_datetime():
            now = datetime.now()
            date_str = now.strftime("%d-%m-%Y")
            time_str = now.strftime("%H:%M:%S")
            self.datetime_label.config(text=f"📅 {date_str} | 🕐 {time_str}")
            self.root.after(1000, update_datetime)

        datetime_frame = tk.Frame(self.root, bg="#f8fafc")
        datetime_frame.pack(anchor="nw", padx=20, pady=10)

        self.datetime_label = tk.Label(
            datetime_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg="#4f46e5",
            bg="#f8fafc"
        )
        self.datetime_label.pack()
        update_datetime()

    def create_widgets(self):
        # כותרת ראשית
        title_frame = tk.Frame(self.root, bg="#f8fafc")
        title_frame.pack(pady=(10, 30))

        tk.Label(
            title_frame,
            text="⚙️ שאילתות ופרוצדורות",
            font=("Segoe UI", 24, "bold"),
            bg="#f8fafc",
            fg="#1e293b"
        ).pack()

        # מסגרת בחירת שאילתה
        selection_container = tk.Frame(self.root, bg="#f8fafc")
        selection_container.pack(pady=(0, 20), padx=40, fill=tk.X)

        selection_frame = tk.Frame(selection_container, bg="white", relief="solid", bd=2)
        selection_frame.pack(fill=tk.X)

        # כותרת מסגרת הבחירה
        header_frame = tk.Frame(selection_frame, bg="#6366f1", height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🔍 בחירת שאילתה/פרוצדורה",
            font=("Segoe UI", 16, "bold"),
            bg="#6366f1",
            fg="white"
        ).pack(expand=True)

        # גוף מסגרת הבחירה
        body_frame = tk.Frame(selection_frame, bg="white")
        body_frame.pack(fill=tk.X, padx=30, pady=20)

        # תווית ובחירה
        tk.Label(
            body_frame,
            text="בחר פעולה לביצוע:",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#374151"
        ).pack(anchor="e", pady=(0, 10))

        # מסגרת לקומבו
        combo_frame = tk.Frame(body_frame, bg="white")
        combo_frame.pack(fill=tk.X, pady=(0, 15))

        self.combo = ttk.Combobox(
            combo_frame,
            values=list(self.queries.keys()),
            state="readonly",
            font=("Segoe UI", 11),
            width=40
        )
        self.combo.pack(anchor="e")
        self.combo.bind("<<ComboboxSelected>>", self.on_selection)

        # תיאור השאילתה הנבחרת
        self.description_label = tk.Label(
            body_frame,
            text="",
            font=("Segoe UI", 10),
            bg="white",
            fg="#6b7280",
            wraplength=600,
            justify="right"
        )
        self.description_label.pack(anchor="e", pady=(0, 10))

        # מסגרת פרמטרים
        self.param_container = tk.Frame(body_frame, bg="white")
        self.param_container.pack(fill=tk.X, pady=10)

        # כפתור הפעלה מעוצב
        button_frame = tk.Frame(body_frame, bg="white")
        button_frame.pack(pady=15)

        self.btn_execute = tk.Button(
            button_frame,
            text="▶️ הפעל שאילתה",
            command=self.execute,
            font=("Segoe UI", 12, "bold"),
            bg="#10b981",
            fg="white",
            width=20,
            height=2,
            relief="flat",
            cursor="hand2",
            bd=0
        )
        self.btn_execute.pack()

        # אפקט hover לכפתור
        def on_enter(e):
            self.btn_execute.config(bg="#059669")

        def on_leave(e):
            self.btn_execute.config(bg="#10b981")

        self.btn_execute.bind("<Enter>", on_enter)
        self.btn_execute.bind("<Leave>", on_leave)

        # מסגרת תוצאות
        results_container = tk.Frame(self.root, bg="#f8fafc")
        results_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))

        # כותרת תוצאות
        tk.Label(
            results_container,
            text="📊 תוצאות:",
            font=("Segoe UI", 14, "bold"),
            bg="#f8fafc",
            fg="#1e293b"
        ).pack(anchor="e", pady=(0, 10))

        # מסגרת הטבלה
        self.tree_frame = tk.Frame(results_container, bg="white", relief="solid", bd=1)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # גלילה
        self.tree_scroll_y = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_scroll_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # הטבלה
        self.tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set,
            selectmode="browse"
        )
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # סטטוס
        status_frame = tk.Frame(self.root, bg="#f8fafc")
        status_frame.pack(fill=tk.X, padx=40, pady=(0, 10))

        self.status_label = tk.Label(
            status_frame,
            text="בחר שאילתה ולחץ הפעל כדי לראות תוצאות",
            fg="#6b7280",
            font=("Segoe UI", 11),
            bg="#f8fafc"
        )
        self.status_label.pack(anchor="e")

    def on_selection(self, event):
        # ניקוי פרמטרים קיימים
        for widget in self.param_container.winfo_children():
            widget.destroy()

        query_name = self.combo.get()
        if not query_name:
            return

        query_info = self.queries[query_name]
        params = query_info["params"]

        # הצגת תיאור
        description = query_info.get("description", "")
        icon = query_info.get("icon", "")
        self.description_label.config(text=f"{icon} {description}")

        self.param_entries = {}

        if params:
            # כותרת פרמטרים
            tk.Label(
                self.param_container,
                text="🔧 פרמטרים נדרשים:",
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#374151"
            ).pack(anchor="e", pady=(10, 5))

            # מסגרת פרמטרים
            params_grid = tk.Frame(self.param_container, bg="white")
            params_grid.pack(fill=tk.X, pady=5)

            for i, (param_name, param_type) in enumerate(params):
                # מסגרת לכל פרמטר
                param_frame = tk.Frame(params_grid, bg="white")
                param_frame.pack(fill=tk.X, pady=5)

                # תווית פרמטר
                param_label = tk.Label(
                    param_frame,
                    text=f"{param_name} ({param_type.__name__}):",
                    font=("Segoe UI", 10, "bold"),
                    bg="white",
                    fg="#374151",
                    width=25,
                    anchor="e"
                )
                param_label.pack(side=tk.RIGHT, padx=(0, 10))

                # שדה קלט
                entry = tk.Entry(
                    param_frame,
                    width=20,
                    font=("Segoe UI", 11),
                    relief="solid",
                    bd=1,
                    bg="#f9fafb",
                    fg="#374151",
                    justify="center"
                )
                entry.pack(side=tk.RIGHT)

                # אפקטי focus
                def on_focus_in(event, e=entry):
                    e.config(bg="#e0f2fe", bd=2)

                def on_focus_out(event, e=entry):
                    e.config(bg="#f9fafb", bd=1)

                entry.bind("<FocusIn>", on_focus_in)
                entry.bind("<FocusOut>", on_focus_out)

                self.param_entries[param_name] = (entry, param_type)

        self.status_label.config(text="הזן פרמטרים ולחץ הפעל", fg="#6b7280")
        self.clear_treeview()

    def clear_treeview(self):
        """ניקוי הטבלה"""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = []
        self.tree["show"] = ""

    def execute(self):
        """הפעלת השאילתה"""
        query_name = self.combo.get()
        if not query_name:
            messagebox.showerror("שגיאה", "בחר שאילתה או פונקציה להפעלה")
            return

        query_info = self.queries[query_name]
        sql = query_info["call"]
        params = query_info["params"]

        values = []
        try:
            for param_name, param_type in params:
                entry_widget, expected_type = self.param_entries[param_name]
                val = entry_widget.get()
                if val.strip() == "":
                    raise ValueError(f"חסר ערך לפרמטר: {param_name}")
                if expected_type == int:
                    val = int(val)
                elif expected_type == float:
                    val = float(val)
                values.append(val)
        except ValueError as ve:
            messagebox.showerror("שגיאה", str(ve))
            return

        try:
            conn = connect()
            cur = conn.cursor()

            if query_info["type"] == "function":
                if len(values) == 0:
                    cur.execute(sql)
                else:
                    cur.execute(sql, tuple(values))
                rows = cur.fetchall()
                self.show_results(cur, rows)

            elif query_info["type"] == "query":
                cur.execute(sql)
                rows = cur.fetchall()
                self.show_results(cur, rows)

            elif query_info["type"] == "procedure":
                cur.execute(sql, tuple(values))
                rows = cur.fetchall()
                self.show_results(cur, rows)

            elif query_info["type"] == "procedure_update":
                cur.execute(sql, tuple(values))
                conn.commit()
                self.status_label.config(text="✅ הפעולה בוצעה בהצלחה!", fg="#10b981")
                self.clear_treeview()

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("שגיאה", str(e))
            self.status_label.config(text=f"❌ שגיאה: {e}", fg="#ef4444")

    def show_results(self, cursor, rows):
        """הצגת תוצאות בטבלה"""
        self.clear_treeview()

        columns = [desc[0] for desc in cursor.description]
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        # הגדרת כותרות עמודות
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        # הוספת נתונים
        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_label.config(text=f"📊 נמצאו {len(rows)} תוצאות", fg="#3b82f6")

def open_queries_screen():
    window = tk.Toplevel()
    QueryProcedureScreen(window)
