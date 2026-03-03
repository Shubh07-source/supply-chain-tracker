import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timezone, timedelta
from io import BytesIO
import base64

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supply Chain Tracking System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── IST TIMESTAMP ────────────────────────────────────────────────────────────
def now_ist():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
COMPANIES  = ["Robokart", "Bharat Tech", "EL"]
STATUSES   = ["Pending", "Procured", "Dispatched", "Delivered", "Invoiced", "Paid"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]

STATUS_EMOJI = {
    "Pending":"⏳", "Procured":"🔧", "Dispatched":"🚚",
    "Delivered":"📦", "Invoiced":"🧾", "Paid":"💰"
}
STATUS_COLOR = {
    "Pending":"🟡", "Procured":"🔵", "Dispatched":"🟣",
    "Delivered":"🟢", "Invoiced":"🔵", "Paid":"💚"
}

USERS = {
    "Admin":   {"password": "admin@123",    "role": "Admin",   "name": "System Admin"},
    "Manager": {"password": "mgr@123",      "role": "Manager", "name": "Ops Manager"},
    "Staff":   {"password": "Ops@Secure#1", "role": "Staff",   "name": "Operations Staff"},
    "Viewer":  {"password": "view123",      "role": "Viewer",  "name": "Finance Viewer"},
}

ROLE_MENUS = {
    "Admin":   ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports","Admin"],
    "Manager": ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports"],
    "Staff":   ["Dashboard","Update Order","Order Details","Activity Log"],
    "Viewer":  ["Dashboard","Order Details","Activity Log"],
}

# ─── DATA FILES ───────────────────────────────────────────────────────────────
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "orders":       f"{DATA_DIR}/orders.csv",
    "procurement":  f"{DATA_DIR}/procurement.csv",
    "dispatch":     f"{DATA_DIR}/dispatch.csv",
    "delivery":     f"{DATA_DIR}/delivery.csv",
    "invoices":     f"{DATA_DIR}/invoices.csv",
    "activity_log": f"{DATA_DIR}/activity_log.csv",
}

SEED = {
    "orders": pd.DataFrame([
        {"order_id":"ORD-2026-02-28-001","date_created":"2026-02-10 09:30:00","company":"Robokart","govt_department":"Education Department Delhi","contact_person":"Mr. Rajesh Kumar","contact_phone":"9876543210","po_number":"PO/EDU/2026/001","item_description":"Robotics Kits for STEM Labs","quantity":50,"total_value":250000,"assigned_company":"Tech Solutions Pvt Ltd","current_status":"Dispatched","priority":"High","expected_delivery_date":"2026-03-05","remarks":"","created_by":"Admin","last_updated":"2026-02-20 11:00:00"},
        {"order_id":"ORD-2026-02-28-002","date_created":"2026-02-12 10:15:00","company":"Bharat Tech","govt_department":"Health Ministry Maharashtra","contact_person":"Dr. Priya Sharma","contact_phone":"9123456789","po_number":"PO/HLT/2026/044","item_description":"Medical IoT Devices & Sensors","quantity":200,"total_value":980000,"assigned_company":"BioTech India","current_status":"Pending","priority":"Urgent","expected_delivery_date":"2026-03-10","remarks":"","created_by":"Admin","last_updated":"2026-02-12 10:15:00"},
        {"order_id":"ORD-2026-02-28-003","date_created":"2026-01-28 14:00:00","company":"EL","govt_department":"Defence Research DRDO","contact_person":"Col. Vikram Singh","contact_phone":"9000123456","po_number":"PO/DEF/2026/007","item_description":"Surveillance Drone Components","quantity":10,"total_value":1500000,"assigned_company":"AeroDyne Systems","current_status":"Paid","priority":"Medium","expected_delivery_date":"2026-02-20","remarks":"","created_by":"Admin","last_updated":"2026-02-25 16:30:00"},
        {"order_id":"ORD-2026-02-28-004","date_created":"2026-02-18 08:45:00","company":"Robokart","govt_department":"Smart Cities Mission UP","contact_person":"Ms. Anita Verma","contact_phone":"9988776655","po_number":"PO/SCM/2026/019","item_description":"IoT Traffic Management System","quantity":30,"total_value":670000,"assigned_company":"Robokart Solutions","current_status":"Delivered","priority":"Medium","expected_delivery_date":"2026-02-28","remarks":"","created_by":"Admin","last_updated":"2026-02-26 17:00:00"},
    ]),
    "procurement": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-001","procurement_status":"Completed","procurement_date":"2026-02-15","materials_source":"Vendor - RoboSupplies","quality_check_status":"Passed","notes":"All kits verified","updated_by":"Rahul","updated_at":"2026-02-15 14:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-003","procurement_status":"Completed","procurement_date":"2026-02-05","materials_source":"Import - AeroParts Ltd","quality_check_status":"Passed","notes":"Custom components sourced","updated_by":"Vikram","updated_at":"2026-02-05 10:00:00"},
        {"id":3,"order_id":"ORD-2026-02-28-004","procurement_status":"Completed","procurement_date":"2026-02-22","materials_source":"Robokart Warehouse","quality_check_status":"Passed","notes":"","updated_by":"Dev","updated_at":"2026-02-22 09:00:00"},
    ]),
    "dispatch": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-001","dispatch_date":"2026-02-18","courier_name":"BlueDart","vehicle_number":"DL01AB1234","driver_contact":"9111222333","tracking_number":"BD123456789","expected_delivery_date":"2026-03-05","updated_by":"Rahul","updated_at":"2026-02-18 08:30:00"},
        {"id":2,"order_id":"ORD-2026-02-28-003","dispatch_date":"2026-02-10","courier_name":"DTDC","vehicle_number":"MH04XY5678","driver_contact":"9444555666","tracking_number":"DTDC987654321","expected_delivery_date":"2026-02-20","updated_by":"Ops","updated_at":"2026-02-10 10:30:00"},
        {"id":3,"order_id":"ORD-2026-02-28-004","dispatch_date":"2026-02-24","courier_name":"In-House","vehicle_number":"UP32CD9012","driver_contact":"9777888999","tracking_number":"IH-004-UP","expected_delivery_date":"2026-02-28","updated_by":"Dev","updated_at":"2026-02-24 09:00:00"},
    ]),
    "delivery": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-003","delivery_status":"Delivered","delivery_date":"2026-02-19","receiver_name":"Col. Vikram Singh","delivered_quantity":10,"challan_number":"CH-DEF-001","updated_by":"Ops","updated_at":"2026-02-19 16:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-004","delivery_status":"Delivered","delivery_date":"2026-02-26","receiver_name":"Ms. Anita Verma","delivered_quantity":30,"challan_number":"CH-SCM-004","updated_by":"Dev","updated_at":"2026-02-26 14:30:00"},
    ]),
    "invoices": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-003","invoice_number":"INV-2026-0321","invoice_date":"2026-02-20","invoice_amount":1500000,"payment_status":"Completed","payment_date":"2026-02-24","payment_mode":"NEFT","transaction_reference":"TXN20260224DEF","updated_by":"Finance","updated_at":"2026-02-24 16:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-004","invoice_number":"INV-2026-0389","invoice_date":"2026-02-27","invoice_amount":670000,"payment_status":"Approved","payment_date":"","payment_mode":"","transaction_reference":"","updated_by":"Finance","updated_at":"2026-02-27 11:00:00"},
    ]),
    "activity_log": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-001","action_type":"ORDER_CREATED","previous_status":"—","new_status":"Pending","performed_by":"Admin","performed_at":"2026-02-10 09:30:00","details":"Order created"},
        {"id":2,"order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Pending","new_status":"Procured","performed_by":"Rahul","performed_at":"2026-02-15 14:00:00","details":"Procurement completed"},
        {"id":3,"order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Procured","new_status":"Dispatched","performed_by":"Rahul","performed_at":"2026-02-18 08:30:00","details":"Dispatched via BlueDart"},
        {"id":4,"order_id":"ORD-2026-02-28-003","action_type":"PAYMENT","previous_status":"Invoiced","new_status":"Paid","performed_by":"Finance","performed_at":"2026-02-24 16:00:00","details":"NEFT payment received"},
        {"id":5,"order_id":"ORD-2026-02-28-004","action_type":"STATUS_CHANGE","previous_status":"Dispatched","new_status":"Delivered","performed_by":"Dev","performed_at":"2026-02-26 14:30:00","details":"Delivered, challan signed"},
    ]),
}

