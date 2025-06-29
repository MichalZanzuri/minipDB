import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os
sys.path.append(os.path.dirname(__file__))
from db import connect
import plotly.express as px
import plotly.graph_objects as go

# הגדרת עמוד
st.set_page_config(
    page_title="מערכת ניהול חנות",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS מותאם
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #3b82f6, #10b981);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc, #e2e8f0);
    }
</style>
""", unsafe_allow_html=True)

# כותרת ראשית
st.markdown("""
<div class="main-header">
    <h1>🏪 מערכת ניהול חנות מקצועית</h1>
    <p>📅 {} | 🕐 {}</p>
</div>
""".format(
    datetime.now().strftime("%d-%m-%Y"),
    datetime.now().strftime("%H:%M:%S")
), unsafe_allow_html=True)

# תפריט צדדי
st.sidebar.title("🧭 תפריט ניווט")
page = st.sidebar.selectbox(
    "בחר מסך:",
    ["🏠 דף הבית", "📦 ניהול מוצרים", "🛒 ניהול מכירות", "📊 סטטיסטיקות", "💸 ניהול הנחות", "⚙️ שאילתות"]
)

# פונקציות עזר
@st.cache_data
def get_products():
    try:
        conn = connect()
        query = "SELECT product_id, product_name, price, amount, category, minamount FROM product ORDER BY product_id DESC LIMIT 50"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"שגיאה בטעינת מוצרים: {e}")
        return pd.DataFrame()

@st.cache_data
def get_sales():
    try:
        conn = connect()
        query = "SELECT saleid, saledate, totalprice, customerid FROM sale ORDER BY saleid DESC LIMIT 50"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"שגיאה בטעינת מכירות: {e}")
        return pd.DataFrame()

@st.cache_data
def get_discounts():
    try:
        conn = connect()
        query = """
        SELECT d.discountid, p.product_name, s.storelocation, d.discountrate, d.startdate, d.enddate
        FROM discount d
        JOIN product p ON d.productid = p.product_id
        JOIN store s ON d.storeid = s.storeid
        ORDER BY d.discountid DESC LIMIT 20
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"שגיאה בטעינת הנחות: {e}")
        return pd.DataFrame()

@st.cache_data
def get_stats():
    try:
        conn = connect()
        cur = conn.cursor()
        
        # סה"כ מוצרים
        cur.execute("SELECT COUNT(*) FROM product")
        total_products = cur.fetchone()[0]
        
        # מלאי נמוך
        cur.execute("SELECT COUNT(*) FROM product WHERE amount < minamount")
        low_stock = cur.fetchone()[0]
        
        # סה"כ מכירות
        cur.execute("SELECT COUNT(*) FROM sale")
        total_sales = cur.fetchone()[0]
        
        # הכנסות כוללות
        cur.execute("SELECT SUM(totalprice) FROM sale")
        total_revenue = cur.fetchone()[0] or 0
        
        # מכירות היום
        cur.execute("SELECT COUNT(*) FROM sale WHERE saledate = %s", (date.today(),))
        today_sales = cur.fetchone()[0]
        
        # שווי מלאי
        cur.execute("SELECT SUM(price * amount) FROM product")
        inventory_value = cur.fetchone()[0] or 0
        
        cur.close()
        conn.close()
        
        return {
            'total_products': total_products,
            'low_stock': low_stock,
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'today_sales': today_sales,
            'inventory_value': inventory_value
        }
    except Exception as e:
        st.error(f"שגיאה בטעינת סטטיסטיקות: {e}")
        return {}

