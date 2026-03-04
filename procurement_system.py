import streamlit as st
import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# ══════════════════════════════════════════════════════
# PAGE CONFIG — must be FIRST streamlit call
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Supply Chain Tracking System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════
COMPANIES  = ["Robokart", "Bharat Tech", "EL"]
STATUSES   = ["Pending","Procured","Dispatched","Delivered","Invoiced","Paid"]
PRIORITIES = ["Low","Medium","High","Urgent"]

STATUS_EMOJI = {"Pending":"⏳","Procured":"🔧","Dispatched":"🚚","Delivered":"📦","Invoiced":"🧾","Paid":"💰"}
STATUS_BG    = {"Pending":"#fef3c7","Procured":"#dbeafe","Dispatched":"#ede9fe","Delivered":"#d1fae5","Invoiced":"#cffafe","Paid":"#dcfce7"}
STATUS_FG    = {"Pending":"#b45309","Procured":"#1d4ed8","Dispatched":"#6d28d9","Delivered":"#065f46","Invoiced":"#0e7490","Paid":"#15803d"}
PRIO_BG      = {"Low":"#f1f5f9","Medium":"#dbeafe","High":"#fef3c7","Urgent":"#fee2e2"}
PRIO_FG      = {"Low":"#475569","Medium":"#1d4ed8","High":"#b45309","Urgent":"#dc2626"}
CO_BG        = {"Robokart":"#ede9fe","Bharat Tech":"#cffafe","EL":"#ffedd5"}
CO_FG        = {"Robokart":"#6d28d9","Bharat Tech":"#0e7490","EL":"#c2410c"}

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

# ══════════════════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════════════════
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
FILES = {k: f"{DATA_DIR}/{k}.csv" for k in
         ["orders","procurement","dispatch","delivery","invoices","activity_log"]}

SEED = {
    "orders": pd.DataFrame([
        {"order_id":"ORD-2026-02-28-001","date_created":"2026-02-10 09:30:00","company":"Robokart",
         "govt_department":"Education Department Delhi","contact_person":"Mr. Rajesh Kumar",
         "contact_phone":"9876543210","po_number":"PO/EDU/2026/001",
         "item_description":"Robotics Kits for STEM Labs","quantity":50,"total_value":250000,
         "assigned_company":"Tech Solutions Pvt Ltd","current_status":"Dispatched","priority":"High",
         "expected_delivery_date":"2026-03-05","remarks":"","created_by":"Admin","last_updated":"2026-02-20 11:00:00"},
        {"order_id":"ORD-2026-02-28-002","date_created":"2026-02-12 10:15:00","company":"Bharat Tech",
         "govt_department":"Health Ministry Maharashtra","contact_person":"Dr. Priya Sharma",
         "contact_phone":"9123456789","po_number":"PO/HLT/2026/044",
         "item_description":"Medical IoT Devices & Sensors","quantity":200,"total_value":980000,
         "assigned_company":"BioTech India","current_status":"Pending","priority":"Urgent",
         "expected_delivery_date":"2026-03-10","remarks":"","created_by":"Admin","last_updated":"2026-02-12 10:15:00"},
        {"order_id":"ORD-2026-02-28-003","date_created":"2026-01-28 14:00:00","company":"EL",
         "govt_department":"Defence Research DRDO","contact_person":"Col. Vikram Singh",
         "contact_phone":"9000123456","po_number":"PO/DEF/2026/007",
         "item_description":"Surveillance Drone Components","quantity":10,"total_value":1500000,
         "assigned_company":"AeroDyne Systems","current_status":"Paid","priority":"Medium",
         "expected_delivery_date":"2026-02-20","remarks":"","created_by":"Admin","last_updated":"2026-02-25 16:30:00"},
        {"order_id":"ORD-2026-02-28-004","date_created":"2026-02-18 08:45:00","company":"Robokart",
         "govt_department":"Smart Cities Mission UP","contact_person":"Ms. Anita Verma",
         "contact_phone":"9988776655","po_number":"PO/SCM/2026/019",
         "item_description":"IoT Traffic Management System","quantity":30,"total_value":670000,
         "assigned_company":"Robokart Solutions","current_status":"Delivered","priority":"Medium",
         "expected_delivery_date":"2026-02-28","remarks":"","created_by":"Admin","last_updated":"2026-02-26 17:00:00"},
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
    D = st.session_state.data
    row = pd.DataFrame([{"id":str(len(D["activity_log"])+1),"order_id":order_id,
                         "action_type":action,"previous_status":prev,"new_status":new_s,
                         "performed_by":by,"performed_at":now_ist(),"details":details}])
    D["activity_log"] = pd.concat([D["activity_log"],row],ignore_index=True)
    save_table("activity_log")

def update_order_status(order_id, new_status):
    D = st.session_state.data
    D["orders"].loc[D["orders"]["order_id"]==order_id,"current_status"] = new_status
    D["orders"].loc[D["orders"]["order_id"]==order_id,"last_updated"]   = now_ist()
    save_table("orders")

def get_order(order_id):
    rows = st.session_state.data["orders"]
    r    = rows[rows["order_id"]==order_id]
    return r.iloc[0] if len(r) else None

# ══════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════
for k,v in [("logged_in",False),("username",""),("role",""),("user_name",""),
            ("menu","Dashboard"),("company_filter","All")]:
    if k not in st.session_state:
        st.session_state[k] = v
if "data" not in st.session_state:
    st.session_state.data = load_data()

# ══════════════════════════════════════════════════════
# MASTER CSS  — injected once, covers everything
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, .stApp, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background: #f1f5f9 !important;
    color: #1e293b !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }

/* ════════════════════════════════════
   SIDEBAR — always dark, always visible
   ════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    min-width: 240px !important;
    max-width: 240px !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    height: 100vh;
    display: flex;
    flex-direction: column;
}
/* All text in sidebar muted slate */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #94a3b8 !important;
}
/* Nav buttons — transparent base */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    padding: 10px 16px !important;
    margin: 1px 8px !important;
    width: calc(100% - 16px) !important;
    transition: background 0.15s, color 0.15s !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #e2e8f0 !important;
}
/* Active nav item */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #2563eb !important;
}
/* Sign-out button */
[data-testid="stSidebar"] .stButton:last-child > button {
    color: #f87171 !important;
    border: 1px solid #3f1515 !important;
    background: rgba(220,38,38,0.08) !important;
    margin-top: 4px !important;
}
[data-testid="stSidebar"] .stButton:last-child > button:hover {
    background: rgba(220,38,38,0.18) !important;
}

/* ════════════════════════════════════
   ALL INPUT FIELDS — white bg, dark text
   Works on login page AND app pages
   ════════════════════════════════════ */
