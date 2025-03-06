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

    elif page == "ניהול מסמכים":
        st.subheader("📄 ניהול מסמכים")
        for doc, status in st.session_state.document_status["A"].items():
            st.write(f"📌 {doc} - {'🟢 הועלה' if status else '🔴 נדרש להעלאה'}")
        with st.form("document_upload_form"):
            doc_choice = st.selectbox("בחר מסמך להעלאה", list(st.session_state.document_status["A"].keys()))
            uploaded_file = st.file_uploader("📂 העלה מסמך")
            submit_button = st.form_submit_button("✅ שלח")
            if submit_button and uploaded_file:
                st.session_state.document_status["A"][doc_choice] = True
                st.success(f"📌 {doc_choice} הועלה בהצלחה!")

    elif page == "אגרות":
        st.subheader("💳 תשלומים ואגרות")
        paid = st.session_state.projects_data.loc[0, "תשלומים"]
        total_fees = 3
        st.write(f"🔹 שילמת {paid} מתוך {total_fees}")
        if st.button("שלם עכשיו"):
            if paid < total_fees:
                st.session_state.projects_data.loc[0, "תשלומים"] += 1
                st.success(f"✅ התשלום התקבל! כעת שילמת {st.session_state.projects_data.loc[0, 'תשלומים']} מתוך {total_fees}.")
            else:
                st.warning("💰 כל האגרות כבר שולמו!")

    elif page == "פנייה חדשה":
        st.subheader("📨 שליחת פנייה")
        request_text = st.text_area("תוכן הפנייה:")
        if st.button("שלח פנייה"):
            if request_text:
                st.session_state.requests_data.append({"לקוח": username, "תוכן": request_text, "סטטוס": "פתוח"})
                st.success("✅ הפנייה נשלחה!")
            else:
                st.warning("❗ יש להזין תוכן לפנייה לפני השליחה.")

def project_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👷‍♂️")

    page = st.sidebar.radio("ניווט", ["פרויקטים פעילים", "ניהול מסמכים", "דוחות", "פניות"])

    if page == "פרויקטים פעילים":
        st.subheader("📋 רשימת פרויקטים פעילים")
        for i, row in st.session_state.projects_data.iterrows():
            st.write(f"📌 {row['פרויקט']} - סטטוס: {row['סטטוס']}")
            st.progress((i + 1) * 0.3)

    elif page == "ניהול מסמכים":
        st.subheader("📄 מסמכים בפרויקטים")
        for project, docs in st.session_state.document_status.items():
            completed_docs = sum(docs.values())
            total_docs = len(docs)
            st.write(f"📌 {project}: {completed_docs} מסמכים הועלו מתוך {total_docs}")

    elif page == "פניות":
        st.subheader("📨 פניות לקוחות")
        for req in st.session_state.requests_data:
            if req["סטטוס"] == "פתוח":
                st.write(f"👤 {req['לקוח']} - {req['תוכן']}")
                if st.button(f"מענה לפנייה - {req['לקוח']}"):
                    req["סטטוס"] = "סגור"
                    st.success("✅ הפנייה טופלה!")
    elif page == "דוחות":
        st.subheader("📊 דוחות אסטרטגיים")
        fig1 = px.bar(st.session_state.projects_data, x="פרויקט", y="זמן ביצוע (שבועות)", title="⏳ משך זמן פרויקטים")
        fig2 = px.bar(st.session_state.projects_data, x="פרויקט", y="שביעות רצון", title="💬 שביעות רצון לקוחות")
        fig3 = px.bar(st.session_state.projects_data, x="פרויקט", y="תשלומים", title="💰 אגרות ששולמו מתוך 3")
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
                  

def company_manager_dashboard(username):
    st.subheader(f"שלום, {username} 👨‍💼")

    page = st.sidebar.radio("ניווט", ["פרויקטים פעילים","ניהול מסמכים","תשלומים", "דוחות", "ניהול מלאי", "פניות"])

    if page == "תשלומים":
        st.subheader("💰 מצב תשלומים בפרויקטים")
        for project in st.session_state.projects_data["פרויקט"]:
            if st.button(f"שלח דרישת תשלום ל-{project}"):
                st.session_state.payment_requests[project] = True
                st.success(f"💳 דרישת תשלום נשלחה ל-{project}!")
    elif page == "פרויקטים פעילים":
        st.subheader("📋 רשימת פרויקטים פעילים")
        for i, row in st.session_state.projects_data.iterrows():
            st.write(f"📌 {row['פרויקט']} - סטטוס: {row['סטטוס']}")
            st.progress((i + 1) * 0.3)

    elif page == "ניהול מסמכים":
        st.subheader("📄 מסמכים בפרויקטים")
        for project, docs in st.session_state.document_status.items():
            completed_docs = sum(docs.values())
            total_docs = len(docs)
            st.write(f"📌 {project}: {completed_docs} מסמכים הועלו מתוך {total_docs}")          

    elif page == "דוחות":
        st.subheader("📊 דוחות אסטרטגיים")
        fig1 = px.bar(st.session_state.projects_data, x="פרויקט", y="זמן ביצוע (שבועות)", title="⏳ משך זמן פרויקטים")
        fig2 = px.bar(st.session_state.projects_data, x="פרויקט", y="שביעות רצון", title="💬 שביעות רצון לקוחות")
        fig3 = px.bar(st.session_state.projects_data, x="פרויקט", y="תשלומים", title="💰 אגרות ששולמו מתוך 3")
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
    elif page == "פניות":
      st.subheader("📨 פניות לקוחות")
      for req in st.session_state.requests_data:
        if req["סטטוס"] == "פתוח":
            st.write(f"👤 {req['לקוח']} - {req['תוכן']}")
            if st.button(f"מענה לפנייה - {req['לקוח']}"):
                req["סטטוס"] = "סגור"
                st.success("✅ הפנייה טופלה!")
    if page == "ניהול מלאי":
        st.subheader("📦 ניהול מלאי לפי מודל EOQ")
        inventory_data = st.session_state.inventory_data
        inventory_data.setdefault("דרישה שנתית", 10)
        inventory_data.setdefault("עלות הזמנה", 300000)
        inventory_data.setdefault("עלות אחסון", 50000)

        demand = inventory_data["דרישה שנתית"]
        order_cost = inventory_data["עלות הזמנה"]
        holding_cost = inventory_data["עלות אחסון"]

        eoq = ((2 * demand * order_cost) / holding_cost) ** 0.5
        order_quantity = st.slider("בחר מספר מכולות להזמנה", min_value=1, max_value=10, value=int(eoq))
        total_cost = (demand / order_quantity) * order_cost + (order_quantity / 2) * holding_cost

        st.write(f"📦 כמות הזמנה אופטימלית לפי EOQ: **{int(eoq)}** מכולות")
        st.write(f"💰 עלות כוללת שנתית משוערת: **{total_cost:,.0f}** ₪")
        if st.button("חשב הזמנה אופטימלית"):
            st.success(f"✅ מומלץ להזמין {int(eoq)} מכולות לכל הזמנה!")           
                
 
      

if __name__ == "__main__":
    main()
