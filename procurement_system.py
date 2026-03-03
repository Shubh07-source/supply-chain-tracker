import streamlit as st
import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  — must be first Streamlit call
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Supply Chain Tracking System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
COMPANIES  = ["Robokart", "Bharat Tech", "EL"]
STATUSES   = ["Pending", "Procured", "Dispatched", "Delivered", "Invoiced", "Paid"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]

STATUS_EMOJI = {"Pending":"⏳","Procured":"🔧","Dispatched":"🚚","Delivered":"📦","Invoiced":"🧾","Paid":"💰"}
STATUS_BG    = {"Pending":"#fef3c7","Procured":"#dbeafe","Dispatched":"#ede9fe","Delivered":"#d1fae5","Invoiced":"#cffafe","Paid":"#dcfce7"}
STATUS_FG    = {"Pending":"#d97706","Procured":"#2563eb","Dispatched":"#7c3aed","Delivered":"#059669","Invoiced":"#0891b2","Paid":"#16a34a"}
PRIO_BG      = {"Low":"#f1f5f9","Medium":"#dbeafe","High":"#fef3c7","Urgent":"#fee2e2"}
PRIO_FG      = {"Low":"#64748b","Medium":"#2563eb","High":"#d97706","Urgent":"#dc2626"}
CO_BG        = {"Robokart":"#ede9fe","Bharat Tech":"#cffafe","EL":"#ffedd5"}
CO_FG        = {"Robokart":"#7c3aed","Bharat Tech":"#0891b2","EL":"#c2410c"}

USERS = {
    "Admin":   {"password":"admin@123",    "role":"Admin",   "name":"System Admin"},
    "Manager": {"password":"mgr@123",      "role":"Manager", "name":"Ops Manager"},
    "Staff":   {"password":"Ops@Secure#1", "role":"Staff",   "name":"Operations Staff"},
    "Viewer":  {"password":"view123",      "role":"Viewer",  "name":"Finance Viewer"},
}
ROLE_MENUS = {
    "Admin":   ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports","Admin"],
    "Manager": ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports"],
    "Staff":   ["Dashboard","Update Order","Order Details","Activity Log"],
    "Viewer":  ["Dashboard","Order Details","Activity Log"],
}
MENU_ICONS = {
    "Dashboard":"📊","New Order":"➕","Update Order":"🔄",
    "Order Details":"🔍","Activity Log":"📋","Reports":"📈","Admin":"⚙️",
}
ROLE_COLOR = {"Admin":"#dc2626","Manager":"#d97706","Staff":"#2563eb","Viewer":"#059669"}
ROLE_BG    = {"Admin":"#fee2e2","Manager":"#fef3c7","Staff":"#dbeafe","Viewer":"#dcfce7"}

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LAYER
# ═══════════════════════════════════════════════════════════════════════════════
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
FILES = {k: f"{DATA_DIR}/{k}.csv" for k in ["orders","procurement","dispatch","delivery","invoices","activity_log"]}

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
        {"id":1,"order_id":"ORD-2026-02-28-003","delivery_status":"Delivered","delivery_date":"2026-02-19","receiver_name":"Col. Vikram Singh","delivered_quantity":10,"challan_number":"CH-DEF-001","delivery_files":"0 file(s)","challan_files":"0 file(s)","updated_by":"Ops","updated_at":"2026-02-19 16:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-004","delivery_status":"Delivered","delivery_date":"2026-02-26","receiver_name":"Ms. Anita Verma","delivered_quantity":30,"challan_number":"CH-SCM-004","delivery_files":"0 file(s)","challan_files":"0 file(s)","updated_by":"Dev","updated_at":"2026-02-26 14:30:00"},
    ]),
    "invoices": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-003","invoice_number":"INV-2026-0321","invoice_date":"2026-02-20","invoice_amount":1500000,"payment_status":"Completed","payment_date":"2026-02-24","payment_mode":"NEFT","transaction_reference":"TXN20260224DEF","invoice_files":"0 file(s)","updated_by":"Finance","updated_at":"2026-02-24 16:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-004","invoice_number":"INV-2026-0389","invoice_date":"2026-02-27","invoice_amount":670000,"payment_status":"Approved","payment_date":"","payment_mode":"","transaction_reference":"","invoice_files":"0 file(s)","updated_by":"Finance","updated_at":"2026-02-27 11:00:00"},
    ]),
    "activity_log": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-001","action_type":"ORDER_CREATED","previous_status":"—","new_status":"Pending","performed_by":"Admin","performed_at":"2026-02-10 09:30:00","details":"Order created"},
        {"id":2,"order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Pending","new_status":"Procured","performed_by":"Rahul","performed_at":"2026-02-15 14:00:00","details":"Procurement completed"},
        {"id":3,"order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Procured","new_status":"Dispatched","performed_by":"Rahul","performed_at":"2026-02-18 08:30:00","details":"Dispatched via BlueDart"},
        {"id":4,"order_id":"ORD-2026-02-28-003","action_type":"PAYMENT","previous_status":"Invoiced","new_status":"Paid","performed_by":"Finance","performed_at":"2026-02-24 16:00:00","details":"NEFT payment received"},
        {"id":5,"order_id":"ORD-2026-02-28-004","action_type":"STATUS_CHANGE","previous_status":"Dispatched","new_status":"Delivered","performed_by":"Dev","performed_at":"2026-02-26 14:30:00","details":"Delivered, challan signed"},
    ]),
}

def now_ist():
    return datetime.now(timezone(timedelta(hours=5,minutes=30))).strftime("%Y-%m-%d %H:%M:%S")

def load_data():
    out = {}
    for key, path in FILES.items():
        if os.path.exists(path):
            out[key] = pd.read_csv(path, dtype=str).fillna("")
        else:
            df = SEED[key].copy().astype(str).fillna("")
            df.to_csv(path, index=False)
            out[key] = df
    return out

def save_table(key):
    st.session_state.data[key].to_csv(FILES[key], index=False)