# ─── LOAD / SAVE DATA ─────────────────────────────────────────────────────────
def load_data():
    data = {}
    for key, path in FILES.items():
        if os.path.exists(path):
            data[key] = pd.read_csv(path, dtype=str).fillna("")
        else:
            df = SEED[key].copy().astype(str).fillna("")
            df.to_csv(path, index=False)
            data[key] = df
    return data

def save_table(key, df):
    df.to_csv(FILES[key], index=False)

def add_log(data, order_id, action, prev, new, by, details):
    ts = now_ist()
    new_id = str(len(data["activity_log"]) + 1)
    row = pd.DataFrame([{
        "id": new_id, "order_id": order_id, "action_type": action,
        "previous_status": prev, "new_status": new,
        "performed_by": by, "performed_at": ts, "details": details
    }])
    data["activity_log"] = pd.concat([data["activity_log"], row], ignore_index=True)
    save_table("activity_log", data["activity_log"])

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif !important;
        background: #f0f4f8 !important;
        color: #0f172a !important;
    }
    #MainMenu {visibility:hidden;}
    footer     {visibility:hidden;}
    header     {visibility:hidden;}
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0c1426 !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * {
        color: #94a3b8 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
    }
    [data-testid="stSidebar"] h1 { color: #f97316 !important; font-size: 1.2rem !important; font-weight: 800 !important; }
    [data-testid="stSidebar"] h2 { color: #475569 !important; font-size: 0.65rem !important; letter-spacing: 1px !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] hr { border-color: #1e293b !important; }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        border-left: 3px solid transparent !important;
        border-radius: 0 !important;
        color: #94a3b8 !important;
        font-weight: 400 !important;
        text-align: left !important;
        padding: 10px 16px !important;
        width: 100% !important;
        transition: all 0.12s !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.05) !important;
        color: #fff !important;
        border-left-color: #60a5fa !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #1d4ed8 !important;
        color: #fff !important;
        font-weight: 700 !important;
        border-left: 3px solid #60a5fa !important;
        border-radius: 6px !important;
    }

    /* ── Main area ── */
    .main .block-container {
        background: #f0f4f8 !important;
    }

    /* ── Metric cards ── */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07) !important;
    }
    [data-testid="metric-container"] label {
        font-size: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        color: #64748b !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
    }

    /* ── Cards / containers ── */
    .sc-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }
    .sc-card-title {
        font-size: 14px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 14px;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 7px !important;
        font-weight: 600 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        transition: all 0.15s !important;
    }
    .stButton > button[kind="primary"] {
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        color: #fff !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #1e40af !important;
    }
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #374151 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #1d4ed8 !important;
        color: #1d4ed8 !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        border-radius: 7px !important;
        border: 1px solid #d1d5db !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 13px !important;
        background: #ffffff !important;
        color: #0f172a !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #1d4ed8 !important;
        box-shadow: 0 0 0 2px rgba(29,78,216,0.12) !important;
    }

    /* ── Labels ── */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stDateInput label, .stFileUploader label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #374151 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 2px solid #e2e8f0 !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        color: #64748b !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        padding: 8px 18px !important;
        margin-bottom: -2px !important;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #1d4ed8 !important;
        color: #1d4ed8 !important;
        font-weight: 700 !important;
        background: transparent !important;
    }

    /* ── DataFrames ── */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    }
    .stDataFrame table { font-family: 'IBM Plex Sans', sans-serif !important; }
    .stDataFrame thead th {
        background: #f8fafc !important;
        font-size: 10.5px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #475569 !important;
        border-bottom: 2px solid #e2e8f0 !important;
        padding: 9px 12px !important;
    }
    .stDataFrame tbody td {
        font-size: 12.5px !important;
        padding: 10px 12px !important;
        border-bottom: 1px solid #f1f5f9 !important;
        color: #1e293b !important;
    }

    /* ── Forms ── */
    .stForm {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 18px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    }

    /* ── Alerts ── */
    .stSuccess { border-radius: 8px !important; }
    .stError   { border-radius: 8px !important; }
    .stInfo    { border-radius: 8px !important; }
    .stWarning { border-radius: 8px !important; }

    /* ── Progress bar ── */
    .stProgress > div > div {
        background: #1d4ed8 !important;
        border-radius: 3px !important;
    }
    .stProgress > div {
        background: #f1f5f9 !important;
        border-radius: 3px !important;
        height: 6px !important;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
    }
    .badge-pending    { background:#fef3c7; color:#d97706; }
    .badge-procured   { background:#dbeafe; color:#2563eb; }
    .badge-dispatched { background:#ede9fe; color:#7c3aed; }
    .badge-delivered  { background:#d1fae5; color:#059669; }
    .badge-invoiced   { background:#cffafe; color:#0891b2; }
    .badge-paid       { background:#dcfce7; color:#16a34a; }
    .badge-high       { background:#fef3c7; color:#d97706; }
    .badge-urgent     { background:#fee2e2; color:#dc2626; }
    .badge-medium     { background:#dbeafe; color:#2563eb; }
    .badge-low        { background:#f1f5f9; color:#64748b; }
    .badge-rk         { background:#ede9fe; color:#7c3aed; }
    .badge-bt         { background:#cffafe; color:#0891b2; }
    .badge-el         { background:#ffedd5; color:#c2410c; }

    /* ── Page title ── */
    .page-title {
        font-size: 22px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .page-sub {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 18px;
    }

    /* ── Topbar ── */
    .topbar {
        background: #ffffff;
        border-bottom: 1px solid #e2e8f0;
        padding: 10px 0 14px 0;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .saved-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #22c55e;
        margin-right: 4px;
        vertical-align: middle;
    }
    .saved-label { font-size: 11px; color: #16a34a; font-weight: 600; }

    /* ── Login ── */
    .login-box {
        background: #ffffff;
        border-radius: 14px;
        padding: 40px 44px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.12);
        border: 1px solid #e2e8f0;
        margin-top: 60px;
    }

    /* ── Step progress ── */
    .step-done {
        background: #1d4ed8;
        color: #fff;
        border-radius: 8px;
        text-align: center;
        padding: 8px 4px;
        font-size: 10px;
        font-weight: 700;
    }
    .step-pending {
        background: #f1f5f9;
        color: #94a3b8;
        border-radius: 8px;
        text-align: center;
        padding: 8px 4px;
        font-size: 10px;
        font-weight: 600;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        font-size: 11px;
        color: #94a3b8;
        padding: 10px 0 4px 0;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }

    /* ── Divider ── */
    hr { border-color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "logged_in"  not in st.session_state: st.session_state.logged_in  = False
if "username"   not in st.session_state: st.session_state.username   = ""
if "role"       not in st.session_state: st.session_state.role       = ""
if "user_name"  not in st.session_state: st.session_state.user_name  = ""
if "data"       not in st.session_state: st.session_state.data       = load_data()

data = st.session_state.data

# ─── LOGIN PAGE ───────────────────────────────────────────────────────────────
def login_page():
    # full-page gradient background
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg,#0c1426 0%,#1e3a5f 100%) !important; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#fff;border-radius:14px;padding:40px 36px 32px 36px;
                    box-shadow:0 24px 80px rgba(0,0,0,0.4);border:1px solid #e2e8f0;">
            <div style="text-align:center;margin-bottom:28px;">
                <div style="font-size:40px;margin-bottom:8px;">🏭</div>
                <div style="font-size:22px;font-weight:800;color:#0f172a;">
                    Supply Chain Tracking System
                </div>
                <div style="font-size:12px;color:#64748b;margin-top:6px;">
                    Sign in to continue
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username  = st.text_input("Username", placeholder="Enter your username")
            password  = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")
            if submitted:
                if username in USERS and USERS[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username  = username
                    st.session_state.role      = USERS[username]["role"]
                    st.session_state.user_name = USERS[username]["name"]
                    st.rerun()
                else:
                    st.error("⚠ Invalid username or password.")
        st.markdown(
            "<p style='text-align:center;font-size:11px;color:#94a3b8;margin-top:8px;'>"
            "Contact your administrator for login credentials.</p>",
            unsafe_allow_html=True
        )

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("# 🏭 Supply Chain")
        st.markdown("**TRACKING SYSTEM**")
        st.markdown("---")

        menus = ROLE_MENUS[st.session_state.role]
        menu_icons = {
            "Dashboard":"📊", "New Order":"➕", "Update Order":"🔄",
            "Order Details":"🔍", "Activity Log":"📋", "Reports":"📈", "Admin":"⚙️"
        }

        if "menu" not in st.session_state:
            st.session_state.menu = menus[0]

        for m in menus:
            active = st.session_state.menu == m
            if st.button(
                f"{menu_icons.get(m,'')} {m}",
                key=f"nav_{m}",
                use_container_width=True,
                type="primary" if active else "secondary"
            ):
                st.session_state.menu = m
                st.rerun()

        st.markdown("---")
        st.markdown(f"**{st.session_state.user_name}**")
        role_colors = {"Admin":"🔴","Manager":"🟡","Staff":"🔵","Viewer":"🟢"}
        st.markdown(f"{role_colors.get(st.session_state.role,'')} {st.session_state.role}")
        if st.button("← Sign Out", use_container_width=True):
            for k in ["logged_in","username","role","user_name","menu"]:
                st.session_state.pop(k, None)
            st.rerun()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def status_badge(status):
    colors = {
        "Pending":"#fef3c7;color:#d97706",    "Procured":"#dbeafe;color:#2563eb",
        "Dispatched":"#ede9fe;color:#7c3aed", "Delivered":"#d1fae5;color:#059669",
        "Invoiced":"#cffafe;color:#0891b2",   "Paid":"#dcfce7;color:#16a34a",
    }
    s = colors.get(status, "#f1f5f9;color:#64748b")
    bg, col = s.split(";color:")
    return f'<span class="badge" style="background:{bg};color:{col}">{STATUS_EMOJI.get(status,"")} {status}</span>'

def company_badge(company):
    colors = {
        "Robokart":"background:#ede9fe;color:#7c3aed",
        "Bharat Tech":"background:#cffafe;color:#0891b2",
        "EL":"background:#ffedd5;color:#c2410c",
    }
    s = colors.get(company, "background:#f1f5f9;color:#64748b")
    return f'<span class="badge" style="{s}">{company}</span>'

def priority_badge(priority):
    colors = {
        "Low":"background:#f1f5f9;color:#64748b",    "Medium":"background:#dbeafe;color:#2563eb",
        "High":"background:#fef3c7;color:#d97706",   "Urgent":"background:#fee2e2;color:#dc2626",
    }
    s = colors.get(priority, "background:#f1f5f9;color:#64748b")
    return f'<span class="badge" style="{s}">{priority}</span>'

def get_order(order_id):
    rows = data["orders"][data["orders"]["order_id"] == order_id]
    return rows.iloc[0] if len(rows) > 0 else None

def page_title(icon, title, subtitle=""):
    st.markdown(f"""
    <div style="padding:0 0 14px 0;border-bottom:1px solid #e2e8f0;margin-bottom:20px;">
        <div style="font-size:20px;font-weight:800;color:#0f172a;">{icon} {title}</div>
        {"<div style='font-size:12px;color:#64748b;margin-top:3px;'>"+subtitle+"</div>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

# ─── PAGES ────────────────────────────────────────────────────────────────────

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
def page_dashboard():
    orders = data["orders"].copy()
    cf     = st.session_state.get("cf", "All")

    # ── Topbar ──
    today = datetime.now().strftime("%d %b %Y")
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                padding:0 0 14px 0;border-bottom:1px solid #e2e8f0;margin-bottom:18px;">
        <div style="font-size:20px;font-weight:800;color:#0f172a;">📊 Dashboard</div>
        <div style="display:flex;align-items:center;gap:14px;">
            <span style="display:inline-flex;align-items:center;gap:5px;font-size:11px;color:#16a34a;font-weight:600;">
                <span style="width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block;"></span>
                Auto-saved
            </span>
            <span style="font-size:11px;color:#64748b;">{today}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric cards ──
    filtered  = orders if cf == "All" else orders[orders["company"] == cf]
    total_val = filtered["total_value"].astype(float).sum() if len(filtered) else 0

    metrics = [
        ("TOTAL ORDERS",  str(len(filtered)),                                                          "#1d4ed8"),
        ("PENDING",       str(len(filtered[filtered["current_status"]=="Pending"])),                   "#d97706"),
        ("IN TRANSIT",    str(len(filtered[filtered["current_status"].isin(["Procured","Dispatched"])])), "#7c3aed"),
        ("DELIVERED",     str(len(filtered[filtered["current_status"].isin(["Delivered","Invoiced","Paid"])])), "#059669"),
        ("PAID",          str(len(filtered[filtered["current_status"]=="Paid"])),                      "#16a34a"),
        ("TOTAL VALUE",   f"₹{total_val/100000:.1f}L",                                                "#f97316"),
    ]
    cols = st.columns(6)
    for col, (label, value, color) in zip(cols, metrics):
        col.markdown(f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-top:3px solid {color};
                    border-radius:10px;padding:14px 16px;box-shadow:0 1px 4px rgba(0,0,0,0.07);">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.6px;color:#64748b;">{label}</div>
            <div style="font-size:24px;font-weight:800;margin-top:6px;color:{color};">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Company filter pills ──
    cf_buttons = st.columns([1,1,1,1,4])
    labels = [("🏢 All Companies","All"), ("Robokart","Robokart"), ("Bharat Tech","Bharat Tech"), ("EL","EL")]
    pill_colors = {
        "All":         ("background:#dbeafe;color:#1d4ed8;border:1.5px solid #1d4ed8;",
                        "background:#fff;color:#374151;border:1px solid #e2e8f0;"),
        "Robokart":    ("background:#ede9fe;color:#7c3aed;border:1.5px solid #7c3aed;",
                        "background:#fff;color:#374151;border:1px solid #e2e8f0;"),
        "Bharat Tech": ("background:#cffafe;color:#0891b2;border:1.5px solid #0891b2;",
                        "background:#fff;color:#374151;border:1px solid #e2e8f0;"),
        "EL":          ("background:#ffedd5;color:#c2410c;border:1.5px solid #c2410c;",
                        "background:#fff;color:#374151;border:1px solid #e2e8f0;"),
    }
    for col, (label, val) in zip(cf_buttons, labels):
        active_style, inactive_style = pill_colors[val]
        style = active_style if cf == val else inactive_style
        with col:
            if st.button(
                f"{label} {'✓' if cf==val else ''}",
                key=f"cf_{val}",
                use_container_width=True,
                type="primary" if cf == val else "secondary"
            ):
                st.session_state.cf = val
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Orders table ──
    count = len(filtered)
    title = "All Orders" if cf == "All" else f"{cf} Orders"

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;
                box-shadow:0 1px 3px rgba(0,0,0,0.06);overflow:hidden;">
        <div style="padding:12px 18px;border-bottom:1px solid #f1f5f9;
                    display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:14px;font-weight:700;color:#0f172a;">📦 {title}</span>
            <span style="font-size:11px;color:#64748b;background:#f1f5f9;
                         padding:3px 12px;border-radius:99px;font-weight:600;">{count} orders</span>
        </div>
    """, unsafe_allow_html=True)

    if count == 0:
        st.markdown("<div style='padding:20px;text-align:center;color:#94a3b8;'>No orders found.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Build HTML table
    STATUS_BG  = {"Pending":"#fef3c7","Procured":"#dbeafe","Dispatched":"#ede9fe",
                  "Delivered":"#d1fae5","Invoiced":"#cffafe","Paid":"#dcfce7"}
    STATUS_COL = {"Pending":"#d97706","Procured":"#2563eb","Dispatched":"#7c3aed",
                  "Delivered":"#059669","Invoiced":"#0891b2","Paid":"#16a34a"}
    PRIO_BG    = {"Low":"#f1f5f9","Medium":"#dbeafe","High":"#fef3c7","Urgent":"#fee2e2"}
    PRIO_COL   = {"Low":"#64748b","Medium":"#2563eb","High":"#d97706","Urgent":"#dc2626"}
    CO_BG      = {"Robokart":"#ede9fe","Bharat Tech":"#cffafe","EL":"#ffedd5"}
    CO_COL     = {"Robokart":"#7c3aed","Bharat Tech":"#0891b2","EL":"#c2410c"}

    th = "padding:9px 14px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#475569;border-bottom:2px solid #e2e8f0;white-space:nowrap;"
    td = "padding:11px 14px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;vertical-align:middle;"

    rows_html = ""
    for i, (_, row) in enumerate(filtered.iterrows()):
        bg    = "#fff" if i % 2 == 0 else "#fafbfc"
        s     = row["current_status"]
        p     = row["priority"]
        co    = row["company"]
        val   = f"₹{float(row['total_value']):,.0f}"
        sbg   = STATUS_BG.get(s,"#f1f5f9");  scol = STATUS_COL.get(s,"#64748b")
        pbg   = PRIO_BG.get(p,"#f1f5f9");    pcol = PRIO_COL.get(p,"#64748b")
        cobg  = CO_BG.get(co,"#f1f5f9");     cocol= CO_COL.get(co,"#64748b")
        sbadge = f'<span style="background:{sbg};color:{scol};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;white-space:nowrap;">{STATUS_EMOJI.get(s,"")} {s}</span>'
        pbadge = f'<span style="background:{pbg};color:{pcol};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;">{p}</span>'
        cobadge= f'<span style="background:{cobg};color:{cocol};padding:3px 10px;border-radius:5px;font-size:11px;font-weight:700;">{co}</span>'
        rows_html += f"""
        <tr style="background:{bg};">
            <td style="{td}font-weight:700;color:#1d4ed8;font-size:11.5px;">{row["order_id"]}</td>
            <td style="{td}">{cobadge}</td>
            <td style="{td}color:#64748b;font-size:11.5px;">{row["po_number"]}</td>
            <td style="{td}">{row["govt_department"]}</td>
            <td style="{td}max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{row["item_description"]}</td>
            <td style="{td}text-align:center;">{row["quantity"]}</td>
            <td style="{td}font-weight:700;">{val}</td>
            <td style="{td}">{pbadge}</td>
            <td style="{td}">{sbadge}</td>
            <td style="{td}font-size:11px;color:#94a3b8;">{row["last_updated"]}</td>
        </tr>"""

    st.markdown(f"""
        <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
            <thead>
                <tr>
                    <th style="{th}">Order ID</th>
                    <th style="{th}">Company</th>
                    <th style="{th}">PO Number</th>
                    <th style="{th}">Department</th>
                    <th style="{th}">Description</th>
                    <th style="{th}">Qty</th>
                    <th style="{th}">Value</th>
                    <th style="{th}">Priority</th>
                    <th style="{th}">Status</th>
                    <th style="{th}">Last Updated</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

# ─── PAGES ────────────────────────────────────────────────────────────────────

# ── NEW ORDER ─────────────────────────────────────────────────────────────────
def page_new_order():
    page_title("➕", "Create New Purchase Order")

    with st.form("new_order_form", clear_on_submit=True):
        st.markdown("#### Select Company *")
        company = st.selectbox("Company", COMPANIES, label_visibility="collapsed")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            govt_dept    = st.text_input("Govt Department *",   placeholder="e.g., Education Department Delhi")
            contact_name = st.text_input("Contact Person *",    placeholder="e.g., Mr. Rajesh Kumar")
            contact_ph   = st.text_input("Contact Phone",       placeholder="e.g., 9876543210")
            po_number    = st.text_input("PO Number *",         placeholder="e.g., PO/EDU/2026/001")
        with col2:
            assigned_co  = st.text_input("Assigned Company",    placeholder="e.g., Tech Solutions Pvt Ltd")
            exp_delivery = st.date_input("Expected Delivery Date")
            quantity     = st.number_input("Quantity *",        min_value=1, value=1)
            total_value  = st.number_input("Total Value (₹) *", min_value=0, value=0)

        col3, col4 = st.columns(2)
        with col3:
            priority = st.selectbox("Priority", PRIORITIES, index=1)
        item_desc = st.text_area("Item Description *", placeholder="Detailed description of items to be procured...")
        remarks   = st.text_area("Remarks", placeholder="Any additional remarks...")

        submitted = st.form_submit_button("🚀 Create Order", use_container_width=True, type="primary")

        if submitted:
            if not all([company, govt_dept, contact_name, po_number, item_desc, quantity, total_value]):
                st.error("Please fill all required fields *")
            elif po_number in data["orders"]["po_number"].values:
                st.error("⚠ PO Number already exists!")
            else:
                ts       = now_ist()
                order_id = f"ORD-{ts[:10]}-{str(len(data['orders'])+1).zfill(3)}"
                new_row  = pd.DataFrame([{
                    "order_id": order_id, "date_created": ts, "company": company,
                    "govt_department": govt_dept, "contact_person": contact_name,
                    "contact_phone": contact_ph, "po_number": po_number,
                    "item_description": item_desc, "quantity": str(quantity),
                    "total_value": str(total_value), "assigned_company": assigned_co,
                    "current_status": "Pending", "priority": priority,
                    "expected_delivery_date": str(exp_delivery),
                    "remarks": remarks, "created_by": st.session_state.user_name, "last_updated": ts
                }])
                data["orders"] = pd.concat([data["orders"], new_row], ignore_index=True)
                save_table("orders", data["orders"])
                add_log(data, order_id, "ORDER_CREATED", "—", "Pending",
                        st.session_state.user_name, f"Created by {st.session_state.user_name} [{company}]")
                st.success(f"✅ Order {order_id} created successfully!")
                st.rerun()

# ── UPDATE ORDER ──────────────────────────────────────────────────────────────
def page_update_order():
    page_title("🔄","Update Order","Select an order and update its procurement, dispatch, delivery or invoice status")

    order_options = ["— Select an order —"] + [
        f"{row['order_id']} · {row['po_number']} · [{row['current_status']}]"
        for _, row in data["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order *", order_options)

    if sel == "— Select an order —":
        return

    order_id  = sel.split(" · ")[0]
    order     = get_order(order_id)
    if order is None:
        st.error("Order not found."); return

    # Live status display
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"**Company:** {order['company']}")
    col2.markdown(f"**Status:** {STATUS_EMOJI.get(order['current_status'],'')} {order['current_status']}")
    col3.markdown(f"**Value:** ₹{float(order['total_value']):,.0f}")
    col4.markdown(f"**Dept:** {order['govt_department']}")

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 Procurement", "🚚 Dispatch", "📦 Delivery", "💰 Invoice"])

    updated_by = st.text_input("Your Name / Department *", placeholder="e.g., Rahul - Logistics")

    # PROCUREMENT
    with tab1:
        with st.form("proc_form"):
            col1, col2 = st.columns(2)
            with col1:
                proc_status = st.selectbox("Procurement Status *", ["","Not_Started","In_Progress","Completed","On_Hold"])
                proc_date   = st.date_input("Procurement Date")
                source      = st.text_input("Materials Source", placeholder="Vendor / Warehouse")
            with col2:
                qc_status   = st.selectbox("QC Status", ["","Pending","In_Progress","Passed","Failed"])
                notes       = st.text_area("Notes", height=100)
            save = st.form_submit_button("✅ Save Procurement", use_container_width=True, type="primary")
            if save:
                if not updated_by:
                    st.error("Please enter your name above."); return
                ts = now_ist()
                new_row = pd.DataFrame([{
                    "id": str(len(data["procurement"])+1), "order_id": order_id,
                    "procurement_status": proc_status, "procurement_date": str(proc_date),
                    "materials_source": source, "quality_check_status": qc_status,
                    "notes": notes, "updated_by": updated_by, "updated_at": ts
                }])
                data["procurement"] = pd.concat([data["procurement"], new_row], ignore_index=True)
                save_table("procurement", data["procurement"])
                next_status = "Procured" if proc_status == "Completed" else order["current_status"]
                data["orders"].loc[data["orders"]["order_id"]==order_id, "current_status"] = next_status
                data["orders"].loc[data["orders"]["order_id"]==order_id, "last_updated"]   = ts
                save_table("orders", data["orders"])
                add_log(data, order_id, "STATUS_CHANGE", order["current_status"], next_status,
                        updated_by, f"Procurement: {proc_status}")
                st.success(f"✅ Procurement saved! Status → {next_status}"); st.rerun()

    # DISPATCH
    with tab2:
        with st.form("disp_form"):
            col1, col2 = st.columns(2)
            with col1:
                disp_date   = st.date_input("Dispatch Date")
                courier     = st.text_input("Courier / Transporter *", placeholder="e.g., BlueDart")
                vehicle     = st.text_input("Vehicle Number",           placeholder="e.g., DL01AB1234")
            with col2:
                driver_cont = st.text_input("Driver Contact")
                tracking    = st.text_input("Tracking Number")
                exp_del     = st.date_input("Expected Delivery")
            save = st.form_submit_button("✅ Save Dispatch", use_container_width=True, type="primary")
            if save:
                if not updated_by:
                    st.error("Please enter your name above."); return
                ts = now_ist()
                new_row = pd.DataFrame([{
                    "id": str(len(data["dispatch"])+1), "order_id": order_id,
                    "dispatch_date": str(disp_date), "courier_name": courier,
                    "vehicle_number": vehicle, "driver_contact": driver_cont,
                    "tracking_number": tracking, "expected_delivery_date": str(exp_del),
                    "updated_by": updated_by, "updated_at": ts
                }])
                data["dispatch"] = pd.concat([data["dispatch"], new_row], ignore_index=True)
                save_table("dispatch", data["dispatch"])
                data["orders"].loc[data["orders"]["order_id"]==order_id, "current_status"] = "Dispatched"
                data["orders"].loc[data["orders"]["order_id"]==order_id, "last_updated"]   = ts
                save_table("orders", data["orders"])
                add_log(data, order_id, "STATUS_CHANGE", order["current_status"], "Dispatched",
                        updated_by, f"Dispatched via {courier}")
                st.success("✅ Dispatch saved! Status → Dispatched"); st.rerun()

    # DELIVERY
    with tab3:
        with st.form("del_form"):
            col1, col2 = st.columns(2)
            with col1:
                del_status  = st.selectbox("Delivery Status *", ["","Delivered","Partial","Failed","Rescheduled"])
                del_date    = st.date_input("Delivery Date")
                receiver    = st.text_input("Receiver Name")
            with col2:
                del_qty     = st.number_input("Delivered Quantity", min_value=0)
                challan_no  = st.text_input("Challan Number")

            st.markdown("**📸 Delivery Photos / Files**")
            delivery_files = st.file_uploader("Upload delivery photos, proof of delivery",
                                               accept_multiple_files=True, key="del_files",
                                               label_visibility="collapsed")
            st.markdown("**📋 Challan Documents**")
            challan_files  = st.file_uploader("Upload signed challan copies",
                                               accept_multiple_files=True, key="chal_files",
                                               label_visibility="collapsed")
            save = st.form_submit_button("✅ Save Delivery", use_container_width=True, type="primary")
            if save:
                if not updated_by:
                    st.error("Please enter your name above."); return
                ts = now_ist()
                new_row = pd.DataFrame([{
                    "id": str(len(data["delivery"])+1), "order_id": order_id,
                    "delivery_status": del_status, "delivery_date": str(del_date),
                    "receiver_name": receiver, "delivered_quantity": str(del_qty),
                    "challan_number": challan_no,
                    "delivery_files": str(len(delivery_files or [])) + " file(s)",
                    "challan_files":  str(len(challan_files  or [])) + " file(s)",
                    "updated_by": updated_by, "updated_at": ts
                }])
                data["delivery"] = pd.concat([data["delivery"], new_row], ignore_index=True)
                save_table("delivery", data["delivery"])
                next_status = "Delivered" if del_status == "Delivered" else order["current_status"]
                data["orders"].loc[data["orders"]["order_id"]==order_id, "current_status"] = next_status
                data["orders"].loc[data["orders"]["order_id"]==order_id, "last_updated"]   = ts
                save_table("orders", data["orders"])
                add_log(data, order_id, "STATUS_CHANGE", order["current_status"], next_status,
                        updated_by, f"Delivery: {del_status} · {len(delivery_files or [])} delivery + {len(challan_files or [])} challan files")
                st.success(f"✅ Delivery saved! Status → {next_status}"); st.rerun()

    # INVOICE
    with tab4:
        with st.form("inv_form"):
            col1, col2 = st.columns(2)
            with col1:
                inv_number  = st.text_input("Invoice Number")
                inv_date    = st.date_input("Invoice Date")
                inv_amount  = st.number_input("Invoice Amount (₹)", min_value=0)
                pay_status  = st.selectbox("Payment Status *", ["","Pending","Approved","Completed"])
            with col2:
                pay_mode    = st.selectbox("Payment Mode", ["","NEFT","RTGS","Cheque","DD","Online","Cash"])
                txn_ref     = st.text_input("Transaction Reference")
                pay_date    = st.date_input("Payment Date")
            st.markdown("**🧾 Invoice Files**")
            invoice_files = st.file_uploader("Upload invoice PDFs, scanned copies",
                                              accept_multiple_files=True, key="inv_files",
                                              label_visibility="collapsed")
            save = st.form_submit_button("✅ Save Invoice", use_container_width=True, type="primary")
            if save:
                if not updated_by:
                    st.error("Please enter your name above."); return
                ts = now_ist()
                new_row = pd.DataFrame([{
                    "id": str(len(data["invoices"])+1), "order_id": order_id,
                    "invoice_number": inv_number, "invoice_date": str(inv_date),
                    "invoice_amount": str(inv_amount), "payment_status": pay_status,
                    "payment_date": str(pay_date), "payment_mode": pay_mode,
                    "transaction_reference": txn_ref,
                    "invoice_files": str(len(invoice_files or [])) + " file(s)",
                    "updated_by": updated_by, "updated_at": ts
                }])
                data["invoices"] = pd.concat([data["invoices"], new_row], ignore_index=True)
                save_table("invoices", data["invoices"])
                next_status = "Paid" if pay_status == "Completed" else "Invoiced"
                data["orders"].loc[data["orders"]["order_id"]==order_id, "current_status"] = next_status
                data["orders"].loc[data["orders"]["order_id"]==order_id, "last_updated"]   = ts
                save_table("orders", data["orders"])
                add_log(data, order_id, "STATUS_CHANGE", order["current_status"], next_status,
                        updated_by, f"Invoice {inv_number} · payment: {pay_status} · {len(invoice_files or [])} files")
                st.success(f"✅ Invoice saved! Status → {next_status}"); st.rerun()

# ── ORDER DETAILS ─────────────────────────────────────────────────────────────
def page_order_details():
    page_title("🔍","Order Details","View full information and activity log for any order")

    order_options = ["— Select an order —"] + [
        f"{row['order_id']} · {row['po_number']} · {row['current_status']}"
        for _, row in data["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order", order_options)
    if sel == "— Select an order —": return

    order_id = sel.split(" · ")[0]
    order    = get_order(order_id)
    if order is None: st.error("Order not found."); return

    st.markdown("---")

    # Header
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.markdown(f"### {order['order_id']}")
        st.markdown(f"**{order['po_number']}** · {order['govt_department']}")
    with col2:
        st.markdown(f"**Company:** {order['company']}")
        st.markdown(f"**Priority:** {order['priority']}")
    with col3:
        st.markdown(f"**Status:** {STATUS_EMOJI.get(order['current_status'],'')} **{order['current_status']}**")
        st.markdown(f"**Value:** ₹{float(order['total_value']):,.0f}")

    # Progress stepper
    st.markdown("---")
    steps = STATUSES
    cur_idx = steps.index(order["current_status"]) if order["current_status"] in steps else 0
    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        done = i <= cur_idx
        with col:
            st.markdown(
                f"<div style='text-align:center;padding:6px;background:{'#1d4ed8' if done else '#f1f5f9'};border-radius:8px;'>"
                f"<div style='font-size:16px'>{STATUS_EMOJI.get(step,'')}</div>"
                f"<div style='font-size:10px;color:{'#fff' if done else '#94a3b8'};font-weight:600'>{step}</div>"
                f"</div>", unsafe_allow_html=True
            )

    # Details tabs
    st.markdown("---")
    t1, t2, t3, t4, t5 = st.tabs(["📋 Order Info","🔧 Procurement","🚚 Dispatch","📦 Delivery","💰 Invoice"])

    with t1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Contact:** {order['contact_person']}")
            st.markdown(f"**Phone:** {order['contact_phone']}")
            st.markdown(f"**Quantity:** {order['quantity']}")
            st.markdown(f"**Assigned Company:** {order['assigned_company']}")
        with col2:
            st.markdown(f"**Created By:** {order['created_by']}")
            st.markdown(f"**Date Created:** {order['date_created']}")
            st.markdown(f"**Expected Delivery:** {order['expected_delivery_date']}")
            st.markdown(f"**Last Updated:** {order['last_updated']}")
        st.markdown(f"**Description:** {order['item_description']}")
        if order["remarks"]: st.markdown(f"**Remarks:** {order['remarks']}")

    def show_latest(table_key, order_id):
        rows = data[table_key][data[table_key]["order_id"] == order_id]
        if len(rows) == 0:
            st.info("No data recorded yet.")
        else:
            row = rows.iloc[-1]
            for col_name, val in row.items():
                if col_name not in ["id","order_id"] and val and val != "nan":
                    st.markdown(f"**{col_name.replace('_',' ').title()}:** {val}")

    with t2: show_latest("procurement", order_id)
    with t3: show_latest("dispatch", order_id)
    with t4: show_latest("delivery", order_id)
    with t5: show_latest("invoices", order_id)

    # Activity log
    st.markdown("---")
    st.markdown("### 📋 Activity Log")
    logs = data["activity_log"][data["activity_log"]["order_id"] == order_id]
    if len(logs) == 0:
        st.info("No activity yet.")
    else:
        for _, log in logs.iloc[::-1].iterrows():
            with st.container():
                col1, col2 = st.columns([3,1])
                with col1:
                    st.markdown(f"🔵 **{log['action_type']}** — {log['details']} — by **{log['performed_by']}**")
                    if log["previous_status"] and log["previous_status"] != "nan":
                        st.caption(f"{log['previous_status']} → {log['new_status']}")
                with col2:
                    st.caption(log["performed_at"])
                st.markdown("---")

# ── ACTIVITY LOG ──────────────────────────────────────────────────────────────
def page_activity_log():
    page_title("📋","Activity Log","Complete audit trail of all order changes")
    logs = data["activity_log"].copy().iloc[::-1].reset_index(drop=True)
    st.markdown(f"**{len(logs)} total events**")
    st.dataframe(logs, use_container_width=True, hide_index=True)

# ── REPORTS ───────────────────────────────────────────────────────────────────
def page_reports():
    page_title("📈","Reports","Financial summaries and order analytics")
    orders = data["orders"].copy()
    orders["total_value"] = orders["total_value"].astype(float)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### By Company")
        for company in COMPANIES:
            co_orders = orders[orders["company"] == company]
            cnt = len(co_orders)
            val = co_orders["total_value"].sum()
            st.markdown(f"**{company}** — {cnt} orders · ₹{val:,.0f}")
            st.progress(cnt / max(len(orders), 1))

    with col2:
        st.markdown("#### By Status")
        for status in STATUSES:
            cnt = len(orders[orders["current_status"] == status])
            pct = cnt / max(len(orders), 1)
            st.markdown(f"{STATUS_EMOJI.get(status,'')} **{status}** — {cnt}")
            st.progress(pct)

    st.markdown("---")
    st.markdown("#### Financial Summary")
    summary_rows = []
    for _, row in orders.iterrows():
        summary_rows.append({
            "Order ID":    row["order_id"],
            "Company":     row["company"],
            "Department":  row["govt_department"],
            "Total Value": f"₹{row['total_value']:,.0f}",
            "Status":      row["current_status"],
            "Paid":        f"₹{row['total_value']:,.0f}" if row["current_status"]=="Paid" else "—",
            "Outstanding": "—" if row["current_status"]=="Paid" else f"₹{row['total_value']:,.0f}",
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

# ── ADMIN ─────────────────────────────────────────────────────────────────────
def page_admin():
    page_title("⚙️","Admin Panel","Manage data exports, users, and system settings")

    st.info("✅ **Auto-Save** — All data saves to CSV files automatically on the server.\n\n"
            "📥 **Export CSV** — Download any table directly to your computer.\n\n"
            "🔄 **Status** — Updates instantly after every save.")

    st.markdown("### 📥 Export Data to CSV")
    cols = st.columns(3)
    tables = ["orders","procurement","dispatch","delivery","invoices","activity_log"]
    for i, table in enumerate(tables):
        with cols[i % 3]:
            csv = df_to_csv_bytes(data[table])
            st.download_button(
                label=f"📄 {table} ({len(data[table])} rows)",
                data=csv,
                file_name=f"supply_chain_{table}_{now_ist()[:10]}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"dl_{table}"
            )

    st.markdown("---")
    st.markdown("### ⚙️ Database Stats")
    cols2 = st.columns(6)
    for i, table in enumerate(tables):
        with cols2[i]:
            st.metric(table, len(data[table]))

    st.markdown("---")
    st.markdown("### 👥 Users & Roles")
    user_rows = [{"Username": u, "Name": v["name"], "Role": v["role"]} for u, v in USERS.items()]
    st.dataframe(pd.DataFrame(user_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### ⚠️ Danger Zone")
    with st.expander("Reset Data (⚠️ Irreversible)"):
        if st.button("🗑 Reset All Data to Sample Data", type="primary"):
            for key, df in SEED.items():
                df.astype(str).fillna("").to_csv(FILES[key], index=False)
            st.session_state.data = load_data()
            st.success("✅ Data reset to sample data.")
            st.rerun()

# ─── FOOTER ───────────────────────────────────────────────────────────────────
def show_footer():
    st.markdown(f"""
    <div style="text-align:center;font-size:11px;color:#94a3b8;
                padding:10px 0 4px 0;border-top:1px solid #e2e8f0;margin-top:2rem;">
        © {datetime.now().year} Robokart. All rights reserved. Supply Chain Tracking System.
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    sidebar()

    menu = st.session_state.get("menu", "Dashboard")
    if   menu == "Dashboard":    page_dashboard()
    elif menu == "New Order":    page_new_order()
    elif menu == "Update Order": page_update_order()
    elif menu == "Order Details":page_order_details()
    elif menu == "Activity Log": page_activity_log()
    elif menu == "Reports":      page_reports()
    elif menu == "Admin":        page_admin()

    show_footer()

if __name__ == "__main__":
    main()
