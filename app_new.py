import streamlit as st
import pandas as pd
import plotly.express as px

# יצירת משתני נתונים בסביבת `session_state`
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

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "סטטוס פרויקט", "ניהול מסמכים", "אגרות"])

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
        for doc in st.session_state.document_status["A"]:
            st.write(f"📌 {doc} - {'🟢 הועלה' if st.session_state.document_status['A'][doc] else '🔴 נדרש להעלאה'}")
        with st.form("document_upload_form"):
            doc_choice = st.selectbox("בחר מסמך להעלאה", list(st.session_state.document_status["A"].keys()))
            uploaded_file = st.file_uploader("📂 העלה מסמך")
            submit_button = st.form_submit_button("✅ שלח")
            if submit_button and uploaded_file:
                st.session_state.document_status["A"][doc_choice] = True
                st.success(f"📌 {doc_choice} הועלה בהצלחה!")

    elif page == "אגרות":
        st.subheader("💳 תשלומים ואגרות")
        st.write(f"🔹 שילמת {st.session_state.projects_data.loc[0, 'תשלומים']} מתוך 3")
        if st.button("שלם עכשיו"):
            st.session_state.projects_data.loc[0, "תשלומים"] += 1
            st.success("✅ התשלום התקבל!")

def project_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👷‍♂️")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "פרויקטים פעילים", "ניהול מסמכים", "דוחות", "פתיחת פרויקט חדש"])

    if page == "עמוד ראשי":
        st.subheader("📌 סקירת פרויקטים")
        st.write(f"🔹 פרויקטים בתהליך: {len(st.session_state.projects_data)}")
        st.write(f"📁 פרויקטים בארכיון: {st.session_state.archive_projects}")
        for i, row in st.session_state.projects_data.iterrows():
            st.write(f"📌 {row['פרויקט']} - {row['סטטוס']}")
            st.progress((i+1) * 0.3)

    elif page == "דוחות":
        st.subheader("📊 ניתוח ביצועי פרויקטים")
        fig1 = px.bar(st.session_state.projects_data, x="פרויקט", y="זמן ביצוע (שבועות)", title="⏳ משך זמן פרויקטים")
        st.plotly_chart(fig1)

    elif page == "פתיחת פרויקט חדש":
        st.subheader("🏗️ יצירת פרויקט חדש")
        project_name = st.text_input("שם הפרויקט")
        if st.button("צור פרויקט"):
            new_project = pd.DataFrame([{
                "פרויקט": project_name,
                "סטטוס": "בתכנון",
                "מסמכים": 0,
                "תשלומים": 0
            }])
            st.session_state.projects_data = pd.concat([st.session_state.projects_data, new_project], ignore_index=True)
            st.success(f"✅ פרויקט {project_name} נוצר בהצלחה!")

def company_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👨‍💼")

    page = st.sidebar.radio("ניווט", ["עמוד ראשי", "תשלומים", "דוחות"])

    if page == "תשלומים":
        st.subheader("💰 מצב תשלומים בפרויקטים")
        st.table(st.session_state.projects_data[["פרויקט", "תשלומים"]])

    elif page == "דוחות":
        st.subheader("📊 דוחות אסטרטגיים")
        fig1 = px.bar(st.session_state.projects_data, x="פרויקט", y="זמן ביצוע (שבועות)", title="⏳ משך זמן פרויקטים")
        st.plotly_chart(fig1)
        fig2 = px.bar(st.session_state.projects_data, x="פרויקט", y="שביעות רצון", title="💬 שביעות רצון לקוחות")
        st.plotly_chart(fig2)

# הפעלת האפליקציה
if __name__ == "__main__":
    main()
