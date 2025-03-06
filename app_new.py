import streamlit as st
import pandas as pd
import plotly.express as px
import time

# הגדרת תצוגת המערכת
st.set_page_config(page_title="הבית הירוק - מערכת ניהול", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>מערכת ניהול - הבית הירוק</h1>", unsafe_allow_html=True)

# פונקציה ראשית לניהול משתמשים
def main():
    choice = st.sidebar.selectbox("בחר סוג התחברות", ["לקוח", "מנהל פרויקטים", "מנהל חברה"])
    username = st.sidebar.text_input("שם משתמש")
    password = st.sidebar.text_input("סיסמא", type="password")

    if username and password:
        if choice == "לקוח":
            customer_dashboard(username)
        elif choice == "מנהל פרויקטים":
            project_manager_dashboard(username)
        elif choice == "מנהל חברה":
            company_manager_dashboard(username)

# 🔹 דשבורד לקוח
def customer_dashboard(username):
    st.subheader(f"שלום, {username} 👋")
    
    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "סטטוס פרויקט", "ניהול מסמכים", "אגרות"])

    if page == "עמוד ראשי":
        st.subheader("📌 סטטוס הפרויקט שלך")
        st.progress(0.6)
        st.write("סטטוס נוכחי: בתהליך רישוי (60%)")
        st.toast("🔔 תזכורת: יש להעלות מסמך חיבור עד 5.1!", icon="⚠️")

    elif page == "סטטוס פרויקט":
        st.subheader("🔍 ציר זמן הפרויקט")
        timeline = ["פתיחת פרויקט", "שלב רישוי", "המתנה להתקנה", "התקנה", "חיבור לרשת"]
        st.selectbox("שלב נוכחי בפרויקט:", timeline, index=1)

    elif page == "ניהול מסמכים":
        st.subheader("📄 ניהול מסמכים")
        with st.form("document_upload_form"):
            uploaded_file = st.file_uploader("📂 העלה מסמך")
            submit_button = st.form_submit_button("✅ שלח")
            if submit_button and uploaded_file:
                st.success("📌 המסמך הועלה בהצלחה!")

    elif page == "אגרות":
        st.subheader("💳 תשלומים ואגרות")
        fees = pd.DataFrame({"אגרה": ["רישום", "היתר", "חיבור"], "סטטוס": ["שולם", "ממתין", "ממתין"]})
        st.table(fees)

# 🔹 דשבורד מנהל פרויקטים
def project_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👷‍♂️")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "פרויקטים פעילים", "ניהול מסמכים", "דוחות"])

    if page == "עמוד ראשי":
        st.subheader("🔔 התראות ניהול פרויקטים")
        st.write("⚠️ ישנם 2 פרויקטים בעיכוב!")

    elif page == "פרויקטים פעילים":
        st.subheader("📌 פרויקטים פעילים")
        projects_data = pd.DataFrame({"פרויקט": ["פרויקט A", "פרויקט B"], "סטטוס": ["בתהליך רישוי", "ממתין להתקנה"]})
        st.table(projects_data)

        # עדכון סטטוס פרויקט
        selected_project = st.selectbox("בחר פרויקט לעדכון", projects_data["פרויקט"])
        new_status = st.selectbox("עדכן סטטוס", ["בתהליך רישוי", "ממתין להתקנה", "הושלם"])
        if st.button("עדכן סטטוס"):
            st.success(f"✅ סטטוס {selected_project} עודכן ל- {new_status}")
            time.sleep(1)
            st.experimental_rerun()

    elif page == "דוחות":
        st.subheader("📊 דוחות ביצועים")
        chart_data = pd.DataFrame({"פרויקט": ["A", "B", "C"], "זמן ביצוע (שבועות)": [8, 7, 9]})
        fig = px.bar(chart_data, x="פרויקט", y="זמן ביצוע (שבועות)", title="משך זמן ביצוע פרויקטים")
        st.plotly_chart(fig)

# 🔹 דשבורד מנהל חברה
def company_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👨‍💼")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "תשלומים", "ניהול מלאי", "ניתוח פרויקטים"])

    if page == "ניהול מלאי":
        st.subheader("📦 ניהול מלאי לפי מודל EOQ")
        order_quantity = st.slider("בחר מספר מכולות להזמנה", min_value=1, max_value=10, value=5)
        total_cost = 1_700_000 - (order_quantity * 30_000)
        st.write(f"💰 עלות שנתית משוערת: **{total_cost:,.0f}** ₪")

        if st.button("חשב הזמנה אופטימלית"):
            st.success(f"✅ מומלץ להזמין {order_quantity} מכולות לכל הזמנה!")

    elif page == "ניתוח פרויקטים":
        st.subheader("📊 ניתוח פרויקטים")
        summary_data = pd.DataFrame({"מדד": ["זמן ממוצע לפרויקט", "שביעות רצון לקוחות", "חיסכון מלאי"],
                                     "ערך נוכחי": [8, 6.5, "₪ 305,360"],
                                     "ערך יעד": [6, 8, "₪ 500,000"]})
        st.table(summary_data)

# הפעלת האפליקציה
if __name__ == "__main__":
    main()
