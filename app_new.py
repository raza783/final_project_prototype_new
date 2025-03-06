import streamlit as st
import pandas as pd
import plotly.express as px

# יצירת משתני נתונים בסביבת `session_state`
if "projects_data" not in st.session_state:
    st.session_state.projects_data = pd.DataFrame({
        "פרויקט": ["A", "B", "C"],
        "סטטוס": ["ממתין לרישוי", "בתהליך רישוי", "התקנה"],
        "מסמכים": [2, 5, 3],
        "תשלומים": ["לא שולם", "שולם", "שולם"],
        "שביעות רצון": [6.5, 7.8, 8.2],
        "זמן ביצוע (שבועות)": [8, 7, 9]
    })

if "requests_data" not in st.session_state:
    st.session_state.requests_data = []

if "users" not in st.session_state:
    st.session_state.users = {}

st.set_page_config(page_title="הבית הירוק - מערכת ניהול", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>מערכת ניהול - הבית הירוק</h1>", unsafe_allow_html=True)

def main():
    choice = st.sidebar.selectbox("בחר סוג התחברות", ["לקוח", "מנהל פרויקטים", "מנהל חברה"])
    username = st.sidebar.text_input("שם משתמש")
    password = st.sidebar.text_input("סיסמא", type="password")

    # כל משתמש יכול להיכנס ללא בדיקה
    if choice == "לקוח":
        customer_dashboard(username)
    elif choice == "מנהל פרויקטים":
        project_manager_dashboard(username)
    elif choice == "מנהל חברה":
        company_manager_dashboard(username)

def customer_dashboard(username):
    st.subheader(f"שלום, {username} 👋")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "סטטוס פרויקט", "ניהול מסמכים", "אגרות", "פנייה חדשה"])

    if page == "עמוד ראשי":
        st.subheader("📌 סטטוס הפרויקט שלך")
        st.write("🔹 פרויקט A - ממתין לרישוי")
        st.progress(0.3)

    elif page == "סטטוס פרויקט":
        st.subheader("🔍 ציר זמן הפרויקט")
        timeline = ["פתיחת פרויקט", "שלב רישוי", "המתנה להתקנה", "התקנה", "חיבור לרשת"]
        st.selectbox("שלב נוכחי בפרויקט:", timeline, index=1, disabled=True)

    elif page == "ניהול מסמכים":
        st.subheader("📄 ניהול מסמכים")
        with st.form("document_upload_form"):
            uploaded_file = st.file_uploader("📂 העלה מסמך")
            submit_button = st.form_submit_button("✅ שלח")
            if submit_button and uploaded_file:
                st.success("📌 המסמך הועלה בהצלחה!")

    elif page == "אגרות":
        st.subheader("💳 תשלומים ואגרות")
        st.write("🔹 סטטוס תשלום: לא שולם")
        if st.button("שלם עכשיו"):
            st.session_state.projects_data.loc[st.session_state.projects_data["פרויקט"] == "A", "תשלומים"] = "שולם"
            st.success("✅ התשלום התקבל!")

    elif page == "פנייה חדשה":
        st.subheader("📨 שליחת פנייה")
        request_text = st.text_area("תוכן הפנייה:")
        if st.button("שלח פנייה"):
            st.session_state.requests_data.append({"לקוח": username, "תוכן": request_text, "סטטוס": "פתוח"})
            st.success("✅ הפנייה נשלחה!")

def project_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👷‍♂️")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "פרויקטים פעילים", "ניהול מסמכים", "דוחות", "פניות", "פתיחת פרויקט חדש"])

    if page == "עמוד ראשי":
        st.subheader("📌 סטטוס כללי של הפרויקטים")
        st.progress(0.6)

    elif page == "פרויקטים פעילים":
        st.subheader("📋 פרויקטים פעילים")
        st.table(st.session_state.projects_data)

    elif page == "ניהול מסמכים":
        st.subheader("📄 מסמכים שהועלו על ידי לקוחות")
        st.table(st.session_state.projects_data[["פרויקט", "מסמכים"]])

    elif page == "דוחות":
        st.subheader("📊 גרף מסמכים שהועלו לכל פרויקט")
        fig = px.bar(st.session_state.projects_data, x="פרויקט", y="מסמכים", title="כמות מסמכים שהועלו")
        st.plotly_chart(fig)

    elif page == "פניות":
        st.subheader("📨 פניות לקוחות")
        for req in st.session_state.requests_data:
            st.write(f"👤 {req['לקוח']} - {req['תוכן']}")
            if st.button(f"סגור פנייה - {req['לקוח']}"):
                req["סטטוס"] = "סגור"
                st.success("✅ הפנייה נסגרה!")

    elif page == "פתיחת פרויקט חדש":
        st.subheader("🏗️ יצירת פרויקט חדש")
        project_name = st.text_input("שם הפרויקט")
        
        if st.button("צור פרויקט"):
            new_project = pd.DataFrame([{
                "פרויקט": project_name,
                "סטטוס": "בתכנון",
                "מסמכים": 0,
                "תשלומים": "לא שולם"
            }])
            
            st.session_state.projects_data = pd.concat([st.session_state.projects_data, new_project], ignore_index=True)
            st.success(f"✅ פרויקט {project_name} נוצר בהצלחה!")

def company_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👨‍💼")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "תשלומים", "דוחות"])

    if page == "תשלומים":
        st.subheader("💰 מצב תשלומים בפרויקטים")
        st.table(st.session_state.projects_data[["פרויקט", "תשלומים"]])
        if st.button("שלח תזכורת ללקוחות"):
            st.success("📢 תזכורת תשלום נשלחה לכל הלקוחות!")

    elif page == "דוחות":
        st.subheader("📊 דוחות עסקיים")
        fig = px.bar(st.session_state.projects_data, x="פרויקט", y="שביעות רצון", title="שביעות רצון לקוחות")
        st.plotly_chart(fig)

# הפעלת האפליקציה
if __name__ == "__main__":
    main()
