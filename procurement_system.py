import streamlit as st
import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be FIRST st call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title  = "Supply Chain Tracking System",
    page_icon   = "🏭",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
COMPANIES  = ["Robokart", "Bharat Tech", "EL"]
STATUSES   = ["Pending","Procured","Dispatched","Delivered","Invoiced","Paid"]
PRIORITIES = ["Low","Medium","High","Urgent"]

S_EMOJI = {"Pending":"⏳","Procured":"🔧","Dispatched":"🚚","Delivered":"📦","Invoiced":"🧾","Paid":"💰"}
S_BG    = {"Pending":"#fef3c7","Procured":"#dbeafe","Dispatched":"#ede9fe",
           "Delivered":"#d1fae5","Invoiced":"#cffafe","Paid":"#dcfce7"}
S_FG    = {"Pending":"#92400e","Procured":"#1e40af","Dispatched":"#5b21b6",
           "Delivered":"#065f46","Invoiced":"#155e75","Paid":"#14532d"}
P_BG    = {"Low":"#f1f5f9","Medium":"#dbeafe","High":"#fef9c3","Urgent":"#fee2e2"}
P_FG    = {"Low":"#475569","Medium":"#1e40af","High":"#92400e","Urgent":"#dc2626"}
C_BG    = {"Robokart":"#ede9fe","Bharat Tech":"#cffafe","EL":"#ffedd5"}
C_FG    = {"Robokart":"#5b21b6","Bharat Tech":"#155e75","EL":"#9a3412"}

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
R_COLOR = {"Admin":"#dc2626","Manager":"#d97706","Staff":"#2563eb","Viewer":"#059669"}
R_BG    = {"Admin":"#fee2e2","Manager":"#fef3c7","Staff":"#dbeafe","Viewer":"#dcfce7"}

# ─────────────────────────────────────────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────────────────────────────────────────
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
FILES = {k: f"{DATA_DIR}/{k}.csv" for k in
         ["orders","procurement","dispatch","delivery","invoices","activity_log"]}

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
    for k, path in FILES.items():
        if os.path.exists(path):
            out[k] = pd.read_csv(path, dtype=str).fillna("")
        else:
            df = SEED[k].copy().astype(str).fillna("")
            df.to_csv(path, index=False)
            out[k] = df
    return out

def save_tbl(k): st.session_state.data[k].to_csv(FILES[k], index=False)

def add_log(oid, action, prev, nw, by, details):
    D = st.session_state.data
    row = pd.DataFrame([{"id":str(len(D["activity_log"])+1),"order_id":oid,
                         "action_type":action,"previous_status":prev,"new_status":nw,
                         "performed_by":by,"performed_at":now_ist(),"details":details}])
    D["activity_log"] = pd.concat([D["activity_log"],row],ignore_index=True)
    save_tbl("activity_log")

def set_status(oid, ns):
    D = st.session_state.data
    D["orders"].loc[D["orders"]["order_id"]==oid,"current_status"] = ns
    D["orders"].loc[D["orders"]["order_id"]==oid,"last_updated"]   = now_ist()
    save_tbl("orders")

def get_order(oid):
    r = st.session_state.data["orders"]
    r = r[r["order_id"]==oid]
    return r.iloc[0] if len(r) else None

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = [("logged_in",False),("username",""),("role",""),("user_name",""),
            ("menu","Dashboard"),("co_filter","All")]
for k,v in DEFAULTS:
    if k not in st.session_state:
        st.session_state[k] = v
if "data" not in st.session_state:
    st.session_state.data = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# MASTER CSS  — one block, covers login + app, highest specificity everywhere
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ══ Base ══════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background: #f1f5f9 !important;
    color: #1e293b !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }

/* ══ INPUT FIELDS — nuclear specificity, works on login + app ════════════════
   Using every possible selector combination to guarantee white bg + dark text
   regardless of Streamlit theme or any other CSS.
   ═══════════════════════════════════════════════════════════════════════════ */
input,
input[type],
input[type="text"],
input[type="password"],
input[type="number"],
input[type="email"],
input[type="search"],
textarea,
[data-baseweb="input"] input,
[data-baseweb="base-input"] input,
.stTextInput input,
.stTextInput > div > div > input,
.stTextArea textarea,
.stTextArea > div > div > textarea,
.stNumberInput input,
.stNumberInput > div > div > input,
.stDateInput input,
.stDateInput > div > div > input {
    background-color: #ffffff !important;
    background:       #ffffff !important;
    color:            #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color:      #111827 !important;
    border:           1.5px solid #cbd5e1 !important;
    border-radius:    8px !important;
    font-size:        14px !important;
    font-family:      'Inter', sans-serif !important;
    opacity:          1 !important;
}
input::placeholder, textarea::placeholder,
input[type="text"]::placeholder,
input[type="password"]::placeholder,
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color:                   #9ca3af !important;
    -webkit-text-fill-color: #9ca3af !important;
    opacity:                 1 !important;
}
input:focus, textarea:focus,
input[type="text"]:focus, input[type="password"]:focus,
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color:    #3b82f6 !important;
    box-shadow:      0 0 0 3px rgba(59,130,246,0.18) !important;
    outline:         none !important;
    background:      #ffffff !important;
    color:           #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
/* Wrapper divs that hold inputs must also be white */
[data-baseweb="input"],
[data-baseweb="base-input"],
.stTextInput > div > div,
.stTextArea  > div > div,
.stNumberInput > div > div,
.stDateInput   > div > div {
    background: #ffffff !important;
    border-radius: 8px !important;
}

/* Selectbox */
[data-baseweb="select"],
[data-baseweb="select"] > div,
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
    background:    #ffffff !important;
    border:        1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color:         #111827 !important;
}

/* Form field labels — everywhere */
label,
.stTextInput  label,
.stTextArea   label,
.stSelectbox  label,
.stNumberInput label,
.stDateInput   label,
.stFileUploader label,
.stCheckbox    label {
    color:          #374151 !important;
    font-size:      12.5px !important;
    font-weight:    600 !important;
    letter-spacing: 0.01em !important;
}

