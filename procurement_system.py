import streamlit as st
import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG — must be first Streamlit call
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Supply Chain Tracking System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
COMPANIES  = ["Robokart", "Bharat Tech", "EL"]
STATUSES   = ["Pending", "Procured", "Dispatched", "Delivered", "Invoiced", "Paid"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]

# Enhanced Color Palette Matching Screenshots
STATUS_EMOJI = {"Pending":"⏳","Procured":"🔧","Dispatched":"🚚","Delivered":"📦","Invoiced":"🧾","Paid":"💰"}
STATUS_BG    = {"Pending":"#fef3c7","Procured":"#dbeafe","Dispatched":"#ede9fe","Delivered":"#d1fae5","Invoiced":"#cffafe","Paid":"#dcfce7"}
STATUS_FG    = {"Pending":"#d97706","Procured":"#2563eb","Dispatched":"#7c3aed","Delivered":"#059669","Invoiced":"#0891b2","Paid":"#16a34a"}
PRIO_BG      = {"Low":"#f1f5f9","Medium":"#dbeafe","High":"#fef3c7","Urgent":"#fee2e2"}
PRIO_FG      = {"Low":"#64748b","Medium":"#2563eb","High":"#d97706","Urgent":"#dc2626"}
CO_BG        = {"Robokart":"#ede9fe","Bharat Tech":"#cffafe","EL":"#ffedd5"}
CO_FG        = {"Robokart":"#7c3aed","Bharat Tech":"#0891b2","EL":"#c2410c"}

# Enhanced User System
USERS = {
    "Admin":   {"password":"admin@123",    "role":"Admin",   "name":"System Admin"},
    "Manager": {"password":"mgr@123",      "role":"Manager", "name":"Operations Manager"},
    "Staff":   {"password":"staff@123",    "role":"Staff",   "name":"Operations Staff"},
    "Viewer":  {"password":"viewer@123",   "role":"Viewer",  "name":"Finance Viewer"},
}

ROLE_MENUS = {
    "Admin":   ["Dashboard","Orders","New Order","Update Order","Order Details","Activity Log","Reports","Admin"],
    "Manager": ["Dashboard","Orders","New Order","Update Order","Order Details","Activity Log","Reports"],
    "Staff":   ["Dashboard","Orders","Update Order","Order Details","Activity Log"],
    "Viewer":  ["Dashboard","Orders","Order Details","Activity Log"],
}

MENU_ICONS = {
    "Dashboard":"📊","Orders":"📋","New Order":"➕","Update Order":"🔄",
    "Order Details":"🔍","Activity Log":"📈","Reports":"📊","Admin":"⚙️",
}

ROLE_COLOR = {"Admin":"#dc2626","Manager":"#d97706","Staff":"#2563eb","Viewer":"#059669"}
ROLE_BG    = {"Admin":"#fee2e2","Manager":"#fef3c7","Staff":"#dbeafe","Viewer":"#dcfce7"}

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LAYER & ENHANCED SEED DATA
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
        {"id":1,"order_id":"ORD-2026-02-28-001","vendor_name":"RoboSupplies Ltd","vendor_po":"VPO/2026/001","procurement_date":"2026-02-15","expected_delivery":"2026-02-25","qc_status":"Passed","qc_inspector":"Rahul Verma","notes":"All kits verified and tested","updated_by":"Rahul","updated_at":"2026-02-15 14:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-003","vendor_name":"AeroParts International","vendor_po":"VPO/2026/003","procurement_date":"2026-02-05","expected_delivery":"2026-02-15","qc_status":"Passed","qc_inspector":"Vikram Singh","notes":"Custom drone components sourced","updated_by":"Vikram","updated_at":"2026-02-05 10:00:00"},
        {"id":3,"order_id":"ORD-2026-02-28-004","vendor_name":"Robokart Warehouse","vendor_po":"INT/2026/004","procurement_date":"2026-02-22","expected_delivery":"2026-02-26","qc_status":"Passed","qc_inspector":"Dev Kumar","notes":"Internal stock allocation","updated_by":"Dev","updated_at":"2026-02-22 09:00:00"},
    ]),
    "dispatch": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-001","courier_name":"Blue Dart Express","tracking_number":"BD123456789","vehicle_number":"DL01AB1234","driver_contact":"9111222333","dispatch_date":"2026-02-18","estimated_delivery":"2026-03-05","dispatch_address":"Warehouse A, Sector 18, Noida","notes":"Fragile - Handle with care","updated_by":"Rahul","updated_at":"2026-02-18 08:30:00"},
        {"id":2,"order_id":"ORD-2026-02-28-003","courier_name":"DTDC Courier","tracking_number":"DTDC987654321","vehicle_number":"MH04XY5678","driver_contact":"9444555666","dispatch_date":"2026-02-10","estimated_delivery":"2026-02-20","dispatch_address":"Central Facility, Pune","notes":"Secure packaging for defense equipment","updated_by":"Ops","updated_at":"2026-02-10 10:30:00"},
        {"id":3,"order_id":"ORD-2026-02-28-004","courier_name":"In-House Logistics","tracking_number":"IH-004-UP","vehicle_number":"UP32CD9012","driver_contact":"9777888999","dispatch_date":"2026-02-24","estimated_delivery":"2026-02-28","dispatch_address":"Robokart Hub, Lucknow","notes":"Priority delivery for government project","updated_by":"Dev","updated_at":"2026-02-24 09:00:00"},
    ]),
    "delivery": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-003","delivery_date":"2026-02-19","delivery_time":"16:00","received_by":"Col. Vikram Singh","receiver_phone":"9000123456","delivery_status":"Successfully Delivered","quantity_delivered":10,"delivery_location":"DRDO Research Center, New Delhi","feedback":"Excellent condition, all items verified","updated_by":"Ops","updated_at":"2026-02-19 16:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-004","delivery_date":"2026-02-26","delivery_time":"14:30","received_by":"Ms. Anita Verma","receiver_phone":"9988776655","delivery_status":"Successfully Delivered","quantity_delivered":30,"delivery_location":"Smart City Control Room, Lucknow","feedback":"On-time delivery, installation support provided","updated_by":"Dev","updated_at":"2026-02-26 14:30:00"},
    ]),
    "invoices": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-003","invoice_number":"INV-2026-0321","invoice_date":"2026-02-20","invoice_amount":1500000,"payment_status":"Completed","payment_mode":"NEFT","transaction_reference":"TXN20260224DEF","payment_date":"2026-02-24","updated_by":"Finance","updated_at":"2026-02-24 16:00:00"},
        {"id":2,"order_id":"ORD-2026-02-28-004","invoice_number":"INV-2026-0389","invoice_date":"2026-02-27","invoice_amount":670000,"payment_status":"Approved","payment_mode":"","transaction_reference":"","payment_date":"","updated_by":"Finance","updated_at":"2026-02-27 11:00:00"},
    ]),
    "activity_log": pd.DataFrame([
        {"id":1,"order_id":"ORD-2026-02-28-001","action_type":"ORDER_CREATED","previous_status":"—","new_status":"Pending","performed_by":"Admin","performed_at":"2026-02-10 09:30:00","details":"Order created for Education Department Delhi"},
        {"id":2,"order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Pending","new_status":"Procured","performed_by":"Rahul","performed_at":"2026-02-15 14:00:00","details":"Procurement completed - All kits verified"},
        {"id":3,"order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Procured","new_status":"Dispatched","performed_by":"Rahul","performed_at":"2026-02-18 08:30:00","details":"Dispatched via Blue Dart Express"},
        {"id":4,"order_id":"ORD-2026-02-28-003","action_type":"PAYMENT","previous_status":"Invoiced","new_status":"Paid","performed_by":"Finance","performed_at":"2026-02-24 16:00:00","details":"NEFT payment received - TXN20260224DEF"},
        {"id":5,"order_id":"ORD-2026-02-28-004","action_type":"STATUS_CHANGE","previous_status":"Dispatched","new_status":"Delivered","performed_by":"Dev","performed_at":"2026-02-26 14:30:00","details":"Delivered successfully, challan signed"},
    ]),
}

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
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
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════
for k,v in [("logged_in",False),("username",""),("role",""),("user_name",""),
            ("menu","Dashboard"),("company_filter","All")]:
    if k not in st.session_state:
        st.session_state[k] = v