# דף הבית
if page == "🏠 דף הבית":
    st.markdown("## ברוכים הבאים למערכת ניהול החנות! 🎉")
    
    # כרטיסי מידע עיקריים
    stats = get_stats()
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 סה\"כ מוצרים", stats['total_products'])
        with col2:
            st.metric("🛒 סה\"כ מכירות", stats['total_sales'])
        with col3:
            st.metric("💰 הכנסות כוללות", f"₪{stats['total_revenue']:,.0f}")
        with col4:
            st.metric("🗓️ מכירות היום", stats['today_sales'])
    
    st.markdown("---")
    
    # הוראות שימוש
    st.markdown("""
    ### 🧭 איך להשתמש במערכת:
    
    **📦 ניהול מוצרים** - הוספה, עריכה וצפייה במוצרים  
    **🛒 ניהול מכירות** - רישום מכירות חדשות וצפייה בהיסטוריה  
    **📊 סטטיסטיקות** - גרפים ונתונים על הביצועים  
    **💸 ניהול הנחות** - יצירת הנחות ומעקב אחר סטטוס  
    **⚙️ שאילתות** - חיפושים מתקדמים במסד הנתונים  
    
    **💡 טיפ:** השתמש בתפריט הצדדי כדי לנווט בין המסכים השונים!
    """)