/* ══ SIDEBAR ═══════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background:  #0f172a !important;
    min-width:   240px !important;
    max-width:   240px !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding:    0 !important;
    min-height: 100vh;
}
/* Override ALL text color inside sidebar */
[data-testid="stSidebar"] *:not(button):not(button *) {
    color: #94a3b8 !important;
}
/* Nav buttons */
[data-testid="stSidebar"] .stButton > button {
    width:         100% !important;
    text-align:    left !important;
    background:    transparent !important;
    border:        none !important;
    border-radius: 8px !important;
    color:         #94a3b8 !important;
    font-size:     13.5px !important;
    font-weight:   500 !important;
    padding:       10px 16px !important;
    margin:        1px 8px !important;
    width:         calc(100% - 16px) !important;
    transition:    background 0.15s, color 0.15s !important;
    box-shadow:    none !important;
    -webkit-text-fill-color: #94a3b8 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.07) !important;
    color:      #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background:  #1d4ed8 !important;
    color:       #ffffff !important;
    font-weight: 700 !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #2563eb !important;
}
/* Sign-out */
[data-testid="stSidebar"] .signout-btn button {
    color:   #f87171 !important;
    border:  1px solid rgba(248,113,113,0.3) !important;
    background: rgba(220,38,38,0.08) !important;
    -webkit-text-fill-color: #f87171 !important;
}