input, textarea,
input[type="text"],
input[type="password"],
input[type="number"],
input[type="email"],
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
    font-family: 'Inter', sans-serif !important;
}
input::placeholder, textarea::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}
input:focus, textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    outline: none !important;
    background: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #111827 !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #111827 !important;
}

/* Number input wrapper */
.stNumberInput > div > div {
    background: #ffffff !important;
    border-radius: 8px !important;
}
/* Date input */
.stDateInput > div > div {
    background: #ffffff !important;
    border-radius: 8px !important;
}

/* Form field labels */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stNumberInput label, .stDateInput label, .stFileUploader label,
.stCheckbox label {
    font-size: 12.5px !important;
    font-weight: 600 !important;
    color: #374151 !important;
    letter-spacing: 0.01em !important;
}

/* ════════════════════════════════════
   BUTTONS (app-wide)
   ════════════════════════════════════ */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 9px 20px !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
    border: 1.5px solid transparent !important;
}
.stButton > button[kind="primary"] {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1e40af !important;
    border-color: #1e40af !important;
}
.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    color: #374151 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #cbd5e1 !important;
    background: #f8fafc !important;
}

/* ════════════════════════════════════
   TABS
   ════════════════════════════════════ */
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
    padding: 10px 22px !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    border-bottom: 2px solid #1d4ed8 !important;
    color: #1d4ed8 !important;
    font-weight: 700 !important;
}

/* ════════════════════════════════════
   PAGE TOP-BAR
   ════════════════════════════════════ */