if "data" not in st.session_state:
    st.session_state.data = load_data()

# ═══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE CSS STYLING - MATCHING SCREENSHOTS EXACTLY
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap');

/* ── Reset & Base Styling ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #f0f4f8 !important;
    color: #0f172a !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar Styling (Dark Theme) ── */
[data-testid="stSidebar"] {
    background: #1e293b !important;
    min-width: 240px !important;
    max-width: 240px !important;
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
    font-weight: 500 !important;
    padding: 12px 18px !important;
    margin: 0 !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important;
    border-left-color: #3b82f6 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #2563eb !important;
    color: #fff !important;
    font-weight: 700 !important;
    border-left: 3px solid #60a5fa !important;
    border-radius: 6px !important;
    margin: 2px 10px !important;
    width: calc(100% - 20px) !important;
}

/* ── Page Header ── */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    padding: 18px 32px;
    border-bottom: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 24px;
}
.ph-title { font-size: 22px; font-weight: 800; color: #0f172a; }
.ph-subtitle { font-size: 13px; color: #64748b; margin-top: 3px; }
.ph-right { display: flex; align-items: center; gap: 16px; }
.ph-saved { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #16a34a; font-weight: 600; }
.ph-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; }
.ph-date { font-size: 12px; color: #94a3b8; }

/* ── Cards ── */
.card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 20px;
    border-bottom: 1px solid #f1f5f9;
    background: #fafbfc;
}
.card-title { font-size: 14px; font-weight: 700; color: #0f172a; }
.card-count {
    font-size: 11px; font-weight: 600; color: #64748b;
    background: #f1f5f9; padding: 4px 14px; border-radius: 99px;
}
.card-body { padding: 20px; }

/* ── Metric Cards ── */
.metric-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.metric-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.7px; color: #64748b; margin-bottom: 10px;
}
.metric-value { font-size: 28px; font-weight: 800; line-height: 1; }

/* ── Tables ── */
.styled-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.styled-table th {
    padding: 12px 16px;
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
.styled-table td {
    padding: 14px 16px;
    border-bottom: 1px solid #f1f5f9;
    color: #1e293b;
    vertical-align: middle;
}
.styled-table tr:hover td { background: #f8faff; }

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    white-space: nowrap;
}
.co-badge {
    display: inline-block;
    padding: 4px 11px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
}

/* ── Enhanced Form Styling ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stTimeInput > div > div > input {
    border-radius: 7px !important;
    border: 1.5px solid #d1d5db !important;
    font-size: 13px !important;
    background: #ffffff !important;
    color: #0f172a !important;
    padding: 10px 14px !important;
    -webkit-text-fill-color: #0f172a !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #9ca3af !important;
    -webkit-text-fill-color: #9ca3af !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > div:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    outline: none !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stNumberInput label, .stDateInput label, .stTimeInput label,
.stFileUploader label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #374151 !important;
    margin-bottom: 6px !important;
}

/* ── Enhanced Button Styling ── */
.stButton > button {
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    transition: all 0.15s !important;
}
.stButton > button[kind="primary"] {
    background: #dc2626 !important;
    border-color: #dc2626 !important;
    color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #b91c1c !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(220,38,38,0.3);
}
.stButton > button[kind="secondary"] {
    background: #fff !important;
    border: 1px solid #e2e8f0 !important;
    color: #374151 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #f8f9fa !important;
    border-color: #cbd5e1 !important;
}

/* ── Enhanced Tab Styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #fff !important;
    border-bottom: 2px solid #e2e8f0 !important;
    gap: 0 !important;
    padding: 0 20px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    color: #64748b !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 14px 24px !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    border-bottom: 3px solid #2563eb !important;
    color: #2563eb !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #fff !important;
    padding: 24px !important;
    border-radius: 0 0 8px 8px !important;
    border: 1px solid #e2e8f0 !important;
    border-top: none !important;
}

/* ── Info Row for Order Summary ── */
.info-row {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 20px;
}
.info-item { flex: 1; min-width: 140px; }
.info-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.5px; color: #64748b; margin-bottom: 6px;
}
.info-value { font-size: 13px; font-weight: 600; color: #0f172a; }

/* ── Progress Steps ── */
.step-bar { display: flex; align-items: center; margin: 24px 0; }
.step-node {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; flex-shrink: 0;
}
.step-done { background: #2563eb; color: #fff; }
.step-pending { background: #e2e8f0; color: #94a3b8; }
.step-line-d { flex: 1; height: 3px; background: #2563eb; margin: 0 6px; }
.step-line-p { flex: 1; height: 3px; background: #e2e8f0; margin: 0 6px; }
.step-label {
    font-size: 10px; text-align: center; margin-top: 6px; font-weight: 600;
}

/* ── Activity Log Entries ── */
.log-entry {
    display: flex; gap: 14px;
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;
}
.log-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: #2563eb; flex-shrink: 0; margin-top: 6px;
}

/* ── File Upload Styling ── */
.stFileUploader {
    border: 2px dashed #d1d5db !important;
    border-radius: 8px !important;
    background: #fafbfc !important;
    padding: 24px !important;
}
.stFileUploader:hover {
    border-color: #2563eb !important;
    background: rgba(37,99,235,0.05) !important;
}

/* ── Login Page Styling ── */
.login-bg {
    background: linear-gradient(135deg, #0c1426 0%, #1a3a6b 55%, #0c1426 100%) !important;
    min-height: 100vh;
}
[data-testid="stForm"] {
    background: #ffffff !important;
    border-radius: 0 0 16px 16px !important;
    padding: 32px 36px 40px 36px !important;
    box-shadow: 0 24px 60px rgba(0,0,0,0.5) !important;
}
[data-testid="stForm"] input {
    background-color: #f8fafc !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    height: 50px !important;
    padding: 0 16px !important;
}
[data-testid="stForm"] input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    background-color: #ffffff !important;
}
[data-testid="stForm"] button {
    background: #dc2626 !important;
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    height: 52px !important;
    border-radius: 8px !important;
    width: 100% !important;
    margin-top: 16px !important;
}

/* ── Footer ── */
.footer {
    text-align: center; font-size: 11px; color: #94a3b8;
    padding: 20px 0 12px 0; border-top: 1px solid #e2e8f0; margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# UI HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def sbadge(status):
    bg = STATUS_BG.get(status,"#f1f5f9")
    fg = STATUS_FG.get(status,"#64748b")
    em = STATUS_EMOJI.get(status,"")
    return f'<span class="badge" style="background:{bg};color:{fg};">{em} {status}</span>'

def pbadge(priority):
    bg = PRIO_BG.get(priority,"#f1f5f9")
    fg = PRIO_FG.get(priority,"#64748b")
    return f'<span class="badge" style="background:{bg};color:{fg};">{priority}</span>'

def cobadge(company):
    bg = CO_BG.get(company,"#f1f5f9")
    fg = CO_FG.get(company,"#64748b")
    return f'<span class="co-badge" style="background:{bg};color:{fg};">{company}</span>'

def page_header(title, subtitle=""):
    today = datetime.now().strftime("%d %b %Y")
    sub_html = f'<div class="ph-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="ph-title">{title}</div>
            {sub_html}
        </div>
        <div class="ph-right">
            <span class="ph-saved"><span class="ph-dot"></span>&nbsp;Auto-saved</span>
            <span class="ph-date">{today}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def card_start(title, count=None):
    cnt_html = f'<span class="card-count">{count}</span>' if count is not None else ""
    st.markdown(f'<div class="card"><div class="card-header"><span class="card-title">{title}</span>{cnt_html}</div><div class="card-body">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div></div>', unsafe_allow_html=True)

def show_footer():
    st.markdown(f'<div class="footer">© {datetime.now().year} Robokart. All rights reserved. Supply Chain Tracking System.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def login_page():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0c1426 0%, #1a3a6b 55%, #0c1426 100%) !important; }
    [data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 16px 16px 0 0;
            padding: 42px 36px 32px 36px;
            text-align: center;
            border-bottom: 1px solid #f1f5f9;
        ">
            <div style="font-size:56px; margin-bottom:16px;">🏭</div>
            <div style="font-size:24px; font-weight:800; color:#0f172a; line-height:1.3;">
                Supply Chain Tracking System
            </div>
            <div style="font-size:13px; color:#64748b; margin-top:12px;">
                Sign in with your credentials to continue
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            st.text_input("Username", placeholder="Enter your username", key="li_user")
            st.text_input("Password", type="password", placeholder="Enter your password", key="li_pass")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

        if submitted:
            u = st.session_state.get("li_user", "").strip()
            p = st.session_state.get("li_pass", "").strip()
            if u in USERS and USERS[u]["password"] == p:
                st.session_state.logged_in = True
                st.session_state.username  = u
                st.session_state.role      = USERS[u]["role"]
                st.session_state.user_name = USERS[u]["name"]
                st.session_state.menu      = "Dashboard"
                st.rerun()
            else:
                st.error("⚠ Invalid username or password. Please try again.")

        st.markdown("""
        <p style="text-align:center; font-size:12px; color:#94a3b8; margin-top:24px;">
            Default: Admin/admin@123 | Manager/mgr@123 | Staff/staff@123 | Viewer/viewer@123
        </p>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:24px 18px 18px;border-bottom:1px solid #334155;">
            <div style="display:flex;align-items:center;gap:12px;color:#fff;">
                <div style="font-size:24px;background:#3b82f6;width:40px;height:40px;border-radius:8px;display:flex;align-items:center;justify-content:center;">🏭</div>
                <div>
                    <div style="font-weight:700;font-size:15px;line-height:1.2;">Supply Chain</div>
                    <div style="font-size:10px;opacity:0.6;text-transform:uppercase;letter-spacing:0.5px;">Tracking System</div>
                </div>
            </div>
        </div>
        <div style="padding:0 18px;margin:12px 0 10px;font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:1px;">Main Menu</div>
        """, unsafe_allow_html=True)

        menus = ROLE_MENUS[st.session_state.role]
        for m in menus:
            active = st.session_state.menu == m
            icon   = MENU_ICONS.get(m,"")
            if st.button(f"{icon}  {m}", key=f"nav_{m}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.menu = m
                st.rerun()

        role = st.session_state.role
        rc   = ROLE_COLOR.get(role,"#64748b")
        rb   = ROLE_BG.get(role,"#f1f5f9")
        st.markdown(f"""
        <div style="position:fixed;bottom:0;width:240px;padding:16px 18px;
                    border-top:1px solid #334155;background:#1e293b;">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:36px;height:36px;background:#dc2626;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:600;">{st.session_state.user_name[0]}</div>
                <div style="flex:1;">
                    <div style="color:#fff;font-size:13px;font-weight:600;">{st.session_state.user_name}</div>
                    <span style="background:{rb};color:{rc};padding:3px 12px;border-radius:99px;font-size:11px;font-weight:700;">{role}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height:90px'></div>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", use_container_width=True, key="signout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    page_header("📊 Dashboard", "Overview of all purchase orders and supply chain status")

    D      = st.session_state.data
    orders = D["orders"].copy()
    cf     = st.session_state.company_filter
    fil    = orders if cf == "All" else orders[orders["company"] == cf]
    tv     = fil["total_value"].astype(float).sum() if len(fil) else 0.0

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    # Metrics
    metrics = [
        ("TOTAL ORDERS",  str(len(fil)),                                                                "#2563eb"),
        ("PENDING",       str(len(fil[fil["current_status"]=="Pending"])),                              "#d97706"),
        ("IN TRANSIT",    str(len(fil[fil["current_status"].isin(["Procured","Dispatched"])])),         "#7c3aed"),
        ("DELIVERED",     str(len(fil[fil["current_status"].isin(["Delivered","Invoiced","Paid"])])),   "#059669"),
        ("PAID",          str(len(fil[fil["current_status"]=="Paid"])),                                 "#16a34a"),
        ("TOTAL VALUE",   f"₹{tv/100000:.1f}L",                                                        "#dc2626"),
    ]
    cols = st.columns(6)
    for col,(label,value,color) in zip(cols,metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-top:3px solid {color};">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{color};">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Company filters
    c_all, c_rk, c_bt, c_el, _ = st.columns([1.5, 1.1, 1.4, 0.8, 3])
    with c_all:
        if st.button("🏢 All Companies" + (" ✓" if cf=="All" else ""), key="f_all",
                     type="primary" if cf=="All" else "secondary", use_container_width=True):
            st.session_state.company_filter = "All"; st.rerun()
    with c_rk:
        if st.button("Robokart" + (" ✓" if cf=="Robokart" else ""), key="f_rk",
                     type="primary" if cf=="Robokart" else "secondary", use_container_width=True):
            st.session_state.company_filter = "Robokart"; st.rerun()
    with c_bt:
        if st.button("Bharat Tech" + (" ✓" if cf=="Bharat Tech" else ""), key="f_bt",
                     type="primary" if cf=="Bharat Tech" else "secondary", use_container_width=True):
            st.session_state.company_filter = "Bharat Tech"; st.rerun()
    with c_el:
        if st.button("EL" + (" ✓" if cf=="EL" else ""), key="f_el",
                     type="primary" if cf=="EL" else "secondary", use_container_width=True):
            st.session_state.company_filter = "EL"; st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Orders table
    title = "All Orders" if cf == "All" else f"{cf} Orders"
    TH = ("padding:12px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
          "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
          "border-bottom:2px solid #e2e8f0;text-align:left;")
    TD = "padding:14px 16px;border-bottom:1px solid #f1f5f9;color:#1e293b;font-size:12.5px;"

    if len(fil) == 0:
        table_body = '<div style="padding:40px;text-align:center;color:#94a3b8;font-size:14px;">No orders found.</div>'
    else:
        rows_html = ""
        for i, (_, r) in enumerate(fil.iterrows()):
            bg = "#ffffff" if i % 2 == 0 else "#fafbfc"
            desc = str(r['item_description'])
            if len(desc) > 40: desc = desc[:40] + "..."
            rows_html += f"""
            <tr style="background:{bg};" onmouseover="this.style.background='#f0f7ff'" onmouseout="this.style.background='{bg}'">
                <td style="{TD}font-weight:700;color:#2563eb;font-size:11.5px;">{r['order_id']}</td>
                <td style="{TD}">{cobadge(r['company'])}</td>
                <td style="{TD}color:#64748b;font-size:11.5px;">{r['po_number']}</td>
                <td style="{TD}">{r['govt_department']}</td>
                <td style="{TD}color:#374151;">{desc}</td>
                <td style="{TD}text-align:center;font-weight:600;">{r['quantity']}</td>
                <td style="{TD}font-weight:700;">₹{float(r['total_value']):,.0f}</td>
                <td style="{TD}">{pbadge(r['priority'])}</td>
                <td style="{TD}">{sbadge(r['current_status'])}</td>
                <td style="{TD}color:#94a3b8;font-size:11px;">{r['last_updated']}</td>
            </tr>"""
        table_body = f"""
        <table class="styled-table">
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
            <tbody>{rows_html}</tbody>
        </table>"""

    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title">📦 {title}</div>
            <div class="card-count">{len(fil)} orders</div>
        </div>
        <div style="overflow-x:auto;">{table_body}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ORDERS LIST
# ═══════════════════════════════════════════════════════════════════════════════
def page_orders():
    page_header("📋 Orders", "Manage all purchase orders")
    D = st.session_state.data
    orders = D["orders"].copy()

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search by order ID, company, department...", label_visibility="collapsed")
    with col2:
        status_filter = st.selectbox("All Statuses", ["All Statuses"] + STATUSES, label_visibility="collapsed")
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Apply filters
    if search:
        orders = orders[
            orders["order_id"].str.contains(search, case=False) |
            orders["company"].str.contains(search, case=False) |
            orders["govt_department"].str.contains(search, case=False)
        ]
    if status_filter != "All Statuses":
        orders = orders[orders["current_status"] == status_filter]

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Orders table
    card_start(f"All Purchase Orders", f"{len(orders)} records")
    if len(orders) == 0:
        st.info("No orders found matching your criteria.")
    else:
        TH = ("padding:12px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
              "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
              "border-bottom:2px solid #e2e8f0;text-align:left;")
        TD = "padding:14px 16px;border-bottom:1px solid #f1f5f9;color:#1e293b;font-size:12.5px;"
        rows_html = ""
        for i, (_, r) in enumerate(orders.iterrows()):
            bg = "#fff" if i % 2 == 0 else "#fafbfc"
            rows_html += f"""
            <tr style="background:{bg};">
                <td style="{TD}font-weight:700;color:#2563eb;">{r['order_id']}</td>
                <td style="{TD}">{cobadge(r['company'])}</td>
                <td style="{TD}color:#64748b;">{r['po_number']}</td>
                <td style="{TD}">{r['govt_department']}</td>
                <td style="{TD}font-weight:700;">₹{float(r['total_value']):,.0f}</td>
                <td style="{TD}">{pbadge(r['priority'])}</td>
                <td style="{TD}">{sbadge(r['current_status'])}</td>
                <td style="{TD}color:#94a3b8;font-size:11px;">{r['last_updated']}</td>
            </tr>"""
        st.markdown(f"""
        <div style="overflow-x:auto;">
        <table class="styled-table">
            <thead><tr>
                <th style="{TH}">Order ID</th>
                <th style="{TH}">Company</th>
                <th style="{TH}">PO Number</th>
                <th style="{TH}">Department</th>
                <th style="{TH}">Value</th>
                <th style="{TH}">Priority</th>
                <th style="{TH}">Status</th>
                <th style="{TH}">Updated</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table></div>""", unsafe_allow_html=True)
    card_end()

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NEW ORDER
# ═══════════════════════════════════════════════════════════════════════════════
def page_new_order():
    page_header("➕ New Order", "Create a new government purchase order")
    D = st.session_state.data

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)
    card_start("📝 Purchase Order Details")
    with st.form("new_order_form", clear_on_submit=True):
        st.markdown("**Company \\***")
        company = st.selectbox("Company", COMPANIES, label_visibility="collapsed", key="no_company")
        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            govt_dept    = st.text_input("Government Department *",    placeholder="e.g., Education Department Delhi")
            contact_name = st.text_input("Contact Person *",           placeholder="e.g., Mr. Rajesh Kumar")
            contact_ph   = st.text_input("Contact Phone",              placeholder="e.g., 9876543210")
            po_number    = st.text_input("PO Number *",                placeholder="e.g., PO/EDU/2026/001")
        with c2:
            assigned_co  = st.text_input("Assigned Company",           placeholder="e.g., Tech Solutions Pvt Ltd")
            exp_delivery = st.date_input("Expected Delivery Date")
            quantity     = st.number_input("Quantity *",               min_value=1, value=1)
            total_value  = st.number_input("Total Value (₹) *",        min_value=0, value=0)
        c3,_ = st.columns([1,2])
        with c3:
            priority = st.selectbox("Priority", PRIORITIES, index=1)
        item_desc = st.text_area("Item Description *", placeholder="Detailed description of goods/services...", height=100)
        remarks   = st.text_area("Remarks",            placeholder="Any additional remarks...", height=70)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Create Order", use_container_width=True, type="primary")

        if submitted:
            errors = []
            if not govt_dept:    errors.append("Government Department")
            if not contact_name: errors.append("Contact Person")
            if not po_number:    errors.append("PO Number")
            if not item_desc:    errors.append("Item Description")
            if not total_value:  errors.append("Total Value")
            if errors:
                st.error(f"❌ Please fill required fields: {', '.join(errors)}")
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
                add_log(order_id,"ORDER_CREATED","—","Pending",st.session_state.user_name,f"Order created for {govt_dept}")
                st.success(f"✅ Order **{order_id}** created successfully!")
    card_end()
    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: UPDATE ORDER (Enhanced Step-by-Step Forms)
# ═══════════════════════════════════════════════════════════════════════════════
def page_update_order():
    page_header("🔄 Update Order", "Update procurement, dispatch, delivery or invoice status")
    D = st.session_state.data

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    order_opts = ["— Select an order —"] + [
        f"[{r['company']}] {r['order_id']} · {r['po_number']} · {r['current_status']}"
        for _,r in D["orders"].iterrows()
    ]
    sel = st.selectbox("**Select Order to Update \\***", order_opts, key="uo_sel")
    if sel == "— Select an order —":
        st.info("👆 Select an order above to begin updating.")
        st.markdown('</div>', unsafe_allow_html=True)
        show_footer()
        return

    oid   = sel.split(" · ")[0].split("] ")[1].strip()
    order = get_order(oid)

    # Order summary card
    s  = order["current_status"]
    co = order["company"]
    st.markdown(f"""
    <div class="info-row">
        <div class="info-item">
            <div class="info-label">Company</div>
            <div class="info-value">{cobadge(co)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Status</div>
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

    updated_by = st.text_input("**Your Name / Department \\***", placeholder="e.g., Rahul — Logistics Team", key="uo_by")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["🔧  Procurement", "🚚  Dispatch", "📦  Delivery", "💰  Invoice"])

    # ── PROCUREMENT TAB ──
    with tab1:
        st.markdown("### Procurement Details")
        st.markdown("Complete vendor information and quality check details for this order.")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        
        with st.form("proc_form"):
            c1,c2 = st.columns(2)
            with c1:
                vendor_name = st.text_input("Vendor/Supplier Name *", placeholder="e.g., RoboSupplies Ltd")
                vendor_po   = st.text_input("Vendor PO Number *", placeholder="e.g., VPO/2026/001")
                proc_date   = st.date_input("Procurement Date *", key="pd")
            with c2:
                exp_del     = st.date_input("Expected Delivery Date", key="ped")
                qc_status   = st.selectbox("Quality Check Status", ["","Pending","In Progress","Passed","Failed","Partial Pass"])
                qc_insp     = st.text_input("QC Inspector Name", placeholder="Inspector name")
            
            proc_notes = st.text_area("Procurement Notes/Remarks", placeholder="Any procurement-related notes or special instructions...", height=100)
            
            st.markdown("**📁 Procurement Documents**")
            st.markdown("*Upload vendor invoices, QC reports, purchase orders — any file type, multiple files allowed*")
            proc_files = st.file_uploader("Upload files", accept_multiple_files=True, key="pf", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                sv = st.form_submit_button("✅ Save & Continue to Dispatch", use_container_width=True, type="primary")
            with col2:
                st.form_submit_button("Cancel", use_container_width=True, type="secondary")
            
            if sv:
                if not updated_by:
                    st.error("❌ Please enter your name above the tabs.")
                elif not vendor_name or not vendor_po or not proc_date:
                    st.error("❌ Please fill all required fields (marked with *).")
                else:
                    ts = now_ist()
                    row = pd.DataFrame([{"id":str(len(D["procurement"])+1),"order_id":oid,
                        "vendor_name":vendor_name,"vendor_po":vendor_po,
                        "procurement_date":str(proc_date),"expected_delivery":str(exp_del),
                        "qc_status":qc_status,"qc_inspector":qc_insp,
                        "notes":proc_notes,"updated_by":updated_by,"updated_at":ts}])
                    D["procurement"] = pd.concat([D["procurement"],row],ignore_index=True)
                    save_table("procurement")
                    ns = "Procured"
                    prev = order["current_status"]
                    update_order_status(oid, ns)
                    add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,f"Procurement completed - {vendor_name} | {len(proc_files or [])} files")
                    st.success(f"✅ Procurement saved! Status updated → **{ns}**")
                    st.rerun()

    # ── DISPATCH TAB ──
    with tab2:
        st.markdown("### Dispatch & Logistics Details")
        st.markdown("Enter courier information, tracking details, and dispatch logistics.")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        
        with st.form("disp_form"):
            c1,c2 = st.columns(2)
            with c1:
                courier   = st.text_input("Courier/Transporter Name *", placeholder="e.g., Blue Dart Express")
                tracking  = st.text_input("Tracking/AWB Number *", placeholder="e.g., BD123456789")
                vehicle   = st.text_input("Vehicle Number", placeholder="e.g., DL01AB1234")
            with c2:
                driver    = st.text_input("Driver Name/Contact", placeholder="Driver details")
                disp_date = st.date_input("Dispatch Date *", key="dd")
                est_del   = st.date_input("Estimated Delivery Date", key="ded")
            
            disp_addr = st.text_area("Dispatch From Address", placeholder="Complete warehouse/facility address...", height=80)
            disp_notes = st.text_area("Dispatch Instructions/Notes", placeholder="Special handling instructions, delivery preferences...", height=100)
            
            st.markdown("**📁 Dispatch Documents**")
            st.markdown("*E-way bills, dispatch photos, shipping labels — any file type*")
            disp_files = st.file_uploader("Upload files", accept_multiple_files=True, key="df", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                sv = st.form_submit_button("✅ Save & Continue to Delivery", use_container_width=True, type="primary")
            with col2:
                st.form_submit_button("← Back to Procurement", use_container_width=True, type="secondary")
            
            if sv:
                if not updated_by:
                    st.error("❌ Please enter your name above the tabs.")
                elif not courier or not tracking or not disp_date:
                    st.error("❌ Please fill all required fields (marked with *).")
                else:
                    ts = now_ist()
                    row = pd.DataFrame([{"id":str(len(D["dispatch"])+1),"order_id":oid,
                        "courier_name":courier,"tracking_number":tracking,
                        "vehicle_number":vehicle,"driver_contact":driver,
                        "dispatch_date":str(disp_date),"estimated_delivery":str(est_del),
                        "dispatch_address":disp_addr,"notes":disp_notes,
                        "updated_by":updated_by,"updated_at":ts}])
                    D["dispatch"] = pd.concat([D["dispatch"],row],ignore_index=True)
                    save_table("dispatch")
                    prev = order["current_status"]
                    update_order_status(oid,"Dispatched")
                    add_log(oid,"STATUS_CHANGE",prev,"Dispatched",updated_by,f"Dispatched via {courier} | {len(disp_files or [])} files")
                    st.success("✅ Dispatch saved! Status → **Dispatched**")
                    st.rerun()

    # ── DELIVERY TAB ──
    with tab3:
        st.markdown("### Delivery Confirmation Details")
        st.markdown("Record delivery completion, receiver information, and proof of delivery.")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        
        with st.form("del_form"):
            c1,c2 = st.columns(2)
            with c1:
                del_date   = st.date_input("Actual Delivery Date *", key="dld")
                del_time   = st.time_input("Delivery Time", key="dlt")
                recv_name  = st.text_input("Received By (Name) *", placeholder="Person who received the order")
            with c2:
                recv_phone = st.text_input("Receiver Phone Number", placeholder="+91 9876543210")
                del_status = st.selectbox("Delivery Status *", ["","Successfully Delivered","Partially Delivered","Returned to Sender","Delivered with Damage"])
                qty_del    = st.number_input("Quantity Delivered", min_value=0, key="dq")
            
            del_loc = st.text_area("Final Delivery Location", placeholder="Exact delivery location/address confirmation...", height=80)
            feedback = st.text_area("Delivery Feedback/Remarks", placeholder="Any delivery issues, customer feedback, or special notes...", height=100)
            
            st.markdown("**📁 Proof of Delivery (POD)**")
            st.markdown("*Signed receipts, delivery photos, proof documents*")
            del_files = st.file_uploader("Upload POD", accept_multiple_files=True, key="dlf", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                sv = st.form_submit_button("✅ Save & Continue to Invoice", use_container_width=True, type="primary")
            with col2:
                st.form_submit_button("← Back to Dispatch", use_container_width=True, type="secondary")
            
            if sv:
                if not updated_by:
                    st.error("❌ Please enter your name above the tabs.")
                elif not del_date or not recv_name or not del_status:
                    st.error("❌ Please fill all required fields (marked with *).")
                else:
                    ts = now_ist()
                    row = pd.DataFrame([{"id":str(len(D["delivery"])+1),"order_id":oid,
                        "delivery_date":str(del_date),"delivery_time":str(del_time),
                        "received_by":recv_name,"receiver_phone":recv_phone,
                        "delivery_status":del_status,"quantity_delivered":str(qty_del),
                        "delivery_location":del_loc,"feedback":feedback,
                        "updated_by":updated_by,"updated_at":ts}])
                    D["delivery"] = pd.concat([D["delivery"],row],ignore_index=True)
                    save_table("delivery")
                    ns = "Delivered" if del_status=="Successfully Delivered" else order["current_status"]
                    prev = order["current_status"]
                    update_order_status(oid, ns)
                    add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,
                            f"Delivery: {del_status} | {len(del_files or [])} POD files")
                    st.success(f"✅ Delivery saved! Status → **{ns}**")
                    st.rerun()

    # ── INVOICE TAB ──
    with tab4:
        st.markdown("### Invoice & Payment Details")
        st.markdown("Complete invoice information and payment processing details.")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        
        with st.form("inv_form"):
            c1,c2 = st.columns(2)
            with c1:
                inv_num    = st.text_input("Invoice Number *", placeholder="e.g., INV-2026-0001")
                inv_date   = st.date_input("Invoice Date *", key="id")
                inv_amount = st.number_input("Invoice Amount (₹) *", min_value=0, key="ia")
                pay_status = st.selectbox("Payment Status *", ["","Pending","Approved","Completed"])
            with c2:
                pay_mode   = st.selectbox("Payment Mode", ["","NEFT","RTGS","Cheque","DD","Online Transfer","Cash"])
                txn_ref    = st.text_input("Transaction Reference", placeholder="Transaction ID / Reference number")
                pay_date   = st.date_input("Payment Date", key="ipd")
            
            st.markdown("**📁 Invoice Files**")
            st.markdown("*PDF, Excel, scanned copies — multiple files allowed*")
            inv_files = st.file_uploader("Upload invoice files", accept_multiple_files=True, key="ivf", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                sv = st.form_submit_button("✅ Save Invoice", use_container_width=True, type="primary")
            with col2:
                st.form_submit_button("← Back to Delivery", use_container_width=True, type="secondary")
            
            if sv:
                if not updated_by:
                    st.error("❌ Please enter your name above the tabs.")
                elif not inv_num or not inv_date or not inv_amount or not pay_status:
                    st.error("❌ Please fill all required fields (marked with *).")
                else:
                    ts = now_ist()
                    row = pd.DataFrame([{"id":str(len(D["invoices"])+1),"order_id":oid,
                        "invoice_number":inv_num,"invoice_date":str(inv_date),
                        "invoice_amount":str(inv_amount),"payment_status":pay_status,
                        "payment_mode":pay_mode,"transaction_reference":txn_ref,
                        "payment_date":str(pay_date),"updated_by":updated_by,"updated_at":ts}])
                    D["invoices"] = pd.concat([D["invoices"],row],ignore_index=True)
                    save_table("invoices")
                    ns = "Paid" if pay_status=="Completed" else "Invoiced"
                    prev = order["current_status"]
                    update_order_status(oid, ns)
                    add_log(oid,"STATUS_CHANGE",prev,ns,updated_by,
                            f"Invoice {inv_num} | {pay_status} | {len(inv_files or [])} files")
                    st.success(f"✅ Invoice saved! Status → **{ns}**")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ORDER DETAILS
# ═══════════════════════════════════════════════════════════════════════════════
def page_order_details():
    page_header("🔍 Order Details", "Complete order information, timeline and activity log")
    D = st.session_state.data

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  {r['current_status']}"
        for _,r in D["orders"].iterrows()
    ]
    sel = st.selectbox("**Select Order**", opts, key="od_sel")
    if sel == "— Select an order —":
        st.info("👆 Select an order to view its complete details.")
        st.markdown('</div>', unsafe_allow_html=True)
        show_footer()
        return

    oid   = sel.split("  ·  ")[0].strip()
    order = get_order(oid)

    # Order header
    s = order["current_status"]
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:24px 28px;
                box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:24px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
            <div>
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                    {cobadge(order['company'])}
                    <span style="font-size:20px;font-weight:800;color:#0f172a;">{order['order_id']}</span>
                </div>
                <div style="font-size:13px;color:#64748b;">{order['po_number']} · {order['govt_department']}</div>
            </div>
            <div style="display:flex;align-items:center;gap:12px;">
                {sbadge(s)}
                {pbadge(order['priority'])}
            </div>
        </div>
        <div style="margin-top:20px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Contact</div><div style="font-size:13px;font-weight:600;">{order['contact_person']}</div></div>
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Phone</div><div style="font-size:13px;font-weight:600;">{order['contact_phone']}</div></div>
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Quantity</div><div style="font-size:13px;font-weight:600;">{order['quantity']}</div></div>
            <div><div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Total Value</div><div style="font-size:18px;font-weight:800;color:#0f172a;">₹{float(order['total_value']):,.0f}</div></div>
        </div>
        <div style="margin-top:16px;padding:12px 16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;">
            <span style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;">Description: </span>
            <span style="font-size:13px;color:#1e293b;">{order['item_description']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress stepper
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
            step_html += f'<div class="{lclass}"></div>'
    step_html += '</div>'
    st.markdown(step_html, unsafe_allow_html=True)

    # Tabs
    t1,t2,t3,t4,t5 = st.tabs(["🔧 Procurement","🚚 Dispatch","📦 Delivery","💰 Invoice","📋 Activity"])

    def show_record(table, oid):
        rows = D[table][D[table]["order_id"]==oid]
        if len(rows) == 0:
            st.info("No data recorded yet for this stage.")
            return
        row = rows.iloc[-1]
        items = [(c.replace("_"," ").title(), str(row[c])) for c in row.index 
                 if c not in ["id","order_id"] and str(row[c]) not in ["","nan"]]
        for i in range(0, len(items), 3):
            chunk = items[i:i+3]
            cs = st.columns(3)
            for col,(label,val) in zip(cs,chunk):
                with col:
                    st.markdown(f"""
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px 16px;">
                        <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:6px;">{label}</div>
                        <div style="font-size:13px;font-weight:600;color:#0f172a;">{val}</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

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
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                        <div>
                            <span style="font-size:12px;font-weight:700;background:#f1f5f9;padding:3px 10px;border-radius:5px;">{log['action_type']}</span>
                            &nbsp; {prev_b}{arrow}
                        </div>
                        <span style="font-size:11px;color:#94a3b8;">{log['performed_at']}</span>
                    </div>
                    <div style="font-size:12.5px;color:#374151;margin-top:6px;">{log['details']} — by <b>{log['performed_by']}</b></div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ACTIVITY LOG
# ═══════════════════════════════════════════════════════════════════════════════
def page_activity_log():
    page_header("📈 Activity Log", "Complete audit trail of all order changes and status updates")
    D    = st.session_state.data
    logs = D["activity_log"].copy().iloc[::-1].reset_index(drop=True)
    
    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)
    card_start(f"System Activity Log", f"{len(logs)} events")
    
    for _,log in logs.iterrows():
        prev = log.get("previous_status","")
        ns   = log.get("new_status","")
        prev_b = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8;">—</span>'
        ns_b   = sbadge(ns)   if ns   and ns   not in ["nan",""]     else ""
        arrow  = ' → ' if ns_b else ""
        st.markdown(f"""
        <div class="log-entry">
            <div class="log-dot"></div>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                        <span style="font-size:12px;font-weight:700;background:#f1f5f9;padding:3px 10px;border-radius:5px;">{log['action_type']}</span>
                        <span style="font-size:12px;font-weight:700;color:#2563eb;">{log['order_id']}</span>
                        {prev_b}{arrow}{ns_b}
                    </div>
                    <span style="font-size:11px;color:#94a3b8;">{log['performed_at']}</span>
                </div>
                <div style="font-size:12.5px;color:#374151;margin-top:6px;">{log['details']} — by <b>{log['performed_by']}</b></div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    card_end()
    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REPORTS
# ═══════════════════════════════════════════════════════════════════════════════
def page_reports():
    page_header("📊 Reports", "Financial summaries and order analytics")
    D      = st.session_state.data
    orders = D["orders"].copy()
    orders["total_value"] = orders["total_value"].astype(float)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        card_start("🏢 Orders by Company")
        for co in COMPANIES:
            rows = orders[orders["company"]==co]
            cnt  = len(rows)
            val  = rows["total_value"].sum()
            pct  = cnt/max(len(orders),1)
            fg   = CO_FG.get(co,"#64748b")
            bg   = CO_BG.get(co,"#f1f5f9")
            st.markdown(f"""
            <div style="margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span class="co-badge" style="background:{bg};color:{fg};">{co}</span>
                    <span style="font-size:12px;font-weight:700;color:{fg};">{cnt} orders · ₹{val/100000:.1f}L</span>
                </div>
                <div style="background:#f1f5f9;border-radius:5px;height:8px;">
                    <div style="width:{int(pct*100)}%;background:{fg};border-radius:5px;height:8px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        card_end()

    with c2:
        card_start("📊 Orders by Status")
        for status in STATUSES:
            cnt = len(orders[orders["current_status"]==status])
            pct = cnt/max(len(orders),1)
            fg  = STATUS_FG.get(status,"#64748b")
            bg  = STATUS_BG.get(status,"#f1f5f9")
            st.markdown(f"""
            <div style="margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span class="badge" style="background:{bg};color:{fg};">{STATUS_EMOJI.get(status,"")} {status}</span>
                    <span style="font-size:13px;font-weight:700;color:{fg};">{cnt}</span>
                </div>
                <div style="background:#f1f5f9;border-radius:5px;height:8px;">
                    <div style="width:{int(pct*100)}%;background:{fg};border-radius:5px;height:8px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        card_end()

    # Financial table
    card_start("💵 Financial Summary")
    TH = "padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;"
    TD = "padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
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
    <table class="styled-table">
        <thead><tr>
            <th style="{TH}">Order ID</th><th style="{TH}">Company</th>
            <th style="{TH}">Department</th><th style="{TH}">Total Value</th>
            <th style="{TH}">Status</th><th style="{TH}">Paid</th><th style="{TH}">Outstanding</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)
    card_end()

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN
# ═══════════════════════════════════════════════════════════════════════════════
def page_admin():
    page_header("⚙️ Admin Panel", "System management, data export, and user administration")
    D = st.session_state.data

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#eff6ff;border:1px solid#93c5fd;border-radius:10px;padding:16px 20px;margin-bottom:24px;font-size:13px;color:#1e40af;line-height:1.9;">
        ✅ <b>Auto-Save</b> — Every change saves instantly to CSV files.<br>
        📥 <b>Export CSV</b> — Downloads directly to your computer.<br>
        🔄 <b>Real-time Updates</b> — All changes reflect immediately across the system.
    </div>""", unsafe_allow_html=True)

    card_start("📥 Export Data to CSV")
    tables = ["orders","procurement","dispatch","delivery","invoices","activity_log"]
    cols   = st.columns(3)
    for i,t in enumerate(tables):
        with cols[i%3]:
            csv = D[t].to_csv(index=False).encode("utf-8")
            st.download_button(f"📄 {t.replace('_',' ').title()}  ({len(D[t])} rows)", csv,
                               f"supply_chain_{t}_{now_ist()[:10]}.csv","text/csv",
                               use_container_width=True, key=f"dl_{t}")
    st.markdown("<br>",unsafe_allow_html=True)
    all_csv = "\n\n".join([f"=== {t.upper()} ===\n" + D[t].to_csv(index=False) for t in tables])
    st.download_button("📦 Export ALL Tables (Single File)", all_csv.encode(),
                       f"supply_chain_complete_{now_ist()[:10]}.csv", "text/csv",
                       use_container_width=True, key="dl_all", type="primary")
    card_end()

    card_start("📊 Database Statistics")
    cols2 = st.columns(6)
    for i,t in enumerate(tables):
        with cols2[i]:
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-top:3px solid #2563eb;
                        border-radius:10px;padding:14px 16px;text-align:center;">
                <div style="font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;">{t.replace('_',' ')}</div>
                <div style="font-size:24px;font-weight:800;color:#2563eb;margin-top:8px;">{len(D[t])}</div>
                <div style="font-size:10px;color:#94a3b8;">records</div>
            </div>""", unsafe_allow_html=True)
    card_end()

    card_start("👥 System Users & Permissions")
    ROLE_DESC = {
        "Admin":   "Full system access — create, update, reports, admin panel",
        "Manager": "Create & update orders, view reports, manage operations",
        "Staff":   "Update order stages — procurement, dispatch, delivery, invoice",
        "Viewer":  "Read-only access — dashboard, order details, activity log",
    }
    TH = "padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;"
    TD = "padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
    rows_html = ""
    for i,(u,v) in enumerate(USERS.items()):
        bg = "#fff" if i%2==0 else "#fafbfc"
        rc = ROLE_COLOR.get(v['role'],"#64748b")
        rb = ROLE_BG.get(v['role'],"#f1f5f9")
        rows_html += f"""<tr style="background:{bg}">
            <td style="{TD}font-weight:700;font-family:monospace;color:#2563eb;">{u}</td>
            <td style="{TD}">{v['name']}</td>
            <td style="{TD}"><span class="badge" style="background:{rb};color:{rc};">{v['role']}</span></td>
            <td style="{TD}font-size:12px;color:#64748b;">{ROLE_DESC.get(v['role'],'')}</td>
        </tr>"""
    st.markdown(f"""
    <table class="styled-table">
        <thead><tr>
            <th style="{TH}">Username</th><th style="{TH}">Full Name</th>
            <th style="{TH}">Role</th><th style="{TH}">Access Level</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)
    card_end()

    with st.expander("⚠️ Danger Zone — Reset Database"):
        st.warning("⚠️ **Warning:** This will permanently delete all data and restore sample records. This action cannot be undone.")
        if st.button("🗑 Reset All Data to Sample Data", type="primary", key="reset_data"):
            for key,df in SEED.items():
                df.astype(str).fillna("").to_csv(FILES[key],index=False)
            st.session_state.data = load_data()
            st.success("✅ Database has been reset to sample records successfully.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    show_footer()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    render_sidebar()

    menu = st.session_state.menu
    PAGES = {
        "Dashboard":     page_dashboard,
        "Orders":        page_orders,
        "New Order":     page_new_order,
        "Update Order":  page_update_order,
        "Order Details": page_order_details,
        "Activity Log":  page_activity_log,
        "Reports":       page_reports,
        "Admin":         page_admin,
    }

    allowed = ROLE_MENUS.get(st.session_state.role, [])
    if menu not in allowed:
        st.session_state.menu = "Dashboard"
        st.rerun()

    if menu in PAGES:
        PAGES[menu]()

if __name__ == "__main__":
    main()
