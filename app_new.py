import streamlit as st
import pandas as pd
import plotly.express as px

# משתנים כלליים למערכת
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

if "archive_projects" not in st.session_state:
    st.session_state.archive_projects = 0

if "payment_requests" not in st.session_state:
    st.session_state.payment_requests = {}

if "inventory_data" not in st.session_state:
    st.session_state.inventory_data = {"סה״כ מלאי": 100, "עלות הזמנה": 30000, "עלות אחסון": 5000}

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

def customer_dashboard(username):
    st.subheader(f"שלום, {username} 👋")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "סטטוס פרויקט", "ניהול מסמכים", "אגרות", "פנייה חדשה"])

    if page == "ניהול מסמכים":
        st.subheader("📄 ניהול מסמכים")
        for doc in st.session_state.document_status["A"]:
            st.write(f"📌 {doc} - {'🟢 הועלה' if st.session_state.document_status['A'][doc] else '🔴 נדרש להעלאה'}")
        with st.form("document_upload_form"):
            doc_choice = st.selectbox("בחר מסמך להעלאה", list(st.session_state.document_status["A"].keys()))
            uploaded_file = st.file_uploader("📂 העלה מסמך")
            submit_button = st.form_submit_button("✅ שלח")
            if submit_button and uploaded_file:
                st.session_state.document_status["A"][doc_choice] = True
                st.success(f"📌 {doc_choice} הועלה בהצלחה!")

    elif page == "פנייה חדשה":
        st.subheader("📨 שליחת פנייה")
        request_text = st.text_area("תוכן הפנייה:")
        if st.button("שלח פנייה"):
            st.session_state.requests_data.append({"לקוח": username, "תוכן": request_text, "סטטוס": "פתוח"})
            st.success("✅ הפנייה נשלחה!")

def project_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👷‍♂️")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "פרויקטים פעילים", "ניהול מסמכים", "דוחות", "פניות"])

    if page == "ניהול מסמכים":
        st.subheader("📄 מסמכים בפרויקטים")
        for project, docs in st.session_state.document_status.items():
            st.write(f"📌 {project}: {sum(docs.values())} מסמכים הועלו מתוך {len(docs)}")

    elif page == "פניות":
        st.subheader("📨 פניות לקוחות")
        for req in st.session_state.requests_data:
            st.write(f"👤 {req['לקוח']} - {req['תוכן']}")
            if st.button(f"מענה לפנייה - {req['לקוח']}"):
                req["סטטוס"] = "סגור"
                st.success("✅ הפנייה טופלה!")

def company_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👨‍💼")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "תשלומים", "דוחות", "ניהול מלאי", "פניות"])

    if page == "תשלומים":
        st.subheader("💰 מצב תשלומים")
        for project in st.session_state.projects_data["פרויקט"]:
            if st.button(f"שלח דרישת תשלום ל-{project}"):
                st.session_state.payment_requests[project] = True
                st.success(f"💳 דרישת תשלום נשלחה ל-{project}!")

    elif page == "ניהול מלאי":
        st.subheader("📦 ניהול מלאי")
        st.write(f"📦 סה״כ מלאי: {st.session_state.inventory_data['סה״כ מלאי']} יחידות")
        if st.button("חשב מלאי לפי EOQ"):
            order_quantity = 10
            st.session_state.inventory_data["סה״כ מלאי"] += order_quantity
            st.success(f"📦 הזמנה בוצעה! מלאי חדש: {st.session_state.inventory_data['סה״כ מלאי']}")

    elif page == "פניות":
        st.subheader("📨 פניות לקוחות")
        for req in st.session_state.requests_data:
            st.write(f"👤 {req['לקוח']} - {req['תוכן']}")
            if st.button(f"מענה לפנייה - {req['לקוח']}"):
                req["סטטוס"] = "סגור"
                st.success("✅ הפנייה טופלה!")

# הפעלת האפליקציה
if __name__ == "__main__":
    main()