/* ══ BUTTONS (main area) ══════════════════════════════════════════════════ */
.stButton > button {
    border-radius: 8px !important;
    font-weight:   600 !important;
    font-size:     13px !important;
    padding:       9px 20px !important;
    cursor:        pointer !important;
    border:        1.5px solid transparent !important;
    transition:    all 0.15s !important;
}
.stButton > button[kind="primary"] {
    background:   #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    color:        #fff !important;
    -webkit-text-fill-color: #fff !important;
}
.stButton > button[kind="primary"]:hover { background: #1e40af !important; }
.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    border:     1.5px solid #e2e8f0 !important;
    color:      #374151 !important;
}
.stButton > button[kind="secondary"]:hover { background: #f8fafc !important; }

/* ══ TABS ═════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background:   transparent !important;
    border-bottom: 2px solid #e2e8f0 !important;
    gap:   0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background:    transparent !important;
    border:        none !important;
    border-bottom: 2px solid transparent !important;
    color:         #64748b !important;
    font-weight:   500 !important;
    font-size:     13px !important;
    padding:       10px 22px !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    border-bottom: 2px solid #1d4ed8 !important;
    color:         #1d4ed8 !important;
    font-weight:   700 !important;
}

/* ══ ALERTS ═══════════════════════════════════════════════════════════════ */
.stAlert, .stSuccess, .stError, .stInfo, .stWarning { border-radius: 8px !important; }

/* ══ EXPANDER ════════════════════════════════════════════════════════════ */
.streamlit-expanderHeader {
    background:  #f8fafc !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ══ MISC ════════════════════════════════════════════════════════════════ */
hr { border-color: #e2e8f0 !important; margin: 14px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def sbadge(s):
    bg=S_BG.get(s,"#f1f5f9"); fg=S_FG.get(s,"#475569")
    return f'<span style="display:inline-block;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;background:{bg};color:{fg};white-space:nowrap;">{S_EMOJI.get(s,"")} {s}</span>'

def pbadge(p):
    bg=P_BG.get(p,"#f1f5f9"); fg=P_FG.get(p,"#475569")
    return f'<span style="display:inline-block;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;background:{bg};color:{fg};">{p}</span>'

def cobadge(c):
    bg=C_BG.get(c,"#f1f5f9"); fg=C_FG.get(c,"#475569")
    return f'<span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;background:{bg};color:{fg};">{c}</span>'

def sp(px=12):
    st.markdown(f'<div style="height:{px}px"></div>', unsafe_allow_html=True)

def topbar(title, sub=""):
    today = datetime.now().strftime("%d %b %Y")
    s = f'<div style="font-size:12px;color:#64748b;margin-top:3px;">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div style="background:#fff;border-bottom:1px solid #e2e8f0;padding:14px 28px;
                display:flex;justify-content:space-between;align-items:center;
                box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div>
            <div style="font-size:18px;font-weight:800;color:#0f172a;">{title}</div>
            {s}
        </div>
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="display:flex;align-items:center;gap:6px;background:#f0fdf4;
                        border:1px solid #bbf7d0;border-radius:20px;padding:5px 14px;
                        font-size:11.5px;font-weight:600;color:#15803d;">
                <div style="width:7px;height:7px;border-radius:50%;background:#22c55e;"></div>
                Auto-saved
            </div>
            <div style="font-size:12px;color:#64748b;font-weight:500;">📅 {today}</div>
        </div>
    </div>
    <div style="height:24px;background:#f1f5f9;"></div>
    """, unsafe_allow_html=True)

def footer():
    st.markdown(
        f'<div style="text-align:center;font-size:11px;color:#94a3b8;padding:18px 0 10px;'
        f'border-top:1px solid #e2e8f0;margin-top:36px;">'
        f'© {datetime.now().year} Robokart &nbsp;·&nbsp; Supply Chain Tracking System</div>',
        unsafe_allow_html=True)

def sec_label(t):
    st.markdown(f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:0.8px;color:#94a3b8;border-bottom:1px solid #f1f5f9;'
                f'padding-bottom:8px;margin:12px 0 14px;">{t}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN PAGE
# The trick: render the page with the sidebar COLLAPSED on login
# We inject CSS only for the login state to hide sidebar.
# Form inputs are native Streamlit — they pick up the master CSS above.
# ─────────────────────────────────────────────────────────────────────────────
def login_page():
    # Hide sidebar on login page only
    st.markdown("""
    <style>
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .stApp {
        background: linear-gradient(135deg, #0c1426 0%, #1e3a5f 50%, #0c1426 100%) !important;
    }
    /* Extra insurance for login input fields */
    input, input[type="text"], input[type="password"] {
        background-color: #ffffff !important;
        background:       #ffffff !important;
        color:            #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        border: 1.5px solid #d1d5db !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        height: 46px !important;
    }
    /* Login Sign In button — red like reference screenshot */
    [data-testid="stForm"] button[kind="primaryFormSubmit"],
    [data-testid="stForm"] .stButton > button,
    [data-testid="stForm"] .stButton > button[kind="primary"] {
        background:   #e53e3e !important;
        border-color: #e53e3e !important;
        color:        #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size:    15px !important;
        font-weight:  700 !important;
        height:       50px !important;
        border-radius: 8px !important;
    }
    [data-testid="stForm"] .stButton > button:hover { background: #c53030 !important; }
    </style>
    """, unsafe_allow_html=True)

    # Center vertically with spacer
    st.markdown('<div style="height:60px"></div>', unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.25, 1])
    with col:

        # ── TOP HALF: pure HTML branding card ──────────────────────
        st.markdown("""
        <div style="
            background:#ffffff;
            border:1px solid #e2e8f0;
            border-bottom:none;
            border-radius:16px 16px 0 0;
            padding:40px 36px 28px;
            text-align:center;
        ">
            <div style="
                width:76px;height:76px;border-radius:18px;
                background:linear-gradient(135deg,#1e3a5f 0%,#1d4ed8 100%);
                display:flex;align-items:center;justify-content:center;
                font-size:38px;margin:0 auto 18px;
                box-shadow:0 6px 20px rgba(29,78,216,0.35);
            ">🏭</div>
            <div style="font-size:21px;font-weight:800;color:#0f172a;line-height:1.3;">
                Supply Chain Tracking System
            </div>
            <div style="font-size:13px;color:#64748b;margin-top:8px;">
                Enterprise Procurement &amp; Order Management
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── BOTTOM HALF: divider strip + Streamlit form ─────────────
        # NOTE: We do NOT wrap the form inside any HTML div.
        # The form itself is styled via [data-testid="stForm"] in CSS above.
        st.markdown("""
        <div style="
            background:#ffffff;
            border:1px solid #e2e8f0;
            border-top:1px solid #f1f5f9;
            border-radius:0 0 16px 16px;
            padding:24px 36px 8px;
            box-shadow:0 20px 60px rgba(0,0,0,0.4);
            margin-bottom:4px;
        ">
            <div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:4px;">
                Sign in to your account
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            uname = st.text_input("Username", placeholder="Enter your username")
            pword = st.text_input("Password", type="password", placeholder="Enter your password")
            sp(6)
            submit = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

        if submit:
            if uname in USERS and USERS[uname]["password"] == pword:
                st.session_state.logged_in = True
                st.session_state.username  = uname
                st.session_state.role      = USERS[uname]["role"]
                st.session_state.user_name = USERS[uname]["name"]
                st.session_state.menu      = "Dashboard"
                st.rerun()
            else:
                st.error("⚠ Invalid username or password. Please try again.")

        st.markdown("""
        <p style="text-align:center;font-size:12px;color:#94a3b8;margin-top:16px;">
            🔒 Secure access · Contact administrator for credentials
        </p>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="padding:22px 18px 18px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:38px;height:38px;border-radius:9px;flex-shrink:0;
                            background:linear-gradient(135deg,#1e3a5f,#1d4ed8);
                            display:flex;align-items:center;justify-content:center;
                            font-size:20px;box-shadow:0 2px 8px rgba(29,78,216,0.4);">🏭</div>
                <div>
                    <div style="font-size:14px;font-weight:800;color:#f8fafc;">Supply Chain</div>
                    <div style="font-size:9px;color:#475569;letter-spacing:1.2px;
                                text-transform:uppercase;margin-top:1px;">Tracking System</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        sp(10)
        st.markdown('<div style="padding:0 18px;font-size:9.5px;font-weight:700;letter-spacing:1.2px;'
                    'color:#334155;text-transform:uppercase;margin-bottom:6px;">Navigation</div>',
                    unsafe_allow_html=True)

        # Nav items
        for m in ROLE_MENUS.get(st.session_state.role, []):
            active = (st.session_state.menu == m)
            if st.button(f"{MENU_ICONS.get(m,'')}  {m}",
                         key=f"nav_{m}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.menu = m
                st.rerun()

        sp(14)
        st.markdown('<div style="height:1px;background:#1e293b;margin:0 16px 14px;"></div>',
                    unsafe_allow_html=True)

        # User card
        role     = st.session_state.role
        rc       = R_COLOR.get(role,"#64748b")
        rb       = R_BG.get(role,"#1e293b")
        initials = "".join(x[0].upper() for x in st.session_state.user_name.split()[:2])
        st.markdown(f"""
        <div style="padding:0 14px;margin-bottom:10px;">
          <div style="background:#1e293b;border-radius:10px;padding:12px 14px;
                      display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;border-radius:8px;flex-shrink:0;
                        background:{rc};color:#fff;font-size:13px;font-weight:800;
                        display:flex;align-items:center;justify-content:center;">{initials}</div>
            <div style="overflow:hidden;">
              <div style="font-size:12.5px;font-weight:700;color:#f1f5f9;
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                  {st.session_state.user_name}</div>
              <span style="font-size:10px;font-weight:700;background:{rb};
                           color:{rc};padding:1px 8px;border-radius:4px;">{role}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Sign out
        st.markdown('<div class="signout-btn">', unsafe_allow_html=True)
        if st.button("⬅ Sign Out", use_container_width=True, key="signout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        sp(10)

# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
def page_dashboard():
    topbar("📊 Dashboard", "Real-time overview of all purchase orders and supply chain status")
    D   = st.session_state.data
    df  = D["orders"].copy()
    cf  = st.session_state.co_filter
    fil = df if cf=="All" else df[df["company"]==cf]
    tv  = fil["total_value"].astype(float).sum() if len(fil) else 0.0
    P   = "padding:0 28px;"

    # ── KPI Metrics ──────────────────────────────────────────────────────────
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    kpis = [
        ("Total Orders",  len(fil),                                                               "#1d4ed8"),
        ("Pending",       len(fil[fil["current_status"]=="Pending"]),                             "#d97706"),
        ("In Transit",    len(fil[fil["current_status"].isin(["Procured","Dispatched"])]),        "#7c3aed"),
        ("Delivered",     len(fil[fil["current_status"].isin(["Delivered","Invoiced","Paid"])]),  "#059669"),
        ("Paid",          len(fil[fil["current_status"]=="Paid"]),                                "#0891b2"),
        ("Total Value",   f"₹{tv/100000:.1f}L",                                                   "#c2410c"),
    ]
    cols = st.columns(6, gap="small")
    for col,(label,val,color) in zip(cols,kpis):
        with col:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                        padding:18px 16px 16px;box-shadow:0 1px 4px rgba(0,0,0,0.05);
                        position:relative;overflow:hidden;">
                <div style="position:absolute;top:0;left:0;right:0;height:3px;
                            background:{color};border-radius:12px 12px 0 0;"></div>
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.8px;color:#64748b;margin-bottom:10px;">{label}</div>
                <div style="font-size:28px;font-weight:800;color:{color};line-height:1;">{val}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    sp(22)

    # ── Company Filter ────────────────────────────────────────────────────────
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    fc1,fc2,fc3,fc4,_ = st.columns([1.6,1.1,1.4,0.8,3], gap="small")
    for col,label,key in [
        (fc1,"🏢 All Companies","All"),
        (fc2,"Robokart","Robokart"),
        (fc3,"Bharat Tech","Bharat Tech"),
        (fc4,"EL","EL"),
    ]:
        with col:
            lbl = label+(" ✓" if cf==key else "")
            if st.button(lbl,key=f"cf_{key}",
                         type="primary" if cf==key else "secondary",
                         use_container_width=True):
                st.session_state.co_filter = key; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    sp(20)

    # ── Orders Table ──────────────────────────────────────────────────────────
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    label_text = "All Orders" if cf=="All" else f"{cf} Orders"
    TH = ("padding:11px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
          "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
          "border-bottom:2px solid #e2e8f0;text-align:left;white-space:nowrap;")
    TD = "padding:13px 16px;border-bottom:1px solid #f1f5f9;color:#1e293b;vertical-align:middle;"

    if len(fil)==0:
        tbody='<tr><td colspan="10" style="padding:32px;text-align:center;color:#94a3b8;">No orders found.</td></tr>'
    else:
        tbody=""
        for i,(_,r) in enumerate(fil.iterrows()):
            bg   = "#ffffff" if i%2==0 else "#fafbfc"
            desc = str(r["item_description"])
            desc = desc[:40]+"…" if len(desc)>40 else desc
            tbody+=f"""<tr style="background:{bg}">
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
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
      <div style="display:flex;justify-content:space-between;align-items:center;
                  padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">📦 {label_text}</div>
        <div style="font-size:11px;font-weight:600;color:#64748b;background:#f1f5f9;
                    padding:3px 12px;border-radius:20px;">{len(fil)} orders</div>
      </div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead><tr>
            <th style="{TH}">Order ID</th><th style="{TH}">Company</th>
            <th style="{TH}">PO Number</th><th style="{TH}">Department</th>
            <th style="{TH}">Description</th><th style="{TH}">Qty</th>
            <th style="{TH}">Value</th><th style="{TH}">Priority</th>
            <th style="{TH}">Status</th><th style="{TH}">Last Updated</th>
          </tr></thead>
          <tbody>{tbody}</tbody>
        </table>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    sp(8)
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)
    footer()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NEW ORDER
# ─────────────────────────────────────────────────────────────────────────────
def page_new_order():
    topbar("➕ New Order", "Create a new government purchase order")
    D = st.session_state.data
    P = "padding:0 28px;"
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);
                max-width:860px;margin-bottom:20px;">
      <div style="padding:16px 24px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">📝 Purchase Order Details</div>
        <div style="font-size:12px;color:#64748b;margin-top:3px;">All fields marked * are required</div>
      </div>
      <div style="padding:24px;">
    """, unsafe_allow_html=True)

    with st.form("new_order_form", clear_on_submit=True):
        sec_label("Company & Classification")
        c1,c2 = st.columns(2)
        with c1: company  = st.selectbox("Company *", COMPANIES)
        with c2: priority = st.selectbox("Priority *", PRIORITIES, index=1)

        c3,c4 = st.columns(2)
        with c3: govt_dept = st.text_input("Govt Department *", placeholder="e.g. Education Department Delhi")
        with c4: po_num    = st.text_input("PO Number *", placeholder="e.g. PO/EDU/2026/001")

        sec_label("Contact Information")
        c5,c6 = st.columns(2)
        with c5: contact_name = st.text_input("Contact Person *", placeholder="e.g. Mr. Rajesh Kumar")
        with c6: contact_ph   = st.text_input("Contact Phone",    placeholder="e.g. 9876543210")

        sec_label("Order Details")
        c7,c8 = st.columns(2)
        with c7:
            qty = st.number_input("Quantity *", min_value=1, value=1)
            val = st.number_input("Total Value (₹) *", min_value=0, value=0)
        with c8:
            assigned = st.text_input("Assigned Company", placeholder="e.g. Tech Solutions Pvt Ltd")
            exp_del  = st.date_input("Expected Delivery Date")

        item_desc = st.text_area("Item Description *",
                                  placeholder="Detailed description of goods/services…", height=88)
        remarks   = st.text_area("Remarks / Special Instructions",
                                  placeholder="Any additional notes…", height=66)
        sp(6)
        sub_col, _ = st.columns([1,2])
        with sub_col:
            submitted = st.form_submit_button("🚀 Create Purchase Order",
                                               type="primary", use_container_width=True)
        if submitted:
            errs = [f for f,v in [("Govt Dept",govt_dept),("PO Number",po_num),
                                   ("Contact Person",contact_name),("Item Description",item_desc),
                                   ("Total Value",val)] if not v]
            if errs:
                st.error(f"Missing required fields: {', '.join(errs)}")
            elif po_num in D["orders"]["po_number"].values:
                st.error("⚠ PO Number already exists.")
            else:
                ts  = now_ist()
                oid = f"ORD-{ts[:10]}-{str(len(D['orders'])+1).zfill(3)}"
                new = pd.DataFrame([{
                    "order_id":oid,"date_created":ts,"company":company,
                    "govt_department":govt_dept,"contact_person":contact_name,
                    "contact_phone":contact_ph,"po_number":po_num,
                    "item_description":item_desc,"quantity":str(qty),
                    "total_value":str(val),"assigned_company":assigned,
                    "current_status":"Pending","priority":priority,
                    "expected_delivery_date":str(exp_del),
                    "remarks":remarks,"created_by":st.session_state.user_name,"last_updated":ts
                }])
                D["orders"] = pd.concat([D["orders"],new],ignore_index=True)
                save_tbl("orders")
                add_log(oid,"ORDER_CREATED","—","Pending",st.session_state.user_name,
                        f"Order created — {company} | {po_num}")
                st.success(f"✅ Order **{oid}** created successfully!")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ─────────────────────────────────────────────────────────────────────────────
# UPDATE ORDER
# ─────────────────────────────────────────────────────────────────────────────
def page_update_order():
    topbar("🔄 Update Order", "Update procurement, dispatch, delivery or invoice status")
    D = st.session_state.data
    P = "padding:0 28px;"
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  [{r['current_status']}]"
        for _,r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order *", opts, key="uo_sel")

    if sel == "— Select an order —":
        st.info("👆 Select an order above to begin updating its status.")
        st.markdown('</div>', unsafe_allow_html=True); footer(); return

    oid   = sel.split("  ·  ")[0].strip()
    order = get_order(oid)

    # Summary bar
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
                gap:12px;background:#f8fafc;border:1px solid #e2e8f0;
                border-radius:10px;padding:14px 18px;margin:12px 0 18px;">
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Order ID</div>
             <div style="font-size:13px;font-weight:700;color:#1d4ed8;">{order['order_id']}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Company</div>
             <div>{cobadge(order['company'])}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Status</div>
             <div>{sbadge(order['current_status'])}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Priority</div>
             <div>{pbadge(order['priority'])}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Value</div>
             <div style="font-size:14px;font-weight:800;">₹{float(order['total_value']):,.0f}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Department</div>
             <div style="font-size:12.5px;font-weight:600;">{order['govt_department']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    updated_by = st.text_input("Your Name / Department *",
                                placeholder="e.g. Rahul — Logistics Team", key="uo_by")
    sp(4)

    def fcard(title):
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                    overflow:hidden;max-width:720px;margin-bottom:16px;">
          <div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
            <div style="font-size:13.5px;font-weight:700;color:#0f172a;">{title}</div>
          </div><div style="padding:22px;">
        """, unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["🔧  Procurement","🚚  Dispatch","📦  Delivery","💰  Invoice & Payment"])

    with t1:
        fcard("Procurement Details")
        with st.form("proc_form"):
            c1,c2=st.columns(2)
            with c1:
                p_stat = st.selectbox("Procurement Status *",["","Not Started","In Progress","Completed","On Hold"])
                p_date = st.date_input("Procurement Date")
            with c2:
                p_qc  = st.selectbox("Quality Check Status",["","Pending","In Progress","Passed","Failed"])
                p_src = st.text_input("Materials Source", placeholder="Vendor / Warehouse")
            p_notes = st.text_area("Notes", height=75)
            sv = st.form_submit_button("✅ Save Procurement", type="primary")
            if sv:
                if not updated_by: st.error("Enter your name above the tabs.")
                else:
                    ts=now_ist()
                    D["procurement"]=pd.concat([D["procurement"],pd.DataFrame([{
                        "id":str(len(D["procurement"])+1),"order_id":oid,
                        "procurement_status":p_stat,"procurement_date":str(p_date),
                        "materials_source":p_src,"quality_check_status":p_qc,
                        "notes":p_notes,"updated_by":updated_by,"updated_at":ts
                    }])],ignore_index=True); save_tbl("procurement")
                    ns="Procured" if p_stat=="Completed" else order["current_status"]
                    set_status(oid,ns)
                    add_log(oid,"STATUS_CHANGE",order["current_status"],ns,updated_by,f"Procurement: {p_stat}")
                    st.success(f"✅ Saved! Status → **{ns}**"); st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    with t2:
        fcard("Dispatch Details")
        with st.form("disp_form"):
            c1,c2=st.columns(2)
            with c1:
                d_date=st.date_input("Dispatch Date")
                d_cour=st.text_input("Courier / Transporter *", placeholder="e.g. BlueDart, DTDC")
                d_veh =st.text_input("Vehicle Number", placeholder="e.g. DL01AB1234")
            with c2:
                d_drv =st.text_input("Driver Contact", placeholder="e.g. 9111222333")
                d_trk =st.text_input("Tracking Number", placeholder="e.g. BD123456789")
                d_exp =st.date_input("Expected Delivery")
            sv=st.form_submit_button("✅ Save Dispatch", type="primary")
            if sv:
                if not updated_by: st.error("Enter your name above the tabs.")
                else:
                    ts=now_ist()
                    D["dispatch"]=pd.concat([D["dispatch"],pd.DataFrame([{
                        "id":str(len(D["dispatch"])+1),"order_id":oid,
                        "dispatch_date":str(d_date),"courier_name":d_cour,
                        "vehicle_number":d_veh,"driver_contact":d_drv,
                        "tracking_number":d_trk,"expected_delivery_date":str(d_exp),
                        "updated_by":updated_by,"updated_at":ts
                    }])],ignore_index=True); save_tbl("dispatch")
                    set_status(oid,"Dispatched")
                    add_log(oid,"STATUS_CHANGE",order["current_status"],"Dispatched",updated_by,f"Dispatched via {d_cour}")
                    st.success("✅ Dispatch saved! Status → **Dispatched**"); st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    with t3:
        fcard("Delivery Confirmation")
        with st.form("del_form"):
            c1,c2=st.columns(2)
            with c1:
                de_stat=st.selectbox("Delivery Status *",["","Delivered","Partial","Failed","Rescheduled"])
                de_date=st.date_input("Delivery Date")
                de_recv=st.text_input("Receiver Name", placeholder="Person who received goods")
            with c2:
                de_qty=st.number_input("Delivered Quantity",min_value=0)
                de_ch =st.text_input("Challan Number", placeholder="e.g. CH-EDU-001")
            st.markdown("**Delivery Proof** *(photos, PDFs)*")
            del_f=st.file_uploader("Upload",accept_multiple_files=True,key="dlf",label_visibility="collapsed")
            st.markdown("**Challan Documents**")
            ch_f =st.file_uploader("Upload",accept_multiple_files=True,key="chf",label_visibility="collapsed")
            sv=st.form_submit_button("✅ Save Delivery", type="primary")
            if sv:
                if not updated_by: st.error("Enter your name above the tabs.")
                else:
                    ts=now_ist()
                    D["delivery"]=pd.concat([D["delivery"],pd.DataFrame([{
                        "id":str(len(D["delivery"])+1),"order_id":oid,
                        "delivery_status":de_stat,"delivery_date":str(de_date),
                        "receiver_name":de_recv,"delivered_quantity":str(de_qty),
                        "challan_number":de_ch,
                        "delivery_files":f"{len(del_f or [])} file(s)",
                        "challan_files":f"{len(ch_f or [])} file(s)",
                        "updated_by":updated_by,"updated_at":ts
                    }])],ignore_index=True); save_tbl("delivery")
                    ns="Delivered" if de_stat=="Delivered" else order["current_status"]
                    set_status(oid,ns)
                    add_log(oid,"STATUS_CHANGE",order["current_status"],ns,updated_by,
                            f"Delivery: {de_stat} | {len(del_f or [])+len(ch_f or [])} files")
                    st.success(f"✅ Delivery saved! Status → **{ns}**"); st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    with t4:
        fcard("Invoice & Payment Details")
        with st.form("inv_form"):
            c1,c2=st.columns(2)
            with c1:
                i_num  =st.text_input("Invoice Number", placeholder="e.g. INV-2026-0001")
                i_date =st.date_input("Invoice Date")
                i_amt  =st.number_input("Invoice Amount (₹)",min_value=0)
                i_pstat=st.selectbox("Payment Status *",["","Pending","Approved","Completed"])
            with c2:
                i_pmode=st.selectbox("Payment Mode",["","NEFT","RTGS","Cheque","DD","Online","Cash"])
                i_txn  =st.text_input("Transaction Reference", placeholder="TXN / UTR number")
                i_pdate=st.date_input("Payment Date")
            st.markdown("**Invoice Documents** *(PDF, Excel, scanned copies)*")
            inv_f=st.file_uploader("Upload",accept_multiple_files=True,key="ivf",label_visibility="collapsed")
            sv=st.form_submit_button("✅ Save Invoice & Payment", type="primary")
            if sv:
                if not updated_by: st.error("Enter your name above the tabs.")
                else:
                    ts=now_ist()
                    D["invoices"]=pd.concat([D["invoices"],pd.DataFrame([{
                        "id":str(len(D["invoices"])+1),"order_id":oid,
                        "invoice_number":i_num,"invoice_date":str(i_date),
                        "invoice_amount":str(i_amt),"payment_status":i_pstat,
                        "payment_date":str(i_pdate),"payment_mode":i_pmode,
                        "transaction_reference":i_txn,
                        "invoice_files":f"{len(inv_f or [])} file(s)",
                        "updated_by":updated_by,"updated_at":ts
                    }])],ignore_index=True); save_tbl("invoices")
                    ns="Paid" if i_pstat=="Completed" else "Invoiced"
                    set_status(oid,ns)
                    add_log(oid,"STATUS_CHANGE",order["current_status"],ns,updated_by,
                            f"Invoice {i_num} | {i_pstat} | {len(inv_f or [])} files")
                    st.success(f"✅ Invoice saved! Status → **{ns}**"); st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ─────────────────────────────────────────────────────────────────────────────
# ORDER DETAILS
# ─────────────────────────────────────────────────────────────────────────────
def page_order_details():
    topbar("🔍 Order Details", "Full order information, timeline and activity log")
    D = st.session_state.data
    P = "padding:0 28px;"
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  {r['current_status']}"
        for _,r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order", opts, key="od_sel")
    if sel=="— Select an order —":
        st.info("👆 Select an order to view its complete details and history.")
        st.markdown('</div>', unsafe_allow_html=True); footer(); return

    oid   = sel.split("  ·  ")[0].strip()
    order = get_order(oid)
    s     = order["current_status"]

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                padding:22px 24px;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:18px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
        <div>
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            {cobadge(order['company'])}
            <span style="font-size:18px;font-weight:800;color:#0f172a;">{order['order_id']}</span>
          </div>
          <div style="font-size:13px;color:#64748b;">{order['po_number']} · {order['govt_department']}</div>
        </div>
        <div style="display:flex;gap:8px;">{sbadge(s)} {pbadge(order['priority'])}</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));
                  gap:14px;margin-top:18px;padding-top:16px;border-top:1px solid #f1f5f9;">
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Contact</div>
             <div style="font-size:13px;font-weight:600;">{order['contact_person']}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Phone</div>
             <div style="font-size:13px;font-weight:600;">{order['contact_phone']}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Quantity</div>
             <div style="font-size:13px;font-weight:600;">{order['quantity']}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Assigned To</div>
             <div style="font-size:13px;font-weight:600;">{order['assigned_company'] or '—'}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Total Value</div>
             <div style="font-size:18px;font-weight:800;color:#0f172a;">₹{float(order['total_value']):,.0f}</div></div>
      </div>
      <div style="margin-top:14px;background:#f8fafc;border-radius:7px;border:1px solid #e2e8f0;padding:11px 14px;">
        <span style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;letter-spacing:0.5px;">Description: </span>
        <span style="font-size:13px;color:#1e293b;">{order['item_description']}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline stepper
    cur = STATUSES.index(s) if s in STATUSES else 0
    html = '<div style="display:flex;align-items:center;margin-bottom:24px;">'
    for i,step in enumerate(STATUSES):
        if i<cur:   cc,lc="#1d4ed8;color:#fff","#1d4ed8"
        elif i==cur: cc,lc="#dbeafe;border:2px solid #1d4ed8;color:#1d4ed8","#1d4ed8"
        else:        cc,lc="#f1f5f9;color:#94a3b8","#94a3b8"
        html+=f"""<div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
            <div style="width:34px;height:34px;border-radius:50%;background:{cc};
                        display:flex;align-items:center;justify-content:center;font-size:14px;">{S_EMOJI.get(step,'')}</div>
            <div style="font-size:9.5px;font-weight:600;color:{lc};margin-top:5px;text-align:center;">{step}</div>
        </div>"""
        if i<len(STATUSES)-1:
            lbg="#1d4ed8" if i<cur else "#e2e8f0"
            html+=f'<div style="flex:1;height:2px;background:{lbg};margin:0 4px 18px;"></div>'
    html+="</div>"
    st.markdown(html, unsafe_allow_html=True)

    def show_rec(table):
        rows = D[table][D[table]["order_id"]==oid]
        if len(rows)==0: st.info("No data recorded yet for this stage."); return
        row   = rows.iloc[-1]
        items = [(c.replace("_"," ").title(),str(row[c]))
                 for c in row.index if c not in ["id","order_id"] and str(row[c]) not in ["","nan"]]
        for i in range(0,len(items),3):
            chunk=items[i:i+3]; cs=st.columns(3)
            for col,(lbl,val) in zip(cs,chunk):
                with col:
                    st.markdown(f"""
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
                                padding:11px 14px;margin-bottom:10px;">
                        <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                                    color:#64748b;margin-bottom:4px;">{lbl}</div>
                        <div style="font-size:13px;font-weight:600;color:#0f172a;">{val}</div>
                    </div>""", unsafe_allow_html=True)

    t1,t2,t3,t4,t5 = st.tabs(["🔧 Procurement","🚚 Dispatch","📦 Delivery","💰 Invoice","📋 Activity"])
    with t1: show_rec("procurement")
    with t2: show_rec("dispatch")
    with t3: show_rec("delivery")
    with t4: show_rec("invoices")
    with t5:
        logs = D["activity_log"][D["activity_log"]["order_id"]==oid].copy().iloc[::-1]
        if len(logs)==0: st.info("No activity recorded yet.")
        for _,log in logs.iterrows():
            prev=log.get("previous_status",""); ns_l=log.get("new_status","")
            pb = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8">—</span>'
            nb = ("&nbsp;→&nbsp;"+sbadge(ns_l)) if ns_l and ns_l not in ["nan",""] else ""
            st.markdown(f"""
            <div style="display:flex;gap:12px;background:#fff;border:1px solid #e2e8f0;
                        border-radius:10px;padding:13px 16px;margin-bottom:8px;">
              <div style="width:9px;height:9px;border-radius:50%;background:#3b82f6;flex-shrink:0;margin-top:4px;"></div>
              <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">
                  <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                    <span style="font-size:11.5px;font-weight:700;background:#f1f5f9;
                                 padding:2px 8px;border-radius:5px;">{log['action_type']}</span>
                    {pb}{nb}
                  </div>
                  <span style="font-size:11px;color:#94a3b8;">{log['performed_at']}</span>
                </div>
                <div style="font-size:12.5px;color:#374151;margin-top:5px;">
                    {log['details']} — <b>{log['performed_by']}</b></div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ─────────────────────────────────────────────────────────────────────────────
# ACTIVITY LOG
# ─────────────────────────────────────────────────────────────────────────────
def page_activity_log():
    topbar("📋 Activity Log","Complete audit trail of all order changes and updates")
    D    = st.session_state.data
    logs = D["activity_log"].copy().iloc[::-1].reset_index(drop=True)
    P    = "padding:0 28px;"
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
      <div style="display:flex;justify-content:space-between;align-items:center;
                  padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">📋 All System Events</div>
        <div style="font-size:11px;font-weight:600;color:#64748b;background:#f1f5f9;
                    padding:3px 12px;border-radius:20px;">{len(logs)} events</div>
      </div>
      <div style="padding:16px;">
    """, unsafe_allow_html=True)

    for _,log in logs.iterrows():
        prev=log.get("previous_status",""); ns_l=log.get("new_status","")
        pb = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8">—</span>'
        nb = ("&nbsp;→&nbsp;"+sbadge(ns_l)) if ns_l and ns_l not in ["nan",""] else ""
        st.markdown(f"""
        <div style="display:flex;gap:12px;background:#fff;border:1px solid #e2e8f0;
                    border-radius:10px;padding:13px 16px;margin-bottom:8px;">
          <div style="width:9px;height:9px;border-radius:50%;background:#3b82f6;
                      flex-shrink:0;margin-top:4px;"></div>
          <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">
              <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
                <span style="font-size:11.5px;font-weight:700;background:#f1f5f9;
                             padding:2px 8px;border-radius:5px;">{log['action_type']}</span>
                <span style="font-size:12px;font-weight:700;color:#1d4ed8;">{log['order_id']}</span>
                {pb}{nb}
              </div>
              <span style="font-size:11px;color:#94a3b8;white-space:nowrap;">{log['performed_at']}</span>
            </div>
            <div style="font-size:12.5px;color:#374151;margin-top:5px;">
                {log['details']} — <b>{log['performed_by']}</b></div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ─────────────────────────────────────────────────────────────────────────────
# REPORTS
# ─────────────────────────────────────────────────────────────────────────────
def page_reports():
    topbar("📈 Reports","Financial summaries and order analytics")
    D  = st.session_state.data
    df = D["orders"].copy()
    df["total_value"] = df["total_value"].astype(float)
    P  = "padding:0 28px;"
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    c1,c2 = st.columns(2,gap="medium")
    def prog_card(title,items,key_bg,key_fg,label_fn,val_fn):
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                    overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;">
          <div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
            <div style="font-size:14px;font-weight:700;color:#0f172a;">{title}</div>
          </div><div style="padding:18px;">
        """, unsafe_allow_html=True)
        for it in items:
            lbl = label_fn(it); val = val_fn(it,df)
            pct = int(len(df[df["company"]==it])/max(len(df),1)*100) if "company" in df.columns and it in COMPANIES \
                  else int(len(df[df["current_status"]==it])/max(len(df),1)*100)
            fg = key_fg.get(it,"#64748b"); bg = key_bg.get(it,"#f1f5f9")
            st.markdown(f"""
            <div style="margin-bottom:16px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;
                             font-weight:700;background:{bg};color:{fg};">{lbl}</span>
                <span style="font-size:12.5px;font-weight:700;color:{fg};">{val}</span>
              </div>
              <div style="background:#f1f5f9;border-radius:4px;height:6px;">
                <div style="width:{pct}%;background:{fg};border-radius:4px;height:6px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with c1:
        prog_card("🏢 By Company", COMPANIES, C_BG, C_FG,
                  lambda c: c,
                  lambda c,d: f"{len(d[d['company']==c])} orders · ₹{d[d['company']==c]['total_value'].sum()/1e5:.1f}L")
    with c2:
        prog_card("📊 By Status", STATUSES, S_BG, S_FG,
                  lambda s: f"{S_EMOJI.get(s,'')} {s}",
                  lambda s,d: str(len(d[d['current_status']==s])))

    # Financial table
    TH=("padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
        "border-bottom:2px solid #e2e8f0;text-align:left;")
    TD="padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
    rows=""; outstanding=0.0
    for i,(_,r) in enumerate(df.iterrows()):
        bg="#fff" if i%2==0 else "#fafbfc"; tv=float(r["total_value"])
        paid=f'<span style="color:#15803d;font-weight:700;">₹{tv:,.0f}</span>' if r["current_status"]=="Paid" else "—"
        out ="—" if r["current_status"]=="Paid" else f'<span style="color:#92400e;font-weight:700;">₹{tv:,.0f}</span>'
        if r["current_status"]!="Paid": outstanding+=tv
        rows+=f'<tr style="background:{bg}"><td style="{TD}font-size:11.5px;color:#64748b;">{r["order_id"]}</td><td style="{TD}">{cobadge(r["company"])}</td><td style="{TD}">{r["govt_department"]}</td><td style="{TD}font-weight:700;">₹{tv:,.0f}</td><td style="{TD}">{sbadge(r["current_status"])}</td><td style="{TD}">{paid}</td><td style="{TD}">{out}</td></tr>'
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;
                box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;">
      <div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">💵 Financial Summary</div>
      </div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead><tr>
            <th style="{TH}">Order ID</th><th style="{TH}">Company</th>
            <th style="{TH}">Department</th><th style="{TH}">Value</th>
            <th style="{TH}">Status</th><th style="{TH}">Paid</th><th style="{TH}">Outstanding</th>
          </tr></thead><tbody>{rows}</tbody>
        </table>
      </div>
      <div style="padding:12px 20px;background:#f8fafc;border-top:1px solid #e2e8f0;
                  display:flex;justify-content:space-between;font-size:13px;font-weight:700;">
        <span style="color:#64748b;">Total Outstanding</span>
        <span style="color:#92400e;">₹{outstanding:,.0f}</span>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN
# ─────────────────────────────────────────────────────────────────────────────
def page_admin():
    topbar("⚙️ Admin Panel","Data export, statistics, user management")
    D  = st.session_state.data
    P  = "padding:0 28px;"
    st.markdown(f'<div style="{P}">', unsafe_allow_html=True)

    st.info("✅ **Auto-Save** — Changes save instantly.  📥 **Export** — Download CSV files below.")

    tables = ["orders","procurement","dispatch","delivery","invoices","activity_log"]

    # Export
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;
                box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;">
      <div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">📥 Export Data</div>
      </div><div style="padding:18px;">
    """, unsafe_allow_html=True)
    cs = st.columns(3)
    for i,t in enumerate(tables):
        with cs[i%3]:
            csv = D[t].to_csv(index=False).encode("utf-8")
            st.download_button(f"📄 {t} ({len(D[t])} rows)", csv,
                               f"sc_{t}_{now_ist()[:10]}.csv","text/csv",
                               use_container_width=True, key=f"dl_{t}")
    sp(8)
    all_csv = "\n\n".join([f"=== {t.upper()} ===\n"+D[t].to_csv(index=False) for t in tables])
    st.download_button("📦 Export ALL Tables", all_csv.encode(),
                       f"sc_full_{now_ist()[:10]}.csv","text/csv",
                       use_container_width=True, key="dl_all", type="primary")
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Stats
    stat_html = "".join([
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-top:3px solid #1d4ed8;'
        f'border-radius:8px;padding:12px;text-align:center;">'
        f'<div style="font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;">{t}</div>'
        f'<div style="font-size:22px;font-weight:800;color:#1d4ed8;margin-top:6px;">{len(D[t])}</div>'
        f'<div style="font-size:10px;color:#94a3b8;">rows</div></div>'
        for t in tables
    ])
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;
                box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;">
      <div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">⚙️ Database Statistics</div>
      </div>
      <div style="padding:18px;display:grid;grid-template-columns:repeat(6,1fr);gap:12px;">{stat_html}</div>
    </div>""", unsafe_allow_html=True)

    # Users
    TH=("padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.5px;color:#475569;"
        "border-bottom:2px solid #e2e8f0;text-align:left;")
    TD="padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;"
    RDESC={"Admin":"Full access — all pages","Manager":"No admin page",
           "Staff":"Update orders only","Viewer":"Read-only access"}
    rows="".join([
        f'<tr style="background:{"#fff" if i%2==0 else "#fafbfc"}"><td style="{TD}font-weight:700;font-family:monospace;">{u}</td>'
        f'<td style="{TD}">{v["name"]}</td>'
        f'<td style="{TD}"><span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;background:{R_BG.get(v["role"],"#f1f5f9")};color:{R_COLOR.get(v["role"],"#64748b")};">{v["role"]}</span></td>'
        f'<td style="{TD}color:#64748b;font-size:12px;">{RDESC.get(v["role"],"")}</td></tr>'
        for i,(u,v) in enumerate(USERS.items())
    ])
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;
                box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;">
      <div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">👥 User Accounts</div>
      </div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead><tr>
            <th style="{TH}">Username</th><th style="{TH}">Full Name</th>
            <th style="{TH}">Role</th><th style="{TH}">Permissions</th>
          </tr></thead><tbody>{rows}</tbody>
        </table>
      </div>
    </div>""", unsafe_allow_html=True)

    with st.expander("⚠️ Danger Zone — Reset All Data"):
        st.warning("Permanently deletes all data and restores sample records. Cannot be undone.")
        if st.button("🗑 Reset to Sample Data", type="primary"):
            for k,d in SEED.items():
                d.astype(str).fillna("").to_csv(FILES[k],index=False)
            st.session_state.data = load_data()
            st.success("✅ Reset complete."); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    render_sidebar()

    allowed = ROLE_MENUS.get(st.session_state.role, [])
    if st.session_state.menu not in allowed:
        st.session_state.menu = "Dashboard"
        st.rerun()

    {
        "Dashboard":     page_dashboard,
        "New Order":     page_new_order,
        "Update Order":  page_update_order,
        "Order Details": page_order_details,
        "Activity Log":  page_activity_log,
        "Reports":       page_reports,
        "Admin":         page_admin,
    }[st.session_state.menu]()

if __name__ == "__main__":
    main()
