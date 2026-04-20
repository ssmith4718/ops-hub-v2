import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Clean App Configuration
st.set_page_config(page_title="Ops Hub", layout="wide", initial_sidebar_state="expanded")

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
except Exception as e:
    st.error("⚠️ Ensure your Google Sheets are set to 'Anyone with the link' and 'Editor'.")
    st.stop()

# 3. Sidebar Navigation for a Clean Layout
st.sidebar.title("🧭 Command Center")
page = st.sidebar.radio("Navigate to:", ["📊 KPI Dashboard", "🤝 Lead Pipeline", "✅ Task Management"])

st.sidebar.divider()
st.sidebar.info("💡 **How to use:** Double-click any cell to edit your numbers or check off tasks. Always click the blue 'Save' button to push your updates to the cloud.")

# 4. Interactive Pages
if page == "📊 KPI Dashboard":
    st.title("Daily & Weekly Targets")
    st.write("Track operational metrics and overall progression.")
    
    # Interactive Data Editor
    edited_kpi = st.data_editor(df_kpi, use_container_width=True, num_rows="dynamic", hide_index=True)
    
    if st.button("💾 Save KPI Updates", type="primary"):
        conn.update(spreadsheet=KPI_URL, data=edited_kpi)
        st.success("KPIs successfully locked in!")

elif page == "🤝 Lead Pipeline":
    st.title("Business Development Pipeline")
    st.write("Manage active prospects, partnerships, and current lead statuses.")
    
    # Clean filter layout
    col1, col2 = st.columns([1, 3])
    with col1:
        status_filter = st.selectbox("Filter Pipeline:", ["All", "New", "Contacted", "Meeting Booked", "Closed"])
    
    display_leads = df_leads if status_filter == "All" else df_leads[df_leads['Status'] == status_filter]
    
    # Interactive Data Editor
    edited_leads = st.data_editor(display_leads, use_container_width=True, num_rows="dynamic", hide_index=True)
    
    if st.button("💾 Save Pipeline Updates", type="primary"):
        conn.update(spreadsheet=LEADS_URL, data=edited_leads)
        st.success("Pipeline successfully updated!")

elif page == "✅ Task Management":
    st.title("Action Items & Tasks")
    st.write("Check off completed duties and outline upcoming priorities.")
    
    # Interactive Data Editor
    edited_tasks = st.data_editor(df_tasks, use_container_width=True, num_rows="dynamic", hide_index=True)
    
    if st.button("💾 Save Task Updates", type="primary"):
        conn.update(spreadsheet=TASKS_URL, data=edited_tasks)
        st.success("Tasks successfully updated!")
