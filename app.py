import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Mobile-Optimized Configuration
# "centered" layout looks much better on phone screens
st.set_page_config(page_title="Ops Hub", layout="centered", initial_sidebar_state="collapsed")

# 2. Database Connection
conn = st.connection("gsheets", type=GSheetsConnection)
KPI_URL = "https://docs.google.com/spreadsheets/d/1KpN1zyLK4164aTuxu4O-4UOhY4fJoGy9G0g2iXz2HWI/edit?usp=drive_web"
LEADS_URL = "https://docs.google.com/spreadsheets/d/1KwDaiO_kurvvvqlTqEWVPDQt0OoIdud1dX5KvpOwxcw/edit?usp=drive_web"
TASKS_URL = "https://docs.google.com/spreadsheets/d/1UDsAIsNsXkuBNbwPllQcR-WVCyypz8QTDjl3c0F03gk/edit?usp=drive_web"

# Read Data Safely
try:
    df_kpi = conn.read(spreadsheet=KPI_URL)
    df_leads = conn.read(spreadsheet=LEADS_URL)
    df_tasks = conn.read(spreadsheet=TASKS_URL)
except Exception:
    st.error("⚠️ Connection Error. Ensure Google Sheets are set to 'Anyone with the link' and 'Editor'.")
    st.stop()

# 3. Clean App Header
st.title("📱 My Hub")

# 4. Mobile Navigation Tabs (Acts like a native app menu)
tab1, tab2, tab3 = st.tabs(["📊 Stats", "🤝 Leads", "✅ Tasks"])

# --- TAB 1: KPI DASHBOARD ---
with tab1:
    st.subheader("Today's Snapshot")
    
    # Convert KPI data to visual app metric cards
    if not df_kpi.empty:
        col1, col2 = st.columns(2)
        # Display the first two KPIs as large app metrics
        kpi_list = df_kpi.to_dict('records')
        if len(kpi_list) > 0:
            col1.metric(label=kpi_list[0]['Metric_Name'], value=kpi_list[0]['Value'])
        if len(kpi_list) > 1:
            col2.metric(label=kpi_list[1]['Metric_Name'], value=kpi_list[1]['Value'])
    
    st.divider()
    
    # Hide the spreadsheet editor inside a drop-down to keep the app clean
    with st.expander("⚙️ Edit Database & Add Stats"):
        st.caption("Double-click cells to update. Click save when done.")
        edited_kpi = st.data_editor(df_kpi, use_container_width=True, num_rows="dynamic", hide_index=True)
        if st.button("💾 Save Stats", type="primary", use_container_width=True):
            conn.update(spreadsheet=KPI_URL, data=edited_kpi)
            st.success("Saved!")

# --- TAB 2: LEAD PIPELINE ---
with tab2:
    st.subheader("Active Pipeline")
    
    # Display leads as clean text cards instead of a grid
    if not df_leads.empty:
        for index, row in df_leads.iterrows():
            with st.container():
                st.markdown(f"**{row['Lead_Name']}** | {row['Company']}")
                st.caption(f"Status: {row['Status']} • Next Follow-up: {row['Next_Follow_Up']}")
                st.markdown("---")

    # Hide the spreadsheet editor inside a drop-down
    with st.expander("⚙️ Edit Leads Database"):
        edited_leads = st.data_editor(df_leads, use_container_width=True, num_rows="dynamic", hide_index=True)
        if st.button("💾 Save Leads", type="primary", use_container_width=True):
            conn.update(spreadsheet=LEADS_URL, data=edited_leads)
            st.success("Saved!")

# --- TAB 3: TASK MANAGEMENT ---
with tab3:
    st.subheader("To-Do List")
    
    # Display tasks as native app checkboxes
    if not df_tasks.empty:
        for index, row in df_tasks.iterrows():
            is_done = True if row['Status'] == 'Completed' else False
            st.checkbox(f"{row['Task_Description']} ({row['Category']})", value=is_done, key=f"task_{index}")
    
    st.divider()
    
    # Hide the spreadsheet editor inside a drop-down
    with st.expander("⚙️ Add & Edit Tasks"):
        edited_tasks = st.data_editor(df_tasks, use_container_width=True, num_rows="dynamic", hide_index=True)
        if st.button("💾 Save Tasks", type="primary", use_container_width=True):
            conn.update(spreadsheet=TASKS_URL, data=edited_tasks)
            st.success("Saved!")
