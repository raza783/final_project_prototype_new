import streamlit as st
import pandas as pd
import time

# הגדרת כותרת ועיצוב ראשי
st.set_page_config(page_title="הבית הירוק - מערכת ניהול", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>מערכת ניהול - הבית הירוק</h1>", unsafe_allow_html=True)

# התחברות משתמשים
choice = st.selectbox("בחר סוג התחברות", ["לקוח", "מנהל פרויקטים", "מנהל חברה"])
username = st.text_input("שם משתמש")
password = st.text_input("סיסמא", type="password")

if username and password:
    if choice == "לקוח":
        customer_dashboard(username)
    elif choice == "מנהל פרויקטים":
        project_manager_dashboard(username)
    elif choice == "מנהל חברה":
        company_manager_dashboard(username)

# דשבורד לקוח עם סטטוס פרויקט ותזכורות
def customer_dashboard(username):
    st.subheader(f"שלום, {username}")
    
    # ניווט ראשי
    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "סטטוס פרויקט", "ניהול מסמכים", "אגרות"])

    if page == "עמוד ראשי":
        st.subheader("עמוד ראשי")
        st.write("🔔 התראות: עליך להעלות מסמך חיבור עד 5.1")
        st.toast("תזכורת: נותרו לך 3 ימים להשלמת המסמכים!", icon="⚠️")

        # התקדמות הפרויקט
        progress_value = 0.6  # ערך מדומה
        st.progress(progress_value)
        st.write(f"סטטוס הפרויקט: {int(progress_value * 100)}% הושלם")

    elif page == "סטטוס פרויקט":
        st.subheader("סטטוס פרויקט")
        steps = ["בתהליך רישוי", "ממתין להתקנה", "התקנה"]
        progress_step = st.radio("שלב נוכחי", steps, index=1)

    elif page == "ניהול מסמכים":
        st.subheader("ניהול מסמכים")
        with st.form("document_upload_form"):
            uploaded_file = st.file_uploader("העלה מסמך")
            submit_button = st.form_submit_button("שלח")
            if submit_button and uploaded_file:
                st.success("✅ המסמך הועלה בהצלחה!")

    elif page == "אגרות":
        st.subheader("תשלומים ואגרות")
        fees = pd.DataFrame({
            "אגרה": ["רישום", "היתר", "חיבור"],
            "סטטוס": ["שולם", "ממתין", "ממתין"],
            "תשלום": ["✔️", "🔗 לחץ כאן", "🔗 לחץ כאן"]
        })
        st.table(fees)

# דשבורד למנהל פרויקטים עם יכולת עדכון
def project_manager_dashboard(username):
    st.subheader(f"שלום, {username}")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "פרויקטים פעילים", "ארכיון פרויקטים", "ניהול מסמכים"])

    if page == "עמוד ראשי":
        st.subheader("דשבורד מנהל פרויקטים")
        st.write("🔔 עדכון: 2 פרויקטים נמצאים בעיכוב!")

    elif page == "פרויקטים פעילים":
        st.subheader("פרויקטים פעילים")
        projects_data = pd.DataFrame({"פרויקט": ["פרויקט A", "פרויקט B"], "סטטוס": ["בתהליך רישוי", "ממתין להתקנה"]})
        st.table(projects_data)

        # הוספת כפתור לעדכון סטטוס
        selected_project = st.selectbox("בחר פרויקט לעדכון", projects_data["פרויקט"])
        new_status = st.selectbox("עדכן סטטוס", ["בתהליך רישוי", "ממתין להתקנה", "הושלם"])
        if st.button("עדכן סטטוס"):
            st.success(f"✅ סטטוס {selected_project} עודכן ל- {new_status}")
            time.sleep(1)
            st.experimental_rerun()

    elif page == "ניהול מסמכים":
        st.subheader("העלאת מסמכים")
        uploaded_file = st.file_uploader("העלה מסמך")
        if uploaded_file:
            st.success("✅ המסמך הועלה בהצלחה!")

# דשבורד למנהל חברה עם תכנון מלאי חכם
def company_manager_dashboard(username):
    st.subheader(f"שלום, {username}")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "תשלומים", "פרויקטים פעילים", "ניהול מלאי"])

    if page == "ניהול מלאי":
        st.subheader("📦 ניהול מלאי והזמנות")
        st.write("🔹 תכנון הזמנות לפי **מודל EOQ**")

        order_quantity = st.slider("בחר מספר מכולות להזמנה", min_value=1, max_value=10, value=5)
        total_cost = 1_700_000 - (order_quantity * 30_000)
        st.write(f"💰 עלות שנתית משוערת: **{total_cost:,.0f}** ₪")

        if st.button("חשב הזמנה אופטימלית"):
            st.success(f"✅ מומלץ להזמין {order_quantity} מכולות לכל הזמנה!")

# הרצת האפליקציה
if __name__ == "__main__":
    main()
