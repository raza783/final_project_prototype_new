import streamlit as st
import pandas as pd
import plotly.express as px

# יצירת משתנים גלובליים במערכת
if "projects_data" not in st.session_state:
    st.session_state.projects_data = pd.DataFrame({
        "פרויקט": ["A", "B", "C"],
        "סטטוס": ["ממתין לרישוי", "בתהליך רישוי", "התקנה"],
        "מסמכים": [2, 5, 3],
        "תשלומים": [1, 3, 2],  # מתוך 3
        "שביעות רצון": [6.5, 7.8, 8.2],
        "זמן ביצוע (שבועות)": [8, 7, 9]
    })

if "requests_data" not in st.session_state:
    st.session_state.requests_data = []

if "document_status" not in st.session_state:
    st.session_state.document_status = {
        "A": {"תצהיר עורך דין": False, "אישור רישוי": False, "מסמך חיבור": False},
        "B": {"תצהיר עורך דין": True, "אישור רישוי": False, "מסמך חיבור": True},
        "C": {"תצהיר עורך דין": True, "אישור רישוי": True, "מסמך חיבור": True}
    }

if "inventory_data" not in st.session_state:
    st.session_state.inventory_data = {"סה״כ מלאי": 100, "עלות הזמנה": 30000, "עלות אחסון": 5000}

if "payment_requests" not in st.session_state:
    st.session_state.payment_requests = {}

st.set_page_config(page_title="הבית הירוק - מערכת ניהול", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>מערכת ניהול - הבית הירוק</h1>", unsafe_allow_html=True)

def main():
    choice = st.sidebar.selectbox("בחר סוג התחברות", ["לקוח", "מנהל פרויקטים", "מנהל חברה"])
    username = st.sidebar.text_input("שם משתמש")
    password = st.sidebar.text_input("סיסמא", type="password")

    if choice == "לקוח":
        customer_dashboard(username)
    elif choice == "מנהל פרויקטים":
        project_manager_dashboard(username)
    elif choice == "מנהל חברה":
        company_manager_dashboard(username)

# 🔹 דשבורד לקוח
def customer_dashboard(username):
    st.subheader(f"שלום, {username} 👋")

    page = st.sidebar.radio("ניווט", ["סטטוס פרויקט", "ניהול מסמכים", "אגרות", "פנייה חדשה"])

    if page == "סטטוס פרויקט":
        st.subheader("🔍 ציר זמן הפרויקט")
        st.write(f"🔹 סטטוס נוכחי: {st.session_state.projects_data.loc[0, 'סטטוס']}")
        timeline = ["פתיחת פרויקט", "שלב רישוי", "המתנה להתקנה", "התקנה", "חיבור לרשת"]
        current_status = st.session_state.projects_data.loc[0, 'סטטוס']
        index = timeline.index(current_status) if current_status in timeline else 0
        st.selectbox("שלב נוכחי בפרויקט:", timeline, index=index, disabled=True)

# 🔹 דשבורד מנהל פרויקטים
def project_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👷‍♂️")

    page = st.sidebar.radio("ניווט", ["פרויקטים פעילים", "ניהול מסמכים", "דוחות", "פניות"])

    if page == "דוחות":
        st.subheader("📊 דוחות ביצוע")
        fig1 = px.bar(st.session_state.projects_data, x="פרויקט", y="זמן ביצוע (שבועות)", title="⏳ משך זמן פרויקטים")
        fig2 = px.bar(st.session_state.projects_data, x="פרויקט", y="מסמכים", title="📄 מסמכים שהועלו מתוך 6")
        fig3 = px.bar(st.session_state.projects_data, x="פרויקט", y="תשלומים", title="💰 אגרות ששולמו מתוך 3")
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)

# 🔹 דשבורד בעל החברה
def company_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👨‍💼")

    page = st.sidebar.radio("ניווט", ["תשלומים", "דוחות", "ניהול מלאי", "פניות"])

    if page == "ניהול מלאי":
        st.subheader("📦 ניהול מלאי לפי מודל EOQ")
        order_quantity = st.slider("בחר מספר מכולות להזמנה", min_value=1, max_value=10, value=5)
        total_cost = 1_700_000 - (order_quantity * 30_000)
        st.write(f"💰 עלות שנתית משוערת: **{total_cost:,.0f}** ₪")
        if st.button("חשב הזמנה אופטימלית"):
            st.success(f"✅ מומלץ להזמין {order_quantity} מכולות לכל הזמנה!")

# הפעלת האפליקציה
if __name__ == "__main__":
    main()
