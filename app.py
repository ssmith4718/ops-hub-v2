import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# 1. App Configuration
st.set_page_config(page_title="My Hub", layout="wide", initial_sidebar_state="expanded")

# 2. Database Connection
conn = st.connection("gsheets", type=GSheetsConnection)
KPI_URL = "https://docs.google.com/spreadsheets/d/1KpN1zyLK4164aTuxu4O-4UOhY4fJoGy9G0g2iXz2HWI/edit?usp=drive_web"
LEADS_URL = "https://docs.google.com/spreadsheets/d/1KwDaiO_kurvvvqlTqEWVPDQt0OoIdud1dX5KvpOwxcw/edit?usp=drive_web"
TASKS_URL = "https://docs.google.com/spreadsheets/d/1UDsAIsNsXkuBNbwPllQcR-WVCyypz8QTDjl3c0F03gk/edit?usp=drive_web"

# Read Data safely
try:
    df_kpi = conn.read(spreadsheet=KPI_URL)
    df_leads = conn.read(spreadsheet=LEADS_URL)
    df_tasks = conn.read(spreadsheet=TASKS_URL)
except Exception:
    st.error("⚠️ Connection Error. Check Google Sheets permissions.")
    st.stop()

# 3. Sidebar Navigation (Acts as the App Menu)
st.sidebar.title("📱 Main Menu")
page = st.sidebar.radio("Navigate:", ["🏠 Home Dashboard", "🎯 Goals & KPIs", "🤝 Lead Pipeline", "✅ Task Tracker"])

# --- PAGE 1: HOME DASHBOARD ---
if page == "🏠 Home Dashboard":
    st.title("Welcome to the Hub")
    st.markdown("Your daily snapshot for operations, business development, and targets.")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **Active KPIs**")
        st.metric("Metrics Tracked", len(df_kpi) if not df_kpi.empty else 0)
    with col2:
        st.success("🤝 **Pipeline Volume**")
        st.metric("Total Leads", len(df_leads) if not df_leads.empty else 0)
    with col3:
        st.warning("✅ **Pending Tasks**")
        pending = len(df_tasks[df_tasks['Status'] != 'Completed']) if not df_tasks.empty else 0
        st.metric("To-Do Items", pending)

    st.markdown("### Quick Actions")
    st.markdown("Use the sidebar menu to navigate to your specific trackers to update numbers, manage the pipeline, or check off your daily fast-paced task list.")

# --- PAGE 2: GOALS & KPIs ---
elif page == "🎯 Goals & KPIs":
    st.title("Goals & KPIs")
    
    # Visual Metrics
    if not df_kpi.empty:
        st.subheader("Current Numbers")
        st.dataframe(df_kpi, use_container_width=True, hide_index=True)
    
    # App-style editor
    with st.expander("⚙️ Update Dashboard Numbers"):
        st.write("Double-click any cell to adjust your stats:")
        edited_kpi = st.data_editor(df_kpi, use_container_width=True, num_rows="dynamic", hide_index=True)
        if st.button("💾 Save to Cloud", key="save_kpi", type="primary"):
            conn.update(spreadsheet=KPI_URL, data=edited_kpi)
            st.success("Stats successfully synced!")

# --- PAGE 3: LEAD PIPELINE ---
elif page == "🤝 Lead Pipeline":
    st.title("Business Development Pipeline")
    
    # App-style Entry Form
    with st.expander("➕ Add a New Lead", expanded=False):
        with st.form("new_lead_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Lead Name")
                new_company = st.text_input("Company / Brand")
                new_email = st.text_input("Contact Info (Email/Phone)")
            with col2:
                new_source = st.selectbox("Lead Source", ["Networking", "Cold Outreach", "Referral", "Studio Promo", "Other"])
                new_status = st.selectbox("Current Status", ["New", "Contacted", "Meeting Booked", "In Talks", "Closed/Won", "Closed/Lost"])
                new_followup = st.date_input("Next Follow-Up Date", date.today())
            
            notes = st.text_area("Notes")
            submit_lead = st.form_submit_button("Add to Pipeline", type="primary")
            
            if submit_lead and new_name:
                new_row = pd.DataFrame([{
                    "Date_Added": date.today().strftime("%Y-%m-%d"), "Lead_Name": new_name, 
                    "Company": new_company, "Contact_Info": new_email, "Lead_Source": new_source,
                    "Status": new_status, "Next_Follow_Up": new_followup.strftime("%Y-%m-%d"), "Notes": notes
                }])
                updated_leads = pd.concat([df_leads, new_row], ignore_index=True)
                conn.update(spreadsheet=LEADS_URL, data=updated_leads)
                st.success(f"{new_name} added to the pipeline! Refresh the page to see changes.")

    st.subheader("Active Database")
    # Quick Status Filter
    filter_status = st.selectbox("Filter by Status:", ["All"] + list(df_leads['Status'].unique()))
    display_leads = df_leads if filter_status == "All