.topbar {
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 14px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.topbar-title { font-size: 18px; font-weight: 800; color: #0f172a; }
.topbar-sub   { font-size: 12px; color: #64748b; margin-top: 2px; }
.topbar-right { display: flex; align-items: center; gap: 14px; }
.saved-pill   {
    display: flex; align-items: center; gap: 5px;
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 20px; padding: 4px 12px;
    font-size: 11.5px; font-weight: 600; color: #15803d;
}
.saved-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; }
.date-chip  { font-size: 12px; color: #64748b; font-weight: 500; }

/* ════════════════════════════════════
   METRIC CARDS
   ════════════════════════════════════ */
.mcard {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
}
.mcard-label {
    font-size: 10.5px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.8px; color: #64748b; margin-bottom: 10px;
}
.mcard-value { font-size: 28px; font-weight: 800; line-height: 1; }
.mcard-bar {
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 12px 12px 0 0;
}

/* ════════════════════════════════════
   TABLE CARD
   ════════════════════════════════════ */
.tcard {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.tcard-header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 20px;
    border-bottom: 1px solid #f1f5f9;
    background: #fafbfc;
}
.tcard-title { font-size: 14px; font-weight: 700; color: #0f172a; }
.tcard-badge {
    font-size: 11px; font-weight: 600; color: #64748b;
    background: #f1f5f9; padding: 3px 12px; border-radius: 20px;
}
.otable { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.otable th {
    padding: 10px 16px; background: #f8fafc;
    font-size: 10.5px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.5px; color: #475569;
    border-bottom: 2px solid #e2e8f0; text-align: left; white-space: nowrap;
}
.otable td {
    padding: 13px 16px; border-bottom: 1px solid #f1f5f9;
    color: #1e293b; vertical-align: middle;
}

/* ════════════════════════════════════
   BADGES
   ════════════════════════════════════ */
.badge {
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    font-size: 11px; font-weight: 700; white-space: nowrap;
}
.co-tag {
    display: inline-block; padding: 3px 10px; border-radius: 6px;
    font-size: 11px; font-weight: 700;
}

/* ════════════════════════════════════
   FORM CARD
   ════════════════════════════════════ */
.form-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 20px;
    max-width: 860px;
}
.form-card-header {
    padding: 16px 24px;
    border-bottom: 1px solid #f1f5f9;
    background: #fafbfc;
}
.form-card-title { font-size: 14px; font-weight: 700; color: #0f172a; }
.form-card-sub   { font-size: 12px; color: #64748b; margin-top: 3px; }
.form-card-body  { padding: 24px; }

/* ════════════════════════════════════
   SECTION LABEL
   ════════════════════════════════════ */
.section-label {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.8px; color: #94a3b8;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 8px; margin-bottom: 16px; margin-top: 8px;
}

/* ════════════════════════════════════
   LOG / TIMELINE
   ════════════════════════════════════ */
.log-row {
    display: flex; gap: 12px; align-items: flex-start;
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 13px 16px; margin-bottom: 8px;
}
.log-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: #3b82f6; flex-shrink: 0; margin-top: 4px;
}

/* ════════════════════════════════════
   INFO ROW (order details)
   ════════════════════════════════════ */
.info-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr));
    gap: 14px; background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 16px; margin-bottom: 18px;
}
.info-lbl { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; margin-bottom: 5px; }
.info-val { font-size: 13.5px; font-weight: 600; color: #0f172a; }

/* ════════════════════════════════════
   PIPELINE STEPPER
   ════════════════════════════════════ */
.stepper { display: flex; align-items: center; margin: 0 0 22px; }
.step-node {
    display: flex; flex-direction: column; align-items: center; flex-shrink: 0;
}
.step-circle {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700;
}
.step-done    { background: #1d4ed8; color: #fff; }
.step-current { background: #dbeafe; color: #1d4ed8; border: 2px solid #1d4ed8; }
.step-pending { background: #f1f5f9; color: #94a3b8; }
.step-lbl { font-size: 9.5px; font-weight: 600; color: #64748b; margin-top: 5px; text-align: center; }
.step-line { flex:1; height: 2px; margin: 0 4px; margin-bottom: 18px; }
.step-line-done { background: #1d4ed8; }
.step-line-pending { background: #e2e8f0; }

/* ════════════════════════════════════
   FOOTER
   ════════════════════════════════════ */
.sc-footer {
    text-align: center; font-size: 11px; color: #94a3b8;
    padding: 18px 0 10px; border-top: 1px solid #e2e8f0; margin-top: 36px;
}

/* ════════════════════════════════════
   ALERTS
   ════════════════════════════════════ */
.stAlert { border-radius: 8px !important; }
.stSuccess, .stError, .stInfo, .stWarning { border-radius: 8px !important; }

/* ════════════════════════════════════
   EXPANDER
   ════════════════════════════════════ */
.streamlit-expanderHeader {
    background: #f8fafc !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 13px !important;
}

hr { border-color: #e2e8f0 !important; margin: 14px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# BADGE HELPERS
# ══════════════════════════════════════════════════════
def sbadge(s):
    bg = STATUS_BG.get(s,"#f1f5f9"); fg = STATUS_FG.get(s,"#64748b")
    return f'<span class="badge" style="background:{bg};color:{fg};">{STATUS_EMOJI.get(s,"")} {s}</span>'

def pbadge(p):
    bg = PRIO_BG.get(p,"#f1f5f9"); fg = PRIO_FG.get(p,"#64748b")
    return f'<span class="badge" style="background:{bg};color:{fg};">{p}</span>'

def cobadge(c):
    bg = CO_BG.get(c,"#f1f5f9"); fg = CO_FG.get(c,"#64748b")
    return f'<span class="co-tag" style="background:{bg};color:{fg};">{c}</span>'

def topbar(title, subtitle=""):
    today = datetime.now().strftime("%d %b %Y")
    sub   = f'<div class="topbar-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="topbar">
        <div><div class="topbar-title">{title}</div>{sub}</div>
        <div class="topbar-right">
            <div class="saved-pill"><div class="saved-dot"></div>Auto-saved</div>
            <div class="date-chip">📅 {today}</div>
        </div>
    </div>
    <div style="height:24px;"></div>
    """, unsafe_allow_html=True)

def show_footer():
    st.markdown(
        f'<div class="sc-footer">© {datetime.now().year} Robokart &nbsp;·&nbsp; '
        f'Supply Chain Tracking System &nbsp;·&nbsp; All rights reserved.</div>',
        unsafe_allow_html=True)

def section_label(text):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

def sp(px=12):
    st.markdown(f'<div style="height:{px}px"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════
def login_page():
    # Override entire background to dark gradient; hide sidebar
    st.markdown("""
    <style>
    html, body, .stApp {
        background: linear-gradient(135deg,#0c1426 0%,#1e3a5f 50%,#0c1426 100%) !important;
    }
    [data-testid="stSidebar"] { display: none !important; }
    .block-container { padding: 0 !important; }
    section.main > div { padding: 0 !important; }

    /* ── Override inputs specifically for login card ── */
    .login-form-area input[type="text"],
    .login-form-area input[type="password"],
    .login-form-area input {
        background: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        caret-color: #111827 !important;
        border: 1.5px solid #d1d5db !important;
        border-radius: 8px !important;
        height: 48px !important;
        font-size: 14px !important;
    }
    .login-form-area label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Vertical centering
    st.markdown('<div style="min-height:80px"></div>', unsafe_allow_html=True)

    # 3-col centering
    _, col, _ = st.columns([1, 1.2, 1])
    with col:

        # ── Branding header (pure HTML above form) ──
        st.markdown("""
        <div style="
            background:#fff;
            border-radius:14px 14px 0 0;
            border:1px solid #e2e8f0;
            border-bottom:none;
            padding:38px 36px 26px;
            text-align:center;
        ">
            <div style="
                width:72px;height:72px;border-radius:16px;
                background:linear-gradient(135deg,#1e3a5f,#1d4ed8);
                display:flex;align-items:center;justify-content:center;
                font-size:34px;margin:0 auto 16px;
                box-shadow:0 4px 14px rgba(29,78,216,0.3);
            ">🏭</div>
            <div style="font-size:20px;font-weight:800;color:#0f172a;">Supply Chain Tracking System</div>
            <div style="font-size:13px;color:#64748b;margin-top:8px;">
                Enterprise Procurement &amp; Order Management
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Form bottom half of card ──
        st.markdown("""
        <div style="
            background:#fff;
            border-radius:0 0 14px 14px;
            border:1px solid #e2e8f0;
            border-top:1px solid #f1f5f9;
            padding:28px 36px 32px;
            box-shadow:0 20px 50px rgba(0,0,0,0.35);
        ">
            <div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:18px;">
                Sign in to your account
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Streamlit form — NOT wrapped in any HTML div
        with st.form("login_form"):
            uname = st.text_input("Username", placeholder="Enter your username")
            passw = st.text_input("Password", type="password", placeholder="Enter your password")
            sp(8)
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

        if submitted:
            if uname in USERS and USERS[uname]["password"] == passw:
                st.session_state.logged_in = True
                st.session_state.username  = uname
                st.session_state.role      = USERS[uname]["role"]
                st.session_state.user_name = USERS[uname]["name"]
                st.session_state.menu      = "Dashboard"
                st.rerun()
            else:
                st.error("⚠ Invalid credentials. Please check username and password.")

        st.markdown("""
        <p style="text-align:center;font-size:12px;color:#94a3b8;margin-top:18px;">
            🔒 Secure access · Contact admin for credentials
        </p>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        # ── Logo ──
        st.markdown("""
        <div style="padding:22px 16px 18px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="
                    width:36px;height:36px;border-radius:8px;
                    background:linear-gradient(135deg,#1e3a5f,#1d4ed8);
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;flex-shrink:0;">🏭</div>
                <div>
                    <div style="font-size:14px;font-weight:800;color:#f8fafc;">Supply Chain</div>
                    <div style="font-size:9px;color:#475569;letter-spacing:1.2px;text-transform:uppercase;">Tracking System</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        sp(10)

        # ── Nav label ──
        st.markdown('<div style="padding:0 16px;font-size:9.5px;font-weight:700;letter-spacing:1.2px;color:#334155;text-transform:uppercase;margin-bottom:4px;">Navigation</div>', unsafe_allow_html=True)

        # ── Nav buttons ──
        menus = ROLE_MENUS.get(st.session_state.role, [])
        for m in menus:
            is_active = (st.session_state.menu == m)
            icon      = MENU_ICONS.get(m, "")
            btn_type  = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {m}", key=f"nav_{m}",
                         use_container_width=True, type=btn_type):
                st.session_state.menu = m
                st.rerun()

        sp(12)
        st.markdown('<div style="height:1px;background:#1e293b;margin:0 16px;"></div>', unsafe_allow_html=True)
        sp(12)

        # ── User card ──
        role = st.session_state.role
        rc   = ROLE_COLOR.get(role,"#64748b")
        rb   = ROLE_BG.get(role,"#1e293b")
        initials = "".join([x[0].upper() for x in st.session_state.user_name.split()[:2]])
        st.markdown(f"""
        <div style="padding:0 16px;margin-bottom:10px;">
            <div style="background:#1e293b;border-radius:10px;padding:12px 14px;
                        display:flex;align-items:center;gap:10px;">
                <div style="
                    width:36px;height:36px;border-radius:8px;
                    background:{rc};color:#fff;
                    display:flex;align-items:center;justify-content:center;
                    font-size:13px;font-weight:800;flex-shrink:0;">{initials}</div>
                <div style="flex:1;overflow:hidden;">
                    <div style="font-size:12.5px;font-weight:700;color:#f1f5f9;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                        {st.session_state.user_name}
                    </div>
                    <span style="font-size:10px;font-weight:700;
                                 background:{rb};color:{rc};
                                 padding:1px 8px;border-radius:4px;">{role}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Sign Out", use_container_width=True, key="signout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        sp(16)

# ══════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════
def page_dashboard():
    topbar("📊 Dashboard", "Real-time overview of all purchase orders and supply chain status")

    D      = st.session_state.data
    orders = D["orders"].copy()
    cf     = st.session_state.company_filter
    fil    = orders if cf == "All" else orders[orders["company"] == cf]
    total_val = fil["total_value"].astype(float).sum() if len(fil) else 0.0

    pad = "padding:0 28px;"

    # ── KPI cards ──
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)
    metrics = [
        ("Total Orders",  len(fil),                                                               "#1d4ed8"),
        ("Pending",       len(fil[fil["current_status"]=="Pending"]),                             "#d97706"),
        ("In Transit",    len(fil[fil["current_status"].isin(["Procured","Dispatched"])]),        "#6d28d9"),
        ("Delivered",     len(fil[fil["current_status"].isin(["Delivered","Invoiced","Paid"])]),  "#059669"),
        ("Paid",          len(fil[fil["current_status"]=="Paid"]),                                "#0891b2"),
        ("Total Value",   f"₹{total_val/100000:.1f}L",                                           "#c2410c"),
    ]
    cols = st.columns(6)
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="mcard">
                <div class="mcard-bar" style="background:{color};"></div>
                <div class="mcard-label">{label}</div>
                <div class="mcard-value" style="color:{color};">{value}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    sp(20)

    # ── Company filter ──
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4, _ = st.columns([1.5, 1, 1.3, 0.8, 3])
    for col, label, key in [
        (fc1, "🏢 All Companies", "All"),
        (fc2, "Robokart",        "Robokart"),
        (fc3, "Bharat Tech",     "Bharat Tech"),
        (fc4, "EL",              "EL"),
    ]:
        with col:
            active = cf == key
            lbl    = label + (" ✓" if active else "")
            if st.button(lbl, key=f"cf_{key}",
                         type="primary" if active else "secondary",
                         use_container_width=True):
                st.session_state.company_filter = key
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    sp(18)

    # ── Orders table ──
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)
    title_label = "All Orders" if cf == "All" else f"{cf} Orders"

    TH = ("padding:11px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
          "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
          "border-bottom:2px solid #e2e8f0;text-align:left;white-space:nowrap;")
    TD = "padding:13px 16px;border-bottom:1px solid #f1f5f9;color:#1e293b;vertical-align:middle;"

    if len(fil) == 0:
        tbody = '<tr><td colspan="10" style="padding:32px;text-align:center;color:#94a3b8;font-size:13px;">No orders found.</td></tr>'
    else:
        tbody = ""
        for i, (_, r) in enumerate(fil.iterrows()):
            bg   = "#ffffff" if i % 2 == 0 else "#fafbfc"
            desc = str(r["item_description"])
            desc = desc[:42] + "…" if len(desc) > 42 else desc
            tbody += f"""<tr style="background:{bg}">
                <td style="{TD}font-weight:700;color:#1d4ed8;font-size:12px;white-space:nowrap;">{r['order_id']}</td>
                <td style="{TD}">{cobadge(r['company'])}</td>
                <td style="{TD}color:#64748b;font-size:12px;">{r['po_number']}</td>
                <td style="{TD}font-size:12.5px;">{r['govt_department']}</td>
                <td style="{TD}color:#374151;font-size:12.5px;">{desc}</td>
                <td style="{TD}text-align:center;font-weight:600;">{r['quantity']}</td>
                <td style="{TD}font-weight:700;white-space:nowrap;">₹{float(r['total_value']):,.0f}</td>
                <td style="{TD}">{pbadge(r['priority'])}</td>
                <td style="{TD}">{sbadge(r['current_status'])}</td>
                <td style="{TD}color:#94a3b8;font-size:11.5px;white-space:nowrap;">{r['last_updated']}</td>
            </tr>"""

    st.markdown(f"""
    <div class="tcard">
        <div class="tcard-header">
            <div class="tcard-title">📦 {title_label}</div>
            <div class="tcard-badge">{len(fil)} orders</div>
        </div>
        <div style="overflow-x:auto;">
        <table class="otable">
            <thead><tr>
                <th style="{TH}">Order ID</th>
                <th style="{TH}">Company</th>
                <th style="{TH}">PO Number</th>
                <th style="{TH}">Department</th>
                <th style="{TH}">Description</th>
                <th style="{TH}">Qty</th>
                <th style="{TH}">Value</th>
                <th style="{TH}">Priority</th>
                <th style="{TH}">Status</th>
                <th style="{TH}">Last Updated</th>
            </tr></thead>
            <tbody>{tbody}</tbody>
        </table></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    sp(8)
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)
    show_footer()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# NEW ORDER
# ══════════════════════════════════════════════════════
def page_new_order():
    topbar("➕ New Order", "Create a new government purchase order")
    D   = st.session_state.data
    pad = "padding:0 28px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    st.markdown("""
    <div class="form-card">
        <div class="form-card-header">
            <div class="form-card-title">📝 Purchase Order Details</div>
            <div class="form-card-sub">Fill all required fields marked with *</div>
        </div>
        <div class="form-card-body">
    """, unsafe_allow_html=True)

    with st.form("new_order_form", clear_on_submit=True):
        section_label("Company & Department")
        c1, c2 = st.columns(2)
        with c1:
            company   = st.selectbox("Company *", COMPANIES)
        with c2:
            priority  = st.selectbox("Priority *", PRIORITIES, index=1)

        c3, c4 = st.columns(2)
        with c3:
            govt_dept = st.text_input("Govt Department *", placeholder="e.g. Education Department Delhi")
        with c4:
            po_number = st.text_input("PO Number *", placeholder="e.g. PO/EDU/2026/001")

        sp(4)
        section_label("Contact Information")
        c5, c6 = st.columns(2)
        with c5:
            contact_name = st.text_input("Contact Person *", placeholder="e.g. Mr. Rajesh Kumar")
        with c6:
            contact_ph   = st.text_input("Contact Phone", placeholder="e.g. 9876543210")

        sp(4)
        section_label("Order Details")
        c7, c8 = st.columns(2)
        with c7:
            quantity    = st.number_input("Quantity *", min_value=1, value=1)
            total_value = st.number_input("Total Value (₹) *", min_value=0, value=0)
        with c8:
            assigned_co  = st.text_input("Assigned Company", placeholder="e.g. Tech Solutions Pvt Ltd")
            exp_delivery = st.date_input("Expected Delivery Date")

        item_desc = st.text_area("Item Description *",
                                  placeholder="Detailed description of goods/services to be procured…", height=90)
        remarks   = st.text_area("Remarks / Special Instructions",
                                  placeholder="Any additional notes…", height=68)

        sp(8)
        sub_col, _ = st.columns([1, 2])
        with sub_col:
            submitted = st.form_submit_button("🚀 Create Purchase Order", type="primary", use_container_width=True)

        if submitted:
            errors = [f for f, v in [("Govt Dept", govt_dept), ("PO Number", po_number),
                                       ("Contact Person", contact_name), ("Item Description", item_desc),
                                       ("Total Value", total_value)] if not v]
            if errors:
                st.error(f"Please fill required fields: {', '.join(errors)}")
            elif po_number in D["orders"]["po_number"].values:
                st.error("⚠ PO Number already exists in the system.")
            else:
                ts = now_ist()
                oid = f"ORD-{ts[:10]}-{str(len(D['orders'])+1).zfill(3)}"
                new_row = pd.DataFrame([{
                    "order_id":oid,"date_created":ts,"company":company,
                    "govt_department":govt_dept,"contact_person":contact_name,
                    "contact_phone":contact_ph,"po_number":po_number,
                    "item_description":item_desc,"quantity":str(quantity),
                    "total_value":str(total_value),"assigned_company":assigned_co,
                    "current_status":"Pending","priority":priority,
                    "expected_delivery_date":str(exp_delivery),
                    "remarks":remarks,"created_by":st.session_state.user_name,"last_updated":ts
                }])
                D["orders"] = pd.concat([D["orders"], new_row], ignore_index=True)
                save_table("orders")
                add_log(oid,"ORDER_CREATED","—","Pending",st.session_state.user_name,
                        f"Order created for {company} — {po_number}")
                st.success(f"✅ Order **{oid}** created successfully!")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════
# UPDATE ORDER
# ══════════════════════════════════════════════════════
def page_update_order():
    topbar("🔄 Update Order", "Update procurement, dispatch, delivery or invoice status")
    D   = st.session_state.data
    pad = "padding:0 28px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  [{r['current_status']}]"
        for _, r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order *", opts, key="uo_sel")

    if sel == "— Select an order —":
        st.info("👆 Select an order from the dropdown above to update its status.")
        st.markdown('</div>', unsafe_allow_html=True)
        show_footer(); return

    oid   = sel.split("  ·  ")[0].strip()
    order = get_order(oid)

    # Order summary bar
    st.markdown(f"""
    <div class="info-grid">
        <div><div class="info-lbl">Order ID</div>
             <div class="info-val" style="color:#1d4ed8;">{order['order_id']}</div></div>
        <div><div class="info-lbl">Company</div>
             <div class="info-val">{cobadge(order['company'])}</div></div>
        <div><div class="info-lbl">Status</div>
             <div class="info-val">{sbadge(order['current_status'])}</div></div>
        <div><div class="info-lbl">Priority</div>
             <div class="info-val">{pbadge(order['priority'])}</div></div>
        <div><div class="info-lbl">Value</div>
             <div class="info-val" style="font-weight:800;">₹{float(order['total_value']):,.0f}</div></div>
        <div><div class="info-lbl">Department</div>
             <div class="info-val">{order['govt_department']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    updated_by = st.text_input("Your Name / Department *",
                                placeholder="e.g. Rahul — Logistics Team", key="uo_by")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧  Procurement", "🚚  Dispatch", "📦  Delivery", "💰  Invoice & Payment"
    ])

    # ── Procurement ──
    with tab1:
        st.markdown('<div class="form-card" style="max-width:720px;">'
                    '<div class="form-card-header"><div class="form-card-title">Procurement Details</div></div>'
                    '<div class="form-card-body">', unsafe_allow_html=True)
        with st.form("proc_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_status = st.selectbox("Status *", ["","Not Started","In Progress","Completed","On Hold"])
                p_date   = st.date_input("Procurement Date")
            with c2:
                p_qc     = st.selectbox("Quality Check", ["","Pending","In Progress","Passed","Failed"])
                p_source = st.text_input("Materials Source", placeholder="Vendor / Warehouse name")
            p_notes = st.text_area("Notes", height=80)
            sv = st.form_submit_button("✅ Save Procurement Update", type="primary")
            if sv:
                if not updated_by:
                    st.error("Enter your name above the tabs first.")
                else:
                    ts = now_ist()
                    D["procurement"] = pd.concat([D["procurement"], pd.DataFrame([{
                        "id":str(len(D["procurement"])+1),"order_id":oid,
                        "procurement_status":p_status,"procurement_date":str(p_date),
                        "materials_source":p_source,"quality_check_status":p_qc,
                        "notes":p_notes,"updated_by":updated_by,"updated_at":ts
                    }])], ignore_index=True)
                    save_table("procurement")
                    ns = "Procured" if p_status == "Completed" else order["current_status"]
                    prev = order["current_status"]
                    update_order_status(oid, ns)
                    add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,f"Procurement: {p_status}")
                    st.success(f"✅ Saved! Order status → **{ns}**")
                    st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Dispatch ──
    with tab2:
        st.markdown('<div class="form-card" style="max-width:720px;">'
                    '<div class="form-card-header"><div class="form-card-title">Dispatch Details</div></div>'
                    '<div class="form-card-body">', unsafe_allow_html=True)
        with st.form("disp_form"):
            c1, c2 = st.columns(2)
            with c1:
                d_date    = st.date_input("Dispatch Date")
                d_courier = st.text_input("Courier / Transporter *", placeholder="e.g. BlueDart, DTDC")
                d_vehicle = st.text_input("Vehicle Number", placeholder="e.g. DL01AB1234")
            with c2:
                d_driver  = st.text_input("Driver Contact", placeholder="e.g. 9111222333")
                d_track   = st.text_input("Tracking Number", placeholder="e.g. BD123456789")
                d_expd    = st.date_input("Expected Delivery")
            sv = st.form_submit_button("✅ Save Dispatch Update", type="primary")
            if sv:
                if not updated_by:
                    st.error("Enter your name above the tabs first.")
                else:
                    ts = now_ist()
                    D["dispatch"] = pd.concat([D["dispatch"], pd.DataFrame([{
                        "id":str(len(D["dispatch"])+1),"order_id":oid,
                        "dispatch_date":str(d_date),"courier_name":d_courier,
                        "vehicle_number":d_vehicle,"driver_contact":d_driver,
                        "tracking_number":d_track,"expected_delivery_date":str(d_expd),
                        "updated_by":updated_by,"updated_at":ts
                    }])], ignore_index=True)
                    save_table("dispatch")
                    prev = order["current_status"]
                    update_order_status(oid, "Dispatched")
                    add_log(oid,"STATUS_CHANGE",prev,"Dispatched",updated_by,f"Dispatched via {d_courier}")
                    st.success("✅ Dispatch saved! Status → **Dispatched**")
                    st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Delivery ──
    with tab3:
        st.markdown('<div class="form-card" style="max-width:720px;">'
                    '<div class="form-card-header"><div class="form-card-title">Delivery Confirmation</div></div>'
                    '<div class="form-card-body">', unsafe_allow_html=True)
        with st.form("del_form"):
            c1, c2 = st.columns(2)
            with c1:
                de_status = st.selectbox("Delivery Status *", ["","Delivered","Partial","Failed","Rescheduled"])
                de_date   = st.date_input("Delivery Date")
                de_recv   = st.text_input("Receiver Name", placeholder="Person who received goods")
            with c2:
                de_qty = st.number_input("Delivered Quantity", min_value=0)
                de_ch  = st.text_input("Challan Number", placeholder="e.g. CH-EDU-001")
            st.markdown("**Delivery Proof Files** *(photos, PDFs)*")
            del_f = st.file_uploader("Upload", accept_multiple_files=True, key="dlf", label_visibility="collapsed")
            st.markdown("**Challan Documents**")
            ch_f  = st.file_uploader("Upload", accept_multiple_files=True, key="chf", label_visibility="collapsed")
            sv = st.form_submit_button("✅ Save Delivery Update", type="primary")
            if sv:
                if not updated_by:
                    st.error("Enter your name above the tabs first.")
                else:
                    ts = now_ist()
                    D["delivery"] = pd.concat([D["delivery"], pd.DataFrame([{
                        "id":str(len(D["delivery"])+1),"order_id":oid,
                        "delivery_status":de_status,"delivery_date":str(de_date),
                        "receiver_name":de_recv,"delivered_quantity":str(de_qty),
                        "challan_number":de_ch,
                        "delivery_files":f"{len(del_f or [])} file(s)",
                        "challan_files":f"{len(ch_f or [])} file(s)",
                        "updated_by":updated_by,"updated_at":ts
                    }])], ignore_index=True)
                    save_table("delivery")
                    ns = "Delivered" if de_status == "Delivered" else order["current_status"]
                    prev = order["current_status"]
                    update_order_status(oid, ns)
                    add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,
                            f"Delivery: {de_status} | {len(del_f or [])+len(ch_f or [])} files")
                    st.success(f"✅ Delivery saved! Status → **{ns}**")
                    st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Invoice ──
    with tab4:
        st.markdown('<div class="form-card" style="max-width:720px;">'
                    '<div class="form-card-header"><div class="form-card-title">Invoice &amp; Payment Details</div></div>'
                    '<div class="form-card-body">', unsafe_allow_html=True)
        with st.form("inv_form"):
            c1, c2 = st.columns(2)
            with c1:
                i_num    = st.text_input("Invoice Number", placeholder="e.g. INV-2026-0001")
                i_date   = st.date_input("Invoice Date")
                i_amount = st.number_input("Invoice Amount (₹)", min_value=0)
                i_pstat  = st.selectbox("Payment Status *", ["","Pending","Approved","Completed"])
            with c2:
                i_pmode  = st.selectbox("Payment Mode", ["","NEFT","RTGS","Cheque","DD","Online","Cash"])
                i_txn    = st.text_input("Transaction Reference", placeholder="TXN or UTR number")
                i_pdate  = st.date_input("Payment Date")
            st.markdown("**Invoice Documents** *(PDF, Excel, scanned copies)*")
            inv_f = st.file_uploader("Upload", accept_multiple_files=True, key="ivf", label_visibility="collapsed")
            sv = st.form_submit_button("✅ Save Invoice & Payment", type="primary")
            if sv:
                if not updated_by:
                    st.error("Enter your name above the tabs first.")
                else:
                    ts = now_ist()
                    D["invoices"] = pd.concat([D["invoices"], pd.DataFrame([{
                        "id":str(len(D["invoices"])+1),"order_id":oid,
                        "invoice_number":i_num,"invoice_date":str(i_date),
                        "invoice_amount":str(i_amount),"payment_status":i_pstat,
                        "payment_date":str(i_pdate),"payment_mode":i_pmode,
                        "transaction_reference":i_txn,
                        "invoice_files":f"{len(inv_f or [])} file(s)",
                        "updated_by":updated_by,"updated_at":ts
                    }])], ignore_index=True)
                    save_table("invoices")
                    ns = "Paid" if i_pstat == "Completed" else "Invoiced"
                    prev = order["current_status"]
                    update_order_status(oid, ns)
                    add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,
                            f"Invoice {i_num} | {i_pstat} | {len(inv_f or [])} files")
                    st.success(f"✅ Invoice saved! Status → **{ns}**")
                    st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════
# ORDER DETAILS
# ══════════════════════════════════════════════════════
def page_order_details():
    topbar("🔍 Order Details", "Full order information, timeline and activity log")
    D   = st.session_state.data
    pad = "padding:0 28px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  {r['current_status']}"
        for _, r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order", opts, key="od_sel")
    if sel == "— Select an order —":
        st.info("👆 Select an order above to view its complete details and history.")
        st.markdown('</div>', unsafe_allow_html=True); show_footer(); return

    oid   = sel.split("  ·  ")[0].strip()
    order = get_order(oid)
    s     = order["current_status"]

    # ── Header card ──
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                padding:22px 24px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:18px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
            <div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:7px;">
                    {cobadge(order['company'])}
                    <span style="font-size:18px;font-weight:800;color:#0f172a;">{order['order_id']}</span>
                </div>
                <div style="font-size:13px;color:#64748b;">
                    {order['po_number']} &nbsp;·&nbsp; {order['govt_department']}
                </div>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                {sbadge(s)} {pbadge(order['priority'])}
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
                    gap:14px;margin-top:18px;padding-top:16px;border-top:1px solid #f1f5f9;">
            <div><div class="info-lbl">Contact</div><div class="info-val">{order['contact_person']}</div></div>
            <div><div class="info-lbl">Phone</div><div class="info-val">{order['contact_phone']}</div></div>
            <div><div class="info-lbl">Quantity</div><div class="info-val">{order['quantity']}</div></div>
            <div><div class="info-lbl">Assigned To</div><div class="info-val">{order['assigned_company'] or '—'}</div></div>
            <div><div class="info-lbl">Total Value</div>
                 <div class="info-val" style="font-size:17px;color:#0f172a;font-weight:800;">
                     ₹{float(order['total_value']):,.0f}</div></div>
        </div>
        <div style="margin-top:14px;background:#f8fafc;border-radius:7px;
                    border:1px solid #e2e8f0;padding:11px 14px;">
            <span style="font-size:10px;font-weight:700;text-transform:uppercase;
                         color:#64748b;letter-spacing:0.5px;">Description: </span>
            <span style="font-size:13px;color:#1e293b;">{order['item_description']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Pipeline stepper ──
    cur_idx = STATUSES.index(s) if s in STATUSES else 0
    step_html = '<div class="stepper">'
    for i, step in enumerate(STATUSES):
        if i < cur_idx:
            nc = "step-done"; lc = "#1d4ed8"
        elif i == cur_idx:
            nc = "step-current"; lc = "#1d4ed8"
        else:
            nc = "step-pending"; lc = "#94a3b8"
        step_html += f"""<div class="step-node">
            <div class="step-circle {nc}">{STATUS_EMOJI.get(step,"")}</div>
            <div class="step-lbl" style="color:{lc};">{step}</div>
        </div>"""
        if i < len(STATUSES) - 1:
            lc2 = "step-line-done" if i < cur_idx else "step-line-pending"
            step_html += f'<div class="step-line {lc2}"></div>'
    step_html += "</div>"
    st.markdown(step_html, unsafe_allow_html=True)

    # ── Sub-record tabs ──
    def show_record(table, oid_filter):
        rows = D[table][D[table]["order_id"] == oid_filter]
        if len(rows) == 0:
            st.info("No data recorded yet for this stage.")
            return
        row = rows.iloc[-1]
        items = [(c.replace("_"," ").title(), str(row[c]))
                 for c in row.index
                 if c not in ["id","order_id"] and str(row[c]) not in ["","nan"]]
        for i in range(0, len(items), 3):
            chunk = items[i:i+3]
            cs    = st.columns(3)
            for col, (lbl, val) in zip(cs, chunk):
                with col:
                    st.markdown(f"""
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
                                padding:11px 14px;margin-bottom:10px;">
                        <div class="info-lbl">{lbl}</div>
                        <div class="info-val">{val}</div>
                    </div>""", unsafe_allow_html=True)

    t1,t2,t3,t4,t5 = st.tabs(["🔧 Procurement","🚚 Dispatch","📦 Delivery","💰 Invoice","📋 Activity"])
    with t1: show_record("procurement", oid)
    with t2: show_record("dispatch",    oid)
    with t3: show_record("delivery",    oid)
    with t4: show_record("invoices",    oid)
    with t5:
        logs = D["activity_log"][D["activity_log"]["order_id"]==oid].copy().iloc[::-1]
        if len(logs) == 0:
            st.info("No activity recorded yet.")
        for _, log in logs.iterrows():
            prev = log.get("previous_status",""); ns_l = log.get("new_status","")
            prev_b = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8">—</span>'
            ns_b   = ("&nbsp;→&nbsp;" + sbadge(ns_l)) if ns_l and ns_l not in ["nan",""] else ""
            st.markdown(f"""
            <div class="log-row">
                <div class="log-dot"></div>
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">
                        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                            <span style="font-size:11.5px;font-weight:700;background:#f1f5f9;
                                         padding:2px 8px;border-radius:5px;">{log['action_type']}</span>
                            {prev_b}{ns_b}
                        </div>
                        <span style="font-size:11px;color:#94a3b8;">{log['performed_at']}</span>
                    </div>
                    <div style="font-size:12.5px;color:#374151;margin-top:5px;">
                        {log['details']} — <b>{log['performed_by']}</b>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════
# ACTIVITY LOG
# ══════════════════════════════════════════════════════
def page_activity_log():
    topbar("📋 Activity Log", "Complete audit trail of all order changes and status updates")
    D   = st.session_state.data
    pad = "padding:0 28px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)
    logs = D["activity_log"].copy().iloc[::-1].reset_index(drop=True)

    st.markdown(f"""
    <div class="tcard" style="margin-bottom:20px;">
        <div class="tcard-header">
            <div class="tcard-title">📋 All System Events</div>
            <div class="tcard-badge">{len(logs)} events</div>
        </div>
        <div style="padding:16px;">
    """, unsafe_allow_html=True)

    for _, log in logs.iterrows():
        prev = log.get("previous_status",""); ns_l = log.get("new_status","")
        prev_b = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8">—</span>'
        ns_b   = ("&nbsp;→&nbsp;" + sbadge(ns_l)) if ns_l and ns_l not in ["nan",""] else ""
        st.markdown(f"""
        <div class="log-row">
            <div class="log-dot"></div>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">
                    <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
                        <span style="font-size:11.5px;font-weight:700;background:#f1f5f9;
                                     padding:2px 8px;border-radius:5px;">{log['action_type']}</span>
                        <span style="font-size:12px;font-weight:700;color:#1d4ed8;">{log['order_id']}</span>
                        {prev_b}{ns_b}
                    </div>
                    <span style="font-size:11px;color:#94a3b8;white-space:nowrap;">{log['performed_at']}</span>
                </div>
                <div style="font-size:12.5px;color:#374151;margin-top:5px;">
                    {log['details']} — <b>{log['performed_by']}</b>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════════════
def page_reports():
    topbar("📈 Reports", "Financial summaries and order analytics by company and status")
    D      = st.session_state.data
    orders = D["orders"].copy()
    orders["total_value"] = orders["total_value"].astype(float)
    pad = "padding:0 28px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="tcard" style="margin-bottom:20px;">
            <div class="tcard-header"><div class="tcard-title">🏢 Orders by Company</div></div>
            <div style="padding:18px;">
        """, unsafe_allow_html=True)
        for co in COMPANIES:
            rows = orders[orders["company"]==co]
            cnt  = len(rows); val = rows["total_value"].sum()
            pct  = int(cnt / max(len(orders),1) * 100)
            fg   = CO_FG.get(co,"#64748b"); bg = CO_BG.get(co,"#f1f5f9")
            st.markdown(f"""
            <div style="margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span class="co-tag" style="background:{bg};color:{fg};">{co}</span>
                    <span style="font-size:12.5px;font-weight:700;color:{fg};">
                        {cnt} orders · ₹{val/100000:.1f}L
                    </span>
                </div>
                <div style="background:#f1f5f9;border-radius:4px;height:6px;">
                    <div style="width:{pct}%;background:{fg};border-radius:4px;height:6px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="tcard" style="margin-bottom:20px;">
            <div class="tcard-header"><div class="tcard-title">📊 Orders by Status</div></div>
            <div style="padding:18px;">
        """, unsafe_allow_html=True)
        for status in STATUSES:
            cnt = len(orders[orders["current_status"]==status])
            pct = int(cnt / max(len(orders),1) * 100)
            fg  = STATUS_FG.get(status,"#64748b"); bg = STATUS_BG.get(status,"#f1f5f9")
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                    <span class="badge" style="background:{bg};color:{fg};">
                        {STATUS_EMOJI.get(status,"")} {status}
                    </span>
                    <span style="font-size:13px;font-weight:700;color:{fg};">{cnt}</span>
                </div>
                <div style="background:#f1f5f9;border-radius:4px;height:5px;">
                    <div style="width:{pct}%;background:{fg};border-radius:4px;height:5px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # Financial table
    st.markdown("""
    <div class="tcard" style="margin-bottom:20px;">
        <div class="tcard-header"><div class="tcard-title">💵 Financial Summary</div></div>
    """, unsafe_allow_html=True)
    TH = ("padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
          "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
          "border-bottom:2px solid #e2e8f0;text-align:left;")
    TD = "padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
    rows_h = ""
    total_outstanding = 0.0
    for i,(_, r) in enumerate(orders.iterrows()):
        bg = "#fff" if i%2==0 else "#fafbfc"
        tv = float(r["total_value"])
        paid = f'<span style="color:#15803d;font-weight:700;">₹{tv:,.0f}</span>' if r["current_status"]=="Paid" else "—"
        out  = "—" if r["current_status"]=="Paid" else f'<span style="color:#b45309;font-weight:700;">₹{tv:,.0f}</span>'
        if r["current_status"] != "Paid":
            total_outstanding += tv
        rows_h += f"""<tr style="background:{bg}">
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
            <th style="{TH}">Department</th><th style="{TH}">Order Value</th>
            <th style="{TH}">Status</th><th style="{TH}">Paid</th><th style="{TH}">Outstanding</th>
        </tr></thead>
        <tbody>{rows_h}</tbody>
    </table></div>
    <div style="padding:12px 16px;background:#f8fafc;border-top:1px solid #e2e8f0;
                display:flex;justify-content:space-between;font-size:13px;font-weight:700;">
        <span style="color:#64748b;">Total Outstanding</span>
        <span style="color:#b45309;">₹{total_outstanding:,.0f}</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════
def page_admin():
    topbar("⚙️ Admin Panel", "Data export, system statistics, user management")
    D   = st.session_state.data
    pad = "padding:0 28px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;
                padding:14px 18px;margin-bottom:20px;font-size:13px;color:#1e40af;line-height:1.8;">
        ✅ <b>Auto-Save</b> — Every update saves instantly to CSV files on the server.<br>
        📥 <b>Export CSV</b> — Download individual or all tables to your computer.<br>
        🔄 <b>Reset</b> — Restore to sample seed data if needed (danger zone).
    </div>""", unsafe_allow_html=True)

    # Export
    st.markdown("""
    <div class="tcard" style="margin-bottom:20px;">
        <div class="tcard-header"><div class="tcard-title">📥 Export Data</div></div>
        <div style="padding:18px;">
    """, unsafe_allow_html=True)
    tables = ["orders","procurement","dispatch","delivery","invoices","activity_log"]
    c = st.columns(3)
    for i, t in enumerate(tables):
        with c[i % 3]:
            csv = D[t].to_csv(index=False).encode("utf-8")
            st.download_button(f"📄 {t} ({len(D[t])} rows)", csv,
                               f"supply_chain_{t}_{now_ist()[:10]}.csv","text/csv",
                               use_container_width=True, key=f"dl_{t}")
    sp(8)
    all_csv = "\n\n".join([f"=== {t.upper()} ===\n"+D[t].to_csv(index=False) for t in tables])
    st.download_button("📦 Export ALL Tables (Single File)", all_csv.encode(),
                       f"supply_chain_full_{now_ist()[:10]}.csv","text/csv",
                       use_container_width=True, key="dl_all", type="primary")
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Stats
    st.markdown("""
    <div class="tcard" style="margin-bottom:20px;">
        <div class="tcard-header"><div class="tcard-title">⚙️ Database Statistics</div></div>
        <div style="padding:18px;display:grid;grid-template-columns:repeat(6,1fr);gap:12px;">
    """, unsafe_allow_html=True)
    for t in tables:
        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-top:3px solid #1d4ed8;
                    border-radius:8px;padding:12px;text-align:center;">
            <div style="font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;">{t}</div>
            <div style="font-size:22px;font-weight:800;color:#1d4ed8;margin-top:6px;">{len(D[t])}</div>
            <div style="font-size:10px;color:#94a3b8;">rows</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Users
    st.markdown("""
    <div class="tcard" style="margin-bottom:20px;">
        <div class="tcard-header"><div class="tcard-title">👥 User Accounts &amp; Roles</div></div>
        <div style="overflow-x:auto;">
    """, unsafe_allow_html=True)
    TH = ("padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
          "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
          "border-bottom:2px solid #e2e8f0;text-align:left;")
    TD = "padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;"
    ROLE_DESC = {
        "Admin":"Full access — create, update, reports, admin panel",
        "Manager":"Create orders, update all stages, view reports",
        "Staff":"Update existing orders only — all stages",
        "Viewer":"Read-only — dashboard, details, activity log",
    }
    rows_h = ""
    for i,(u,v) in enumerate(USERS.items()):
        bg = "#fff" if i%2==0 else "#fafbfc"
        rc = ROLE_COLOR.get(v['role'],"#64748b"); rb = ROLE_BG.get(v['role'],"#f1f5f9")
        rows_h += f"""<tr style="background:{bg}">
            <td style="{TD}font-weight:700;font-family:monospace;">{u}</td>
            <td style="{TD}">{v['name']}</td>
            <td style="{TD}"><span class="badge" style="background:{rb};color:{rc};">{v['role']}</span></td>
            <td style="{TD}color:#64748b;font-size:12px;">{ROLE_DESC.get(v['role'],'')}</td>
        </tr>"""
    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse;">
        <thead><tr>
            <th style="{TH}">Username</th><th style="{TH}">Full Name</th>
            <th style="{TH}">Role</th><th style="{TH}">Permissions</th>
        </tr></thead><tbody>{rows_h}</tbody>
    </table>
    </div></div>""", unsafe_allow_html=True)

    # Danger zone
    with st.expander("⚠️ Danger Zone — Reset All Data"):
        st.warning("This permanently deletes all data and restores sample records. This action cannot be undone.")
        if st.button("🗑 Reset to Sample Data", type="primary"):
            for key, df in SEED.items():
                df.astype(str).fillna("").to_csv(FILES[key], index=False)
            st.session_state.data = load_data()
            st.success("✅ Data reset to sample records.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    render_sidebar()

    allowed = ROLE_MENUS.get(st.session_state.role, [])
    if st.session_state.menu not in allowed:
        st.session_state.menu = "Dashboard"
        st.rerun()

    PAGES = {
        "Dashboard":     page_dashboard,
        "New Order":     page_new_order,
        "Update Order":  page_update_order,
        "Order Details": page_order_details,
        "Activity Log":  page_activity_log,
        "Reports":       page_reports,
        "Admin":         page_admin,
    }
    PAGES[st.session_state.menu]()

if __name__ == "__main__":
    main()