def add_log(order_id, action, prev, new_s, by, details):
    D   = st.session_state.data
    ts  = now_ist()
    row = pd.DataFrame([{"id":str(len(D["activity_log"])+1),"order_id":order_id,
                          "action_type":action,"previous_status":prev,"new_status":new_s,
                          "performed_by":by,"performed_at":ts,"details":details}])
    D["activity_log"] = pd.concat([D["activity_log"],row],ignore_index=True)
    save_table("activity_log")

def update_order_status(order_id, new_status):
    D  = st.session_state.data
    ts = now_ist()
    D["orders"].loc[D["orders"]["order_id"]==order_id,"current_status"] = new_status
    D["orders"].loc[D["orders"]["order_id"]==order_id,"last_updated"]   = ts
    save_table("orders")

def get_order(order_id):
    rows = st.session_state.data["orders"]
    rows = rows[rows["order_id"]==order_id]
    return rows.iloc[0] if len(rows) else None

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════════════════════
for k,v in [("logged_in",False),("username",""),("role",""),("user_name",""),
            ("menu","Dashboard"),("company_filter","All")]:
    if k not in st.session_state:
        st.session_state[k] = v
if "data" not in st.session_state:
    st.session_state.data = load_data()

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Light, clean, IBM Plex Sans, white background
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif !important;
    background-color: #f0f4f8 !important;
    color: #0f172a !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0c1426 !important;
    min-width: 220px !important;
    max-width: 220px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 !important;
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    padding: 10px 18px !important;
    margin: 0 !important;
    transition: all 0.12s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.06) !important;
    color: #fff !important;
    border-left-color: #3b82f6 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #1d4ed8 !important;
    color: #fff !important;
    font-weight: 700 !important;
    border-left: 3px solid #60a5fa !important;
    border-radius: 6px !important;
    margin: 2px 10px !important;
    width: calc(100% - 20px) !important;
}

/* ── Main content wrapper ── */
.main-content {
    padding: 28px 32px 40px 32px;
    background: #f0f4f8;
    min-height: 100vh;
}

