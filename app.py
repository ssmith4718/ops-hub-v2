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

# Read Data safely and pull fresh data every time (ttl=0)
try:
    df_kpi = conn.read(spreadsheet=KPI_URL, ttl=0)
    df_leads = conn.read(spreadsheet=LEADS_URL, ttl=0)
    df_tasks = conn.read(spreadsheet=TASKS_URL, ttl=0)
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
    st.title("Targets & KPIs")
    
    # 1. App-Style Quick Update Form
    st.subheader("⚡ Quick Update Metric")
    st.markdown("Select an existing metric below to quickly update your progress.")
    
    if not df_kpi.empty:
        metric_names = df_kpi['Metric_Name'].tolist()
        selected_metric = st.selectbox("Select Metric:", metric_names)
        
        # Pull current values for the selected metric
        current_row = df_kpi[df_kpi['Metric_Name'] == selected_metric].iloc[0]
        
        # Display large, tap-friendly number inputs
        col1, col2 = st.columns(2)
        with col1:
            new_val = st.number_input("Current Value", value=float(current_row['Value']), step=1.0)
        with col2:
            new_goal = st.number_input("Target / Goal", value=float(current_row['Goal_Target']), step=1.0)
            
        # Massive, thumb-friendly save button
        if st.button("💾 Update Metric", type="primary", use_container_width=True):
            df_kpi.loc[df_kpi['Metric_Name'] == selected_metric, 'Value'] = new_val
            df_kpi.loc[df_kpi['Metric_Name'] == selected_metric, 'Goal_Target'] = new_goal
            conn.update(spreadsheet=KPI_URL, data=df_kpi)
            st.success(f"**{selected_metric}** successfully updated! (Refresh page to see updated list below)")

    st.divider()

    # 2. Form to Add a Brand New Goal
    with st.expander("➕ Create a New Goal or KPI", expanded=False):
        with st.form("new_kpi_form", clear_on_submit=True):
            new_kpi_name = st.text_input("Metric Name (e.g., Cold Calls, Intro Sessions)")
            new_kpi_cat = st.selectbox("Category", ["Business Development", "Studio Operations", "Productivity"])
            
            colA, colB = st.columns(2)
            with colA:
                new_kpi_val = st.number_input("Starting Number", value=0.0)
            with colB:
                new_kpi_target = st.number_input("Target Goal", value=0.0)
                
            new