# מסך ניהול מוצרים
elif page == "📦 ניהול מוצרים":
    st.markdown("## 📦 ניהול מוצרים")
    
    # סטטיסטיקות מוצרים
    stats = get_stats()
    if stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📦 סה\"כ מוצרים", stats['total_products'])
        with col2:
            st.metric("⚠️ מלאי נמוך", stats['low_stock'])
        with col3:
            st.metric("💎 שווי מלאי", f"₪{stats['inventory_value']:,.0f}")
    
    st.markdown("---")
    
    # טופס הוספת מוצר
    st.markdown("### 🆕 הוספת מוצר חדש")
    
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("📝 שם מוצר")
            price = st.number_input("💰 מחיר", min_value=0.0, step=0.01)
            amount = st.number_input("📊 כמות", min_value=0, step=1)
        
        with col2:
            category = st.text_input("🏷️ קטגוריה")
            min_amount = st.number_input("⚠️ כמות מינימלית", min_value=0, step=1)
        
        submitted = st.form_submit_button("➕ הוסף מוצר", type="primary")
        
        if submitted:
            if product_name and price > 0:
                try:
                    conn = connect()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO product (product_name, price, amount, category, minamount, added_date, last_updated)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (product_name, price, amount, category, min_amount, date.today(), date.today()))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ המוצר נוסף בהצלחה!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ שגיאה בהוספת המוצר: {e}")
            else:
                st.error("❌ אנא מלא את כל השדות הנדרשים")
    
    st.markdown("---")
    
    # טבלת מוצרים
    st.markdown("### 📋 רשימת מוצרים")
    products_df = get_products()
    
    if not products_df.empty:
        # הוספת צבעים למלאי נמוך
        def highlight_low_stock(row):
            if row['amount'] < row['minamount']:
                return ['background-color: #fef2f2'] * len(row)
            return [''] * len(row)
        
        styled_df = products_df.style.apply(highlight_low_stock, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # סטטיסטיקות נוספות
        low_stock_count = len(products_df[products_df['amount'] < products_df['minamount']])
        if low_stock_count > 0:
            st.warning(f"⚠️ יש {low_stock_count} מוצרים עם מלאי נמוך!")
    else:
        st.info("אין מוצרים להצגה")

# מסך ניהול מכירות
elif page == "🛒 ניהול מכירות":
    st.markdown("## 🛒 ניהול מכירות")
    
    # סטטיסטיקות מכירות
    stats = get_stats()
    if stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 סה\"כ מכירות", stats['total_sales'])
        with col2:
            st.metric("💎 הכנסות כוללות", f"₪{stats['total_revenue']:,.0f}")
        with col3:
            st.metric("🗓️ מכירות היום", stats['today_sales'])
    
    st.markdown("---")
    
    # טופס הוספת מכירה
    st.markdown("### 🆕 הוספת מכירה חדשה")
    
    with st.form("add_sale_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            total_price = st.number_input("💰 סכום כולל (₪)", min_value=0.0, step=0.01)
        
        with col2:
            customer_id = st.number_input("👤 קוד לקוח", min_value=1, step=1)
        
        submitted = st.form_submit_button("➕ הוסף מכירה", type="primary")
        
        if submitted:
            if total_price > 0 and customer_id > 0:
                try:
                    conn = connect()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO sale (saledate, totalprice, customerid)
                        VALUES (%s, %s, %s)
                    """, (date.today(), total_price, customer_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ המכירה נוספה בהצלחה!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ שגיאה בהוספת המכירה: {e}")
            else:
                st.error("❌ אנא מלא את כל השדות בצורה תקינה")
    
    st.markdown("---")
    
    # טבלת מכירות
    st.markdown("### 📋 רשימת מכירות")
    sales_df = get_sales()
    
    if not sales_df.empty:
        # פורמט התאריכים והמחירים
        sales_df['totalprice'] = sales_df['totalprice'].apply(lambda x: f"₪{x:,.2f}")
        st.dataframe(sales_df, use_container_width=True, height=400)
    else:
        st.info("אין מכירות להצגה")

# מסך סטטיסטיקות
elif page == "📊 סטטיסטיקות":
    st.markdown("## 📊 סטטיסטיקות החנות")
    
    stats = get_stats()
    
    # כרטיסי סטטיסטיקות עליונים
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🛒 סה\"כ מכירות", stats.get('total_sales', 0))
    with col2:
        st.metric("💰 הכנסות כוללות", f"₪{stats.get('total_revenue', 0):,.0f}")
    with col3:
        st.metric("⚠️ מלאי נמוך", stats.get('low_stock', 0))
    with col4:
        st.metric("📦 סה\"כ מוצרים", stats.get('total_products', 0))
    
    st.markdown("---")
    
    # גרפי מכירות
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 מכירות שבועיות")
        
        # נתונים לדוגמה
        days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
        sales_data = [12, 18, 15, 22, 25, 30, 8]
        
        fig = px.bar(
            x=days, 
            y=sales_data,
            labels={'x': 'יום', 'y': 'מכירות'},
            color=sales_data,
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 מוצרים פופולריים")
        
        # נתונים לדוגמה
        products = ["חולצה כחולה", "מכנסיים שחורים", "נעליים לבנות", "תיק יד", "משקפי שמש"]
        counts = [45, 38, 32, 28, 22]
        
        fig = px.pie(
            values=counts,
            names=products,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # טבלאות מפורטות
    st.markdown("---")
    st.markdown("### 📋 נתונים מפורטים")
    
    tab1, tab2 = st.tabs(["מוצרים עם מלאי נמוך", "מכירות אחרונות"])
    
    with tab1:
        try:
            conn = connect()
            low_stock_query = "SELECT product_name, amount, minamount FROM product WHERE amount < minamount"
            low_stock_df = pd.read_sql(low_stock_query, conn)
            conn.close()
            
            if not low_stock_df.empty:
                st.dataframe(low_stock_df, use_container_width=True)
            else:
                st.success("✅ כל המוצרים עם מלאי תקין!")
        except Exception as e:
            st.error(f"שגיאה: {e}")
    
    with tab2:
        sales_df = get_sales()
        if not sales_df.empty:
            st.dataframe(sales_df.head(10), use_container_width=True)

# מסך ניהול הנחות
elif page == "💸 ניהול הנחות":
    st.markdown("## 💸 ניהול הנחות")
    
    # טופס הוספת הנחה
    st.markdown("### 🆕 הוספת הנחה חדשה")
    
    with st.form("add_discount_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            discount_rate = st.number_input("📊 שיעור הנחה (%)", min_value=0.0, max_value=100.0, step=0.1)
            product_id = st.number_input("📦 מספר מוצר", min_value=1, step=1)
        
        with col2:
            store_id = st.number_input("🏪 מספר סניף", min_value=1, step=1)
            start_date = st.date_input("📅 תאריך התחלה")
        
        with col3:
            end_date = st.date_input("📅 תאריך סיום")
        
        submitted = st.form_submit_button("➕ הוסף הנחה", type="primary")
        
        if submitted:
            if discount_rate > 0 and start_date <= end_date:
                try:
                    conn = connect()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO discount (discountrate, startdate, enddate, storeid, productid)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (discount_rate, start_date, end_date, store_id, product_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ ההנחה נוספה בהצלחה!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ שגיאה בהוספת ההנחה: {e}")
            else:
                st.error("❌ אנא בדוק את הנתונים שהוזנו")
    
    st.markdown("---")
    
    # טבלת הנחות
    st.markdown("### 📋 רשימת הנחות")
    discounts_df = get_discounts()
    
    if not discounts_df.empty:
        # הוספת סטטוס פעילות
        today = date.today()
        
        def get_status(row):
            start = pd.to_datetime(row['startdate']).date()
            end = pd.to_datetime(row['enddate']).date()
            if start <= today <= end:
                return "פעילה ✅"
            else:
                return "לא פעילה ❌"
        
        discounts_df['סטטוס'] = discounts_df.apply(get_status, axis=1)
        
        # צביעת השורות לפי סטטוס
        def highlight_status(row):
            if row['סטטוס'] == "פעילה ✅":
                return ['background-color: #dcfce7'] * len(row)
            else:
                return ['background-color: #fef2f2'] * len(row)
        
        styled_df = discounts_df.style.apply(highlight_status, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=400)
    else:
        st.info("אין הנחות להצגה")

# מסך שאילתות
elif page == "⚙️ שאילתות":
    st.markdown("## ⚙️ שאילתות ופרוצדורות")
    
    # רשימת שאילתות
    queries = {
        "כל המוצרים": {
            "query": "SELECT product_id, product_name, price, amount, category FROM product ORDER BY product_name",
            "description": "הצגת כל המוצרים במערכת",
            "params": []
        },
        "מוצרים עם מלאי נמוך": {
            "query": "SELECT product_id, product_name, amount, minamount FROM product WHERE amount < minamount",
            "description": "מוצרים שהכמות שלהם נמוכה מהמינימום הנדרש",
            "params": []
        },
        "כל המכירות": {
            "query": "SELECT saleid, saledate, totalprice, customerid FROM sale ORDER BY saledate DESC",
            "description": "רשימת כל המכירות במערכת",
            "params": []
        },
        "מכירות לפי לקוח": {
            "query": "SELECT s.saleid, s.saledate, s.totalprice FROM sale s WHERE s.customerid = %s ORDER BY s.saledate DESC",
            "description": "מכירות של לקוח ספציפי",
            "params": ["קוד לקוח"]
        },
        "הנחות פעילות": {
            "query": "SELECT d.discountid, p.product_name, d.discountrate FROM discount d JOIN product p ON d.productid = p.product_id WHERE d.startdate <= CURRENT_DATE AND d.enddate >= CURRENT_DATE",
            "description": "הנחות שפעילות כרגע",
            "params": []
        }
    }
    
    # בחירת שאילתה
    selected_query = st.selectbox("🔍 בחר שאילתה:", list(queries.keys()))
    
    if selected_query:
        query_data = queries[selected_query]
        st.info(f"📋 {query_data['description']}")
        
        # פרמטרים אם יש
        params = []
        if query_data['params']:
            st.markdown("### 📝 פרמטרים נדרשים:")
            for param in query_data['params']:
                if param == "קוד לקוח":
                    value = st.number_input(param, min_value=1, step=1)
                    params.append(value)
                else:
                    value = st.text_input(param)
                    params.append(value)
        
        # כפתור הפעלה
        if st.button("▶️ הפעל שאילתה", type="primary"):
            try:
                conn = connect()
                
                if params:
                    df = pd.read_sql(query_data['query'], conn, params=params)
                else:
                    df = pd.read_sql(query_data['query'], conn)
                
                conn.close()
                
                if not df.empty:
                    st.success(f"✅ נמצאו {len(df)} תוצאות")
                    st.dataframe(df, use_container_width=True, height=400)
                else:
                    st.warning("ℹ️ לא נמצאו תוצאות")
                    
            except Exception as e:
                st.error(f"❌ שגיאה בביצוע השאילתה: {e}")

# רווח תחתון
st.markdown("---")
st.markdown("** מערכת פעילה** |  ❤️ Michal Zanzuri & Yael Bouskila-Ditchi")