/* ── Page header ── */
.ph-wrap {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 16px;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 24px;
    background: #fff;
    padding: 14px 32px;
    border-bottom: 1px solid #e2e8f0;
}
.ph-title { font-size: 20px; font-weight: 800; color: #0f172a; }
.ph-right { display: flex; align-items: center; gap: 16px; }
.ph-saved { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #16a34a; font-weight: 600; }
.ph-dot   { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; display: inline-block; }
.ph-date  { font-size: 12px; color: #94a3b8; }

/* ── Metric cards ── */
.metric-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: 14px; margin-bottom: 24px; }
.metric-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.metric-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px; color: #64748b; margin-bottom: 8px; }
.metric-value { font-size: 26px; font-weight: 800; }

/* ── Filter pills ── */
.pill-row { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.pill {
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 12.5px;
    font-weight: 600;
    border: 1.5px solid #e2e8f0;
    background: #fff;
    color: #374151;
    cursor: pointer;
    white-space: nowrap;
}
.pill-active-all  { background:#dbeafe; color:#1d4ed8; border-color:#1d4ed8; }
.pill-active-rk   { background:#ede9fe; color:#7c3aed; border-color:#7c3aed; }
.pill-active-bt   { background:#cffafe; color:#0891b2; border-color:#0891b2; }
.pill-active-el   { background:#ffedd5; color:#c2410c; border-color:#c2410c; }

/* ── Cards ── */
.sc-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
.sc-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 13px 18px;
    border-bottom: 1px solid #f1f5f9;
    background: #fafbfc;
}
.sc-card-title { font-size: 14px; font-weight: 700; color: #0f172a; }
.sc-card-count {
    font-size: 11px; font-weight: 600; color: #64748b;
    background: #f1f5f9; padding: 3px 12px; border-radius: 99px;
}
.sc-card-body { padding: 18px; }

/* ── Table ── */
.orders-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.orders-table th {
    padding: 10px 14px;
    background: #f8fafc;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #475569;
    border-bottom: 2px solid #e2e8f0;
    text-align: left;
    white-space: nowrap;
}
.orders-table td {
    padding: 12px 14px;
    border-bottom: 1px solid #f1f5f9;
    color: #1e293b;
    vertical-align: middle;
}
.orders-table tr:hover td { background: #f8faff; }

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    white-space: nowrap;
}
.co-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
}

/* ── Form styling ── */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    border-radius: 7px !important;
    border: 1px solid #d1d5db !important;
    font-size: 13px !important;
    background: #fff !important;
    color: #0f172a !important;
    padding: 8px 12px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.1) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stNumberInput label, .stDateInput label, .stFileUploader label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #374151 !important;
    margin-bottom: 4px !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
.stButton > button[kind="primary"] {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    color: #fff !important;
}
.stButton > button[kind="primary"]:hover { background: #1e40af !important; }
.stButton > button[kind="secondary"] {
    background: #fff !important;
    border: 1px solid #e2e8f0 !important;
    color: #374151 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #e2e8f0 !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: #64748b !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    border-bottom: 2px solid #1d4ed8 !important;
    color: #1d4ed8 !important;
    font-weight: 700 !important;
}

/* ── DataFrames ── */
.stDataFrame {
    border-radius: 10px !important;
    border: 1px solid #e2e8f0 !important;
    overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}

/* ── Progress bar ── */
.stProgress > div { background: #f1f5f9 !important; border-radius: 4px !important; height: 6px !important; }
.stProgress > div > div { background: #1d4ed8 !important; border-radius: 4px !important; }

/* ── Alerts ── */
.stSuccess, .stError, .stInfo, .stWarning { border-radius: 8px !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #f8fafc !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ── Dividers ── */
hr { border-color: #e2e8f0 !important; margin: 16px 0 !important; }

/* ── Login page ── */
.login-page-bg {
    min-height: 100vh;
    background: linear-gradient(135deg, #0c1426 0%, #1a3a6b 60%, #0c1426 100%);
    display: flex; align-items: center; justify-content: center;
}

/* ── Step bar ── */
.step-bar { display: flex; align-items: center; margin-bottom: 20px; }
.step-node {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.step-done    { background: #1d4ed8; color: #fff; }
.step-pending { background: #e2e8f0; color: #94a3b8; }
.step-line-d  { flex: 1; height: 2px; background: #1d4ed8; margin: 0 4px; }
.step-line-p  { flex: 1; height: 2px; background: #e2e8f0; margin: 0 4px; }
.step-label   { font-size: 9px; text-align: center; margin-top: 4px; font-weight: 600; }

/* ── Info row ── */
.info-row {
    display: flex; gap: 12px; flex-wrap: wrap;
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;
}
.info-item { flex: 1; min-width: 120px; }
.info-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; margin-bottom: 4px; }
.info-value { font-size: 13px; font-weight: 600; color: #0f172a; }

/* ── Log entry ── */
.log-entry {
    display: flex; gap: 12px;
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;
}
.log-dot { width: 8px; height: 8px; border-radius: 50%; background: #1d4ed8; flex-shrink: 0; margin-top: 5px; }

/* ── Footer ── */
.sc-footer {
    text-align: center; font-size: 11px; color: #94a3b8;
    padding: 14px 0 8px 0; border-top: 1px solid #e2e8f0; margin-top: 32px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def sbadge(status):
    bg = STATUS_BG.get(status,"#f1f5f9"); fg = STATUS_FG.get(status,"#64748b")
    return f'<span class="badge" style="background:{bg};color:{fg};">{STATUS_EMOJI.get(status,"")} {status}</span>'

def pbadge(priority):
    bg = PRIO_BG.get(priority,"#f1f5f9"); fg = PRIO_FG.get(priority,"#64748b")
    return f'<span class="badge" style="background:{bg};color:{fg};">{priority}</span>'

def cobadge(company):
    bg = CO_BG.get(company,"#f1f5f9"); fg = CO_FG.get(company,"#64748b")
    return f'<span class="co-tag" style="background:{bg};color:{fg};">{company}</span>'

def card_start(title, count=None):
    cnt_html = f'<span class="sc-card-count">{count}</span>' if count is not None else ""
    st.markdown(f'<div class="sc-card"><div class="sc-card-header"><span class="sc-card-title">{title}</span>{cnt_html}</div><div class="sc-card-body">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div></div>', unsafe_allow_html=True)

def page_header(title, subtitle=""):
    today = datetime.now().strftime("%d %b %Y")
    sub_html = f'<div style="font-size:12px;color:#64748b;margin-top:2px;">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="ph-wrap">
        <div>
            <div class="ph-title">{title}</div>
            {sub_html}
        </div>
        <div class="ph-right">
            <span class="ph-saved"><span class="ph-dot"></span> Auto-saved</span>
            <span class="ph-date">{today}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_footer():
    st.markdown(f'<div class="sc-footer">© {datetime.now().year} Robokart. All rights reserved. Supply Chain Tracking System.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def login_page():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg,#0c1426 0%,#1a3a6b 60%,#0c1426 100%) !important; }
    [data-testid="stSidebar"] { display: none !important; }
    section[data-testid="stSidebar"] + div .block-container { padding: 0 !important; }
    </style>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.0, 1])
    with mid:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        # Card header — HTML only
        st.markdown("""
        <div style="background:#ffffff;border-radius:14px 14px 0 0;padding:36px 40px 24px;
                    box-shadow:0 2px 0 #e2e8f0;text-align:center;">
            <div style="font-size:44px;margin-bottom:10px;">🏭</div>
            <div style="font-size:22px;font-weight:800;color:#0f172a;line-height:1.3;">
                Supply Chain Tracking System
            </div>
            <div style="font-size:13px;color:#64748b;margin-top:8px;">
                Sign in with your credentials to continue
            </div>
        </div>""", unsafe_allow_html=True)

        # Form body
        st.markdown("""
        <div style="background:#ffffff;border-radius:0 0 14px 14px;
                    padding:0 40px 36px;box-shadow:0 20px 60px rgba(0,0,0,0.35);">
        </div>""", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div style="background:#fff;border-radius:0 0 14px 14px;padding:8px 40px 36px;box-shadow:0 20px 60px rgba(0,0,0,0.35);margin-top:-8px;">', unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")
                if submitted:
                    if username in USERS and USERS[username]["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.username  = username
                        st.session_state.role      = USERS[username]["role"]
                        st.session_state.user_name = USERS[username]["name"]
                        st.session_state.menu      = "Dashboard"
                        st.rerun()
                    else:
                        st.error("⚠ Invalid username or password. Please try again.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <p style="text-align:center;font-size:12px;color:#94a3b8;margin-top:16px;">
            Contact your administrator for login credentials.
        </p>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        # Logo block
        st.markdown("""
        <div style="padding:22px 18px 16px;border-bottom:1px solid #1e293b;">
            <div style="font-size:20px;font-weight:800;color:#f97316;">🏭 Supply Chain</div>
            <div style="font-size:10px;color:#475569;letter-spacing:1px;margin-top:3px;">TRACKING SYSTEM</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Navigation
        menus = ROLE_MENUS[st.session_state.role]
        for m in menus:
            active = st.session_state.menu == m
            icon   = MENU_ICONS.get(m,"")
            if st.button(f"{icon}  {m}", key=f"nav_{m}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.menu = m
                st.rerun()

        # User block at bottom
        role   = st.session_state.role
        rc     = ROLE_COLOR.get(role,"#64748b")
        rb     = ROLE_BG.get(role,"#f1f5f9")
        st.markdown(f"""
        <div style="position:fixed;bottom:0;width:200px;padding:14px 18px;
                    border-top:1px solid #1e293b;background:#0c1426;">
            <div style="font-size:13px;font-weight:700;color:#fff;margin-bottom:6px;">
                {st.session_state.user_name}
            </div>
            <span style="background:{rb};color:{rc};padding:2px 10px;border-radius:99px;
                         font-size:11px;font-weight:700;">{role}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        if st.button("← Sign Out", use_container_width=True, key="signout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    page_header("📊 Dashboard", "Overview of all purchase orders and supply chain status")

    D      = st.session_state.data
    orders = D["orders"].copy()
    cf     = st.session_state.company_filter
    fil    = orders if cf == "All" else orders[orders["company"] == cf]
    tv     = fil["total_value"].astype(float).sum() if len(fil) else 0.0

    # ── Metric cards ──
    metrics = [
        ("TOTAL ORDERS",  str(len(fil)),                                                                          "#1d4ed8"),
        ("PENDING",       str(len(fil[fil["current_status"]=="Pending"])),                                        "#d97706"),
        ("IN TRANSIT",    str(len(fil[fil["current_status"].isin(["Procured","Dispatched"])])),                   "#7c3aed"),
        ("DELIVERED",     str(len(fil[fil["current_status"].isin(["Delivered","Invoiced","Paid"])])),             "#059669"),
        ("PAID",          str(len(fil[fil["current_status"]=="Paid"])),                                           "#16a34a"),
        ("TOTAL VALUE",   f"₹{tv/100000:.1f}L",                                                                   "#f97316"),
    ]
    cols = st.columns(6)
    for col,(label,value,color) in zip(cols,metrics):
        with col:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e2e8f0;border-top:3px solid {color};
                        border-radius:10px;padding:16px 18px;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.7px;color:#64748b;">{label}</div>
                <div style="font-size:26px;font-weight:800;margin-top:8px;color:{color};">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Company filter ──
    c_all, c_rk, c_bt, c_el, _ = st.columns([1.3,1,1.2,0.7,3])
    with c_all:
        if st.button("🏢 All Companies" + (" ✓" if cf=="All" else ""), key="f_all",
                     type="primary" if cf=="All" else "secondary", use_container_width=True):
            st.session_state.company_filter="All"; st.rerun()
    with c_rk:
        if st.button("Robokart" + (" ✓" if cf=="Robokart" else ""), key="f_rk",
                     type="primary" if cf=="Robokart" else "secondary", use_container_width=True):
            st.session_state.company_filter="Robokart"; st.rerun()
    with c_bt:
        if st.button("Bharat Tech" + (" ✓" if cf=="Bharat Tech" else ""), key="f_bt",
                     type="primary" if cf=="Bharat Tech" else "secondary", use_container_width=True):
            st.session_state.company_filter="Bharat Tech"; st.rerun()
    with c_el:
        if st.button("EL" + (" ✓" if cf=="EL" else ""), key="f_el",
                     type="primary" if cf=="EL" else "secondary", use_container_width=True):
            st.session_state.company_filter="EL"; st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Orders HTML table ──
    title = "All Orders" if cf=="All" else f"{cf} Orders"
    st.markdown(f"""
    <div class="sc-card">
        <div class="sc-card-header">
            <span class="sc-card-title">📦 {title}</span>
            <span class="sc-card-count">{len(fil)} orders</span>
        </div>
        <div style="overflow-x:auto;">
    """, unsafe_allow_html=True)

    if len(fil) == 0:
        st.markdown('<div style="padding:24px;text-align:center;color:#94a3b8;font-size:13px;">No orders for this company.</div>', unsafe_allow_html=True)
    else:
        TH = "padding:10px 14px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;white-space:nowrap;"
        TD = "padding:12px 14px;border-bottom:1px solid #f1f5f9;color:#1e293b;vertical-align:middle;font-size:12.5px;"
        rows = ""
        for i,(_, r) in enumerate(fil.iterrows()):
            bg = "#fff" if i%2==0 else "#fafbfc"
            rows += f"""<tr style="background:{bg};">
                <td style="{TD}font-weight:700;color:#1d4ed8;font-size:11.5px;">{r['order_id']}</td>
                <td style="{TD}">{cobadge(r['company'])}</td>
                <td style="{TD}color:#64748b;">{r['po_number']}</td>
                <td style="{TD}">{r['govt_department']}</td>
                <td style="{TD}max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{r['item_description']}</td>
                <td style="{TD}text-align:right;">{r['quantity']}</td>
                <td style="{TD}font-weight:700;">₹{float(r['total_value']):,.0f}</td>
                <td style="{TD}">{pbadge(r['priority'])}</td>
                <td style="{TD}">{sbadge(r['current_status'])}</td>
                <td style="{TD}color:#94a3b8;font-size:11px;white-space:nowrap;">{r['last_updated']}</td>
            </tr>"""
        st.markdown(f"""
        <table class="orders-table">
            <thead><tr>
                <th style="{TH}">Order ID</th><th style="{TH}">Company</th>
                <th style="{TH}">PO Number</th><th style="{TH}">Department</th>
                <th style="{TH}">Description</th><th style="{TH}">Qty</th>
                <th style="{TH}">Value</th><th style="{TH}">Priority</th>
                <th style="{TH}">Status</th><th style="{TH}">Last Updated</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# NEW ORDER
# ═══════════════════════════════════════════════════════════════════════════════
def page_new_order():
    page_header("➕ New Order", "Create a new government purchase order")
    D = st.session_state.data

    card_start("📝 Purchase Order Details")
    with st.form("new_order_form", clear_on_submit=True):
        st.markdown("**Select Company \\***")
        company = st.selectbox("Company", COMPANIES, label_visibility="collapsed", key="no_company")
        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            govt_dept    = st.text_input("Govt Department *",    placeholder="e.g., Education Department Delhi")
            contact_name = st.text_input("Contact Person *",     placeholder="e.g., Mr. Rajesh Kumar")
            contact_ph   = st.text_input("Contact Phone",        placeholder="e.g., 9876543210")
            po_number    = st.text_input("PO Number *",          placeholder="e.g., PO/EDU/2026/001")
        with c2:
            assigned_co  = st.text_input("Assigned Company",     placeholder="e.g., Tech Solutions Pvt Ltd")
            exp_delivery = st.date_input("Expected Delivery Date")
            quantity     = st.number_input("Quantity *",         min_value=1, value=1)
            total_value  = st.number_input("Total Value (₹) *",  min_value=0, value=0)
        c3,_ = st.columns([1,2])
        with c3:
            priority = st.selectbox("Priority", PRIORITIES, index=1)
        item_desc = st.text_area("Item Description *", placeholder="Detailed description of goods/services to be procured...", height=100)
        remarks   = st.text_area("Remarks",            placeholder="Any additional remarks or special instructions...", height=70)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Create Order", use_container_width=True, type="primary")

        if submitted:
            errors = []
            if not govt_dept:    errors.append("Govt Department")
            if not contact_name: errors.append("Contact Person")
            if not po_number:    errors.append("PO Number")
            if not item_desc:    errors.append("Item Description")
            if not total_value:  errors.append("Total Value")
            if errors:
                st.error(f"Please fill: {', '.join(errors)}")
            elif po_number in D["orders"]["po_number"].values:
                st.error("⚠ PO Number already exists!")
            else:
                ts       = now_ist()
                order_id = f"ORD-{ts[:10]}-{str(len(D['orders'])+1).zfill(3)}"
                new_row  = pd.DataFrame([{
                    "order_id":order_id,"date_created":ts,"company":company,
                    "govt_department":govt_dept,"contact_person":contact_name,
                    "contact_phone":contact_ph,"po_number":po_number,
                    "item_description":item_desc,"quantity":str(quantity),
                    "total_value":str(total_value),"assigned_company":assigned_co,
                    "current_status":"Pending","priority":priority,
                    "expected_delivery_date":str(exp_delivery),
                    "remarks":remarks,"created_by":st.session_state.user_name,"last_updated":ts
                }])
                D["orders"] = pd.concat([D["orders"],new_row],ignore_index=True)
                save_table("orders")
                add_log(order_id,"ORDER_CREATED","—","Pending",st.session_state.user_name,f"Order created [{company}]")
                st.success(f"✅ Order **{order_id}** created successfully!")
    card_end()
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE ORDER
# ═══════════════════════════════════════════════════════════════════════════════
def page_update_order():
    page_header("🔄 Update Order", "Update procurement, dispatch, delivery or invoice status")
    D = st.session_state.data

    order_opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  [{r['current_status']}]"
        for _,r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order *", order_opts, key="uo_sel")
    if sel == "— Select an order —":
        st.info("👆 Select an order above to begin updating.")
        show_footer()
        return

    oid   = sel.split("  ·  ")[0].strip()
    order = get_order(oid)

    # Live status info bar
    s  = order["current_status"]
    co = order["company"]
    st.markdown(f"""
    <div class="info-row">
        <div class="info-item">
            <div class="info-label">Company</div>
            <div class="info-value">{cobadge(co)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Current Status</div>
            <div class="info-value">{sbadge(s)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Order Value</div>
            <div class="info-value" style="font-weight:700;">₹{float(order['total_value']):,.0f}</div>
        </div>
        <div class="info-item" style="flex:2">
            <div class="info-label">Department</div>
            <div class="info-value">{order['govt_department']}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Priority</div>
            <div class="info-value">{pbadge(order['priority'])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    updated_by = st.text_input("Your Name / Department *", placeholder="e.g., Rahul — Logistics Team", key="uo_by")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["🔧  Procurement", "🚚  Dispatch", "📦  Delivery", "💰  Invoice"])

    # ── PROCUREMENT ──
    with tab1:
        with st.form("proc_form"):
            c1,c2 = st.columns(2)
            with c1:
                p_status = st.selectbox("Procurement Status *", ["","Not_Started","In_Progress","Completed","On_Hold"])
                p_date   = st.date_input("Procurement Date", key="pd")
                p_source = st.text_input("Materials Source", placeholder="Vendor / Warehouse name")
            with c2:
                p_qc     = st.selectbox("QC Status", ["","Pending","In_Progress","Passed","Failed"])
                p_notes  = st.text_area("Notes", height=110)
            sv = st.form_submit_button("✅ Save Procurement Update", use_container_width=True, type="primary")
            if sv:
                if not updated_by: st.error("Please enter your name above the tabs."); st.stop()
                ts = now_ist()
                row = pd.DataFrame([{"id":str(len(D["procurement"])+1),"order_id":oid,
                    "procurement_status":p_status,"procurement_date":str(p_date),
                    "materials_source":p_source,"quality_check_status":p_qc,
                    "notes":p_notes,"updated_by":updated_by,"updated_at":ts}])
                D["procurement"] = pd.concat([D["procurement"],row],ignore_index=True)
                save_table("procurement")
                ns = "Procured" if p_status=="Completed" else order["current_status"]
                prev = order["current_status"]
                update_order_status(oid, ns)
                add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,f"Procurement: {p_status}")
                st.success(f"✅ Saved! Status updated → **{ns}**")
                st.rerun()

    # ── DISPATCH ──
    with tab2:
        with st.form("disp_form"):
            c1,c2 = st.columns(2)
            with c1:
                d_date    = st.date_input("Dispatch Date", key="dd")
                d_courier = st.text_input("Courier / Transporter *", placeholder="e.g., BlueDart, DTDC")
                d_vehicle = st.text_input("Vehicle Number", placeholder="e.g., DL01AB1234")
            with c2:
                d_driver  = st.text_input("Driver Contact")
                d_track   = st.text_input("Tracking Number")
                d_expd    = st.date_input("Expected Delivery", key="ded")
            sv = st.form_submit_button("✅ Save Dispatch Update", use_container_width=True, type="primary")
            if sv:
                if not updated_by: st.error("Please enter your name above the tabs."); st.stop()
                ts = now_ist()
                row = pd.DataFrame([{"id":str(len(D["dispatch"])+1),"order_id":oid,
                    "dispatch_date":str(d_date),"courier_name":d_courier,
                    "vehicle_number":d_vehicle,"driver_contact":d_driver,
                    "tracking_number":d_track,"expected_delivery_date":str(d_expd),
                    "updated_by":updated_by,"updated_at":ts}])
                D["dispatch"] = pd.concat([D["dispatch"],row],ignore_index=True)
                save_table("dispatch")
                prev = order["current_status"]
                update_order_status(oid,"Dispatched")
                add_log(oid,"STATUS_CHANGE",prev,"Dispatched",updated_by,f"Dispatched via {d_courier}")
                st.success("✅ Dispatch saved! Status → **Dispatched**")
                st.rerun()

    # ── DELIVERY ──
    with tab3:
        with st.form("del_form"):
            c1,c2 = st.columns(2)
            with c1:
                de_status = st.selectbox("Delivery Status *", ["","Delivered","Partial","Failed","Rescheduled"])
                de_date   = st.date_input("Delivery Date", key="dld")
                de_recv   = st.text_input("Receiver Name")
            with c2:
                de_qty    = st.number_input("Delivered Quantity", min_value=0, key="dq")
                de_ch     = st.text_input("Challan Number")
            st.markdown("**📸 Delivery Photos / Files** *(any type, multiple allowed)*")
            del_files = st.file_uploader("Upload delivery proof", accept_multiple_files=True, key="dlf", label_visibility="collapsed")
            st.markdown("**📋 Challan Documents** *(PDF, images, etc.)*")
            ch_files  = st.file_uploader("Upload challan copies", accept_multiple_files=True, key="chf", label_visibility="collapsed")
            sv = st.form_submit_button("✅ Save Delivery Update", use_container_width=True, type="primary")
            if sv:
                if not updated_by: st.error("Please enter your name above the tabs."); st.stop()
                ts = now_ist()
                row = pd.DataFrame([{"id":str(len(D["delivery"])+1),"order_id":oid,
                    "delivery_status":de_status,"delivery_date":str(de_date),
                    "receiver_name":de_recv,"delivered_quantity":str(de_qty),
                    "challan_number":de_ch,
                    "delivery_files":f"{len(del_files or [])} file(s)",
                    "challan_files":f"{len(ch_files or [])} file(s)",
                    "updated_by":updated_by,"updated_at":ts}])
                D["delivery"] = pd.concat([D["delivery"],row],ignore_index=True)
                save_table("delivery")
                ns = "Delivered" if de_status=="Delivered" else order["current_status"]
                prev = order["current_status"]
                update_order_status(oid, ns)
                add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,
                        f"Delivery: {de_status} | {len(del_files or [])} delivery + {len(ch_files or [])} challan files")
                st.success(f"✅ Delivery saved! Status → **{ns}**")
                st.rerun()

    # ── INVOICE ──
    with tab4:
        with st.form("inv_form"):
            c1,c2 = st.columns(2)
            with c1:
                i_num    = st.text_input("Invoice Number", placeholder="e.g., INV-2026-0001")
                i_date   = st.date_input("Invoice Date", key="id")
                i_amount = st.number_input("Invoice Amount (₹)", min_value=0, key="ia")
                i_pstat  = st.selectbox("Payment Status *", ["","Pending","Approved","Completed"])
            with c2:
                i_pmode  = st.selectbox("Payment Mode", ["","NEFT","RTGS","Cheque","DD","Online","Cash"])
                i_txn    = st.text_input("Transaction Reference")
                i_pdate  = st.date_input("Payment Date", key="ipd")
            st.markdown("**🧾 Invoice Files** *(PDF, Excel, scanned copies — multiple allowed)*")
            inv_files = st.file_uploader("Upload invoice files", accept_multiple_files=True, key="ivf", label_visibility="collapsed")
            sv = st.form_submit_button("✅ Save Invoice Update", use_container_width=True, type="primary")
            if sv:
                if not updated_by: st.error("Please enter your name above the tabs."); st.stop()
                ts = now_ist()
                row = pd.DataFrame([{"id":str(len(D["invoices"])+1),"order_id":oid,
                    "invoice_number":i_num,"invoice_date":str(i_date),
                    "invoice_amount":str(i_amount),"payment_status":i_pstat,
                    "payment_date":str(i_pdate),"payment_mode":i_pmode,
                    "transaction_reference":i_txn,
                    "invoice_files":f"{len(inv_files or [])} file(s)",
                    "updated_by":updated_by,"updated_at":ts}])
                D["invoices"] = pd.concat([D["invoices"],row],ignore_index=True)
                save_table("invoices")
                ns = "Paid" if i_pstat=="Completed" else "Invoiced"
                prev = order["current_status"]
                update_order_status(oid, ns)
                add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,
                        f"Invoice {i_num} | {i_pstat} | {len(inv_files or [])} files")
                st.success(f"✅ Invoice saved! Status → **{ns}**")
                st.rerun()

    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# ORDER DETAILS
# ═══════════════════════════════════════════════════════════════════════════════
def page_order_details():
    page_header("🔍 Order Details", "Full order information, timeline and activity log")
    D = st.session_state.data

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  {r['current_status']}"
        for _,r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order", opts, key="od_sel")
    if sel == "— Select an order —":
        st.info("👆 Select an order to view its complete details.")
        show_footer(); return

    oid   = sel.split("  ·  ")[0].strip()
    order = get_order(oid)

    # ── Order header card ──
    s = order["current_status"]
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;
                box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:20px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;">
            <div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    {cobadge(order['company'])}
                    <span style="font-size:18px;font-weight:800;color:#0f172a;">{order['order_id']}</span>
                </div>
                <div style="font-size:13px;color:#64748b;">{order['po_number']} · {order['govt_department']}</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
                {sbadge(s)}
                {pbadge(order['priority'])}
            </div>
        </div>
        <div style="margin-top:16px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Contact</div><div style="font-size:13px;font-weight:600;">{order['contact_person']}</div></div>
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Phone</div><div style="font-size:13px;font-weight:600;">{order['contact_phone']}</div></div>
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Quantity</div><div style="font-size:13px;font-weight:600;">{order['quantity']}</div></div>
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Total Value</div><div style="font-size:16px;font-weight:800;color:#0f172a;">₹{float(order['total_value']):,.0f}</div></div>
        </div>
        <div style="margin-top:14px;padding:10px 14px;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0;">
            <span style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;">Description: </span>
            <span style="font-size:13px;color:#1e293b;">{order['item_description']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Pipeline stepper ──
    cur_idx = STATUSES.index(s) if s in STATUSES else 0
    step_html = '<div class="step-bar">'
    for i, step in enumerate(STATUSES):
        done  = i <= cur_idx
        nc    = "step-done" if done else "step-pending"
        lc    = STATUS_FG.get(step,"#94a3b8") if done else "#94a3b8"
        step_html += f'<div style="display:flex;flex-direction:column;align-items:center;">'
        step_html += f'<div class="step-node {nc}">{STATUS_EMOJI.get(step,"")}</div>'
        step_html += f'<div class="step-label" style="color:{lc};">{step}</div></div>'
        if i < len(STATUSES)-1:
            lclass = "step-line-d" if i < cur_idx else "step-line-p"
            step_html += f'<div class="{lclass}" style="margin-bottom:18px;"></div>'
    step_html += '</div>'
    st.markdown(step_html, unsafe_allow_html=True)

    # ── Sub-table tabs ──
    t1,t2,t3,t4,t5 = st.tabs(["🔧 Procurement","🚚 Dispatch","📦 Delivery","💰 Invoice","📋 Activity"])

    def show_record(table, oid):
        rows = D[table][D[table]["order_id"]==oid]
        if len(rows) == 0:
            st.info("No data recorded yet for this stage.")
            return
        row = rows.iloc[-1]
        cols_per_row = 3
        items = [(c.replace("_"," ").title(), str(row[c])) for c in row.index if c not in ["id","order_id"] and str(row[c]) not in ["","nan"]]
        for i in range(0, len(items), cols_per_row):
            chunk = items[i:i+cols_per_row]
            cs = st.columns(cols_per_row)
            for col,(label,val) in zip(cs,chunk):
                with col:
                    st.markdown(f"""
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:7px;padding:10px 14px;">
                        <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:4px;">{label}</div>
                        <div style="font-size:13px;font-weight:600;color:#0f172a;">{val}</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    with t1: show_record("procurement", oid)
    with t2: show_record("dispatch",    oid)
    with t3: show_record("delivery",    oid)
    with t4: show_record("invoices",    oid)
    with t5:
        logs = D["activity_log"][D["activity_log"]["order_id"]==oid].copy().iloc[::-1]
        if len(logs)==0:
            st.info("No activity recorded yet.")
        for _,log in logs.iterrows():
            prev = log.get("previous_status","")
            ns   = log.get("new_status","")
            arrow= f' <span style="color:#94a3b8;">→</span> {sbadge(ns)}' if ns and ns!="nan" else ""
            prev_b = sbadge(prev) if prev and prev not in ["—","nan",""] else f'<span style="color:#94a3b8;">—</span>'
            st.markdown(f"""
            <div class="log-entry">
                <div class="log-dot"></div>
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                            <span style="font-size:12px;font-weight:700;background:#f1f5f9;padding:2px 8px;border-radius:4px;">{log['action_type']}</span>
                            &nbsp; {prev_b}{arrow}
                        </div>
                        <span style="font-size:11px;color:#94a3b8;">{log['performed_at']}</span>
                    </div>
                    <div style="font-size:12.5px;color:#374151;margin-top:5px;">{log['details']} — by <b>{log['performed_by']}</b></div>
                </div>
            </div>""", unsafe_allow_html=True)

    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVITY LOG
# ═══════════════════════════════════════════════════════════════════════════════
def page_activity_log():
    page_header("📋 Activity Log", "Complete audit trail of all order changes and status updates")
    D    = st.session_state.data
    logs = D["activity_log"].copy().iloc[::-1].reset_index(drop=True)
    card_start(f"All Events", f"{len(logs)} total")
    for _,log in logs.iterrows():
        prev = log.get("previous_status",""); ns = log.get("new_status","")
        prev_b = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8;">—</span>'
        ns_b   = sbadge(ns)   if ns   and ns   not in ["nan",""]     else ""
        arrow  = ' → ' if ns_b else ""
        st.markdown(f"""
        <div class="log-entry">
            <div class="log-dot"></div>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                        <span style="font-size:12px;font-weight:700;background:#f1f5f9;padding:2px 8px;border-radius:4px;">{log['action_type']}</span>
                        <span style="font-size:12px;font-weight:700;color:#1d4ed8;">{log['order_id']}</span>
                        {prev_b}{arrow}{ns_b}
                    </div>
                    <span style="font-size:11px;color:#94a3b8;">{log['performed_at']}</span>
                </div>
                <div style="font-size:12.5px;color:#374151;margin-top:5px;">{log['details']} — by <b>{log['performed_by']}</b></div>
            </div>
        </div>""", unsafe_allow_html=True)
    card_end()
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# REPORTS
# ═══════════════════════════════════════════════════════════════════════════════
def page_reports():
    page_header("📈 Reports", "Financial summaries and order analytics by company and status")
    D      = st.session_state.data
    orders = D["orders"].copy()
    orders["total_value"] = orders["total_value"].astype(float)

    c1,c2 = st.columns(2)

    with c1:
        card_start("🏢 Orders by Company")
        for co in COMPANIES:
            rows = orders[orders["company"]==co]
            cnt  = len(rows); val = rows["total_value"].sum()
            pct  = cnt/max(len(orders),1)
            fg   = CO_FG.get(co,"#64748b"); bg = CO_BG.get(co,"#f1f5f9")
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                    <span class="co-tag" style="background:{bg};color:{fg};">{co}</span>
                    <span style="font-size:12px;font-weight:700;color:{fg};">{cnt} orders · ₹{val/100000:.1f}L</span>
                </div>
                <div style="background:#f1f5f9;border-radius:4px;height:6px;">
                    <div style="width:{int(pct*100)}%;background:{fg};border-radius:4px;height:6px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        card_end()

    with c2:
        card_start("📊 Orders by Status")
        for status in STATUSES:
            cnt = len(orders[orders["current_status"]==status])
            pct = cnt/max(len(orders),1)
            fg  = STATUS_FG.get(status,"#64748b"); bg = STATUS_BG.get(status,"#f1f5f9")
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                    <span class="badge" style="background:{bg};color:{fg};">{STATUS_EMOJI.get(status,"")} {status}</span>
                    <span style="font-size:13px;font-weight:700;color:{fg};">{cnt}</span>
                </div>
                <div style="background:#f1f5f9;border-radius:4px;height:6px;">
                    <div style="width:{int(pct*100)}%;background:{fg};border-radius:4px;height:6px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        card_end()

    # Financial table
    card_start("💵 Financial Summary")
    TH = "padding:9px 14px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;"
    TD = "padding:11px 14px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
    rows_html = ""
    for i,(_,r) in enumerate(orders.iterrows()):
        bg  = "#fff" if i%2==0 else "#fafbfc"
        tv  = float(r["total_value"])
        paid= f'<span style="color:#16a34a;font-weight:700;">₹{tv:,.0f}</span>' if r["current_status"]=="Paid" else '<span style="color:#94a3b8;">—</span>'
        out = '<span style="color:#94a3b8;">—</span>' if r["current_status"]=="Paid" else f'<span style="color:#d97706;font-weight:700;">₹{tv:,.0f}</span>'
        rows_html += f"""<tr style="background:{bg}">
            <td style="{TD}font-size:11.5px;color:#64748b;">{r['order_id']}</td>
            <td style="{TD}">{cobadge(r['company'])}</td>
            <td style="{TD}">{r['govt_department']}</td>
            <td style="{TD}font-weight:700;">₹{tv:,.0f}</td>
            <td style="{TD}">{sbadge(r['current_status'])}</td>
            <td style="{TD}">{paid}</td>
            <td style="{TD}">{out}</td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;">
        <thead><tr>
            <th style="{TH}">Order ID</th><th style="{TH}">Company</th>
            <th style="{TH}">Department</th><th style="{TH}">Total Value</th>
            <th style="{TH}">Status</th><th style="{TH}">Paid</th><th style="{TH}">Outstanding</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)
    card_end()
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN
# ═══════════════════════════════════════════════════════════════════════════════
def page_admin():
    page_header("⚙️ Admin Panel", "Data export, database stats, user management")
    D = st.session_state.data

    st.markdown("""
    <div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:13px;color:#1e40af;line-height:1.9;">
        ✅ <b>Auto-Save</b> — Every change saves instantly to CSV files on the server.<br>
        📥 <b>Export CSV</b> — Downloads directly to your computer's Downloads folder.<br>
        🔄 <b>Status</b> — Updates reflect immediately everywhere after saving.
    </div>""", unsafe_allow_html=True)

    card_start("📥 Export Data to CSV")
    tables = ["orders","procurement","dispatch","delivery","invoices","activity_log"]
    cols   = st.columns(3)
    for i,t in enumerate(tables):
        with cols[i%3]:
            csv = D[t].to_csv(index=False).encode("utf-8")
            st.download_button(f"📄 {t}  ({len(D[t])} rows)", csv,
                               f"supply_chain_{t}_{now_ist()[:10]}.csv","text/csv",
                               use_container_width=True, key=f"dl_{t}")
    st.markdown("<br>",unsafe_allow_html=True)
    all_csv = "\n\n".join([f"=== {t.upper()} ===\n" + D[t].to_csv(index=False) for t in tables])
    st.download_button("📦 Export ALL Tables (Single File)", all_csv.encode(),
                       f"supply_chain_full_{now_ist()[:10]}.csv", "text/csv",
                       use_container_width=True, key="dl_all", type="primary")
    card_end()

    card_start("⚙️ Database Statistics")
    cols2 = st.columns(6)
    for i,t in enumerate(tables):
        with cols2[i]:
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-top:3px solid #1d4ed8;
                        border-radius:8px;padding:12px 14px;text-align:center;">
                <div style="font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;">{t}</div>
                <div style="font-size:22px;font-weight:800;color:#1d4ed8;margin-top:6px;">{len(D[t])}</div>
                <div style="font-size:10px;color:#94a3b8;">rows</div>
            </div>""", unsafe_allow_html=True)
    card_end()

    card_start("👥 Users & Role Permissions")
    ROLE_DESC = {
        "Admin":   "Full access — create, update, reports, admin panel",
        "Manager": "Create orders, update all stages, view reports",
        "Staff":   "Update orders only — procurement / dispatch / delivery / invoice",
        "Viewer":  "Read-only — dashboard, order details, activity log",
    }
    TH = "padding:9px 14px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;"
    TD = "padding:11px 14px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
    rows_html = ""
    for i,(u,v) in enumerate(USERS.items()):
        bg = "#fff" if i%2==0 else "#fafbfc"
        rc = ROLE_COLOR.get(v['role'],"#64748b"); rb = ROLE_BG.get(v['role'],"#f1f5f9")
        rows_html += f"""<tr style="background:{bg}">
            <td style="{TD}font-weight:700;font-family:monospace;">{u}</td>
            <td style="{TD}">{v['name']}</td>
            <td style="{TD}"><span class="badge" style="background:{rb};color:{rc};">{v['role']}</span></td>
            <td style="{TD}font-size:12px;color:#64748b;">{ROLE_DESC.get(v['role'],'')}</td>
        </tr>"""
    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse;">
        <thead><tr>
            <th style="{TH}">Username</th><th style="{TH}">Name</th>
            <th style="{TH}">Role</th><th style="{TH}">Access Level</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)
    card_end()

    with st.expander("⚠️ Danger Zone — Reset Data"):
        st.warning("This will permanently delete all data and restore sample records.")
        if st.button("🗑 Reset All Data to Sample Data", type="primary", key="reset_data"):
            for key,df in SEED.items():
                df.astype(str).fillna("").to_csv(FILES[key],index=False)
            st.session_state.data = load_data()
            st.success("✅ Data has been reset to sample records.")
            st.rerun()

    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER — main entry point
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    render_sidebar()

    menu = st.session_state.menu
    PAGES = {
        "Dashboard":    page_dashboard,
        "New Order":    page_new_order,
        "Update Order": page_update_order,
        "Order Details":page_order_details,
        "Activity Log": page_activity_log,
        "Reports":      page_reports,
        "Admin":        page_admin,
    }

    # Guard: if user's role doesn't have access to current menu, redirect to Dashboard
    allowed = ROLE_MENUS.get(st.session_state.role, [])
    if menu not in allowed:
        st.session_state.menu = "Dashboard"
        st.rerun()

    if menu in PAGES:
        PAGES[menu]()

if __name__ == "__main__":
    main()
