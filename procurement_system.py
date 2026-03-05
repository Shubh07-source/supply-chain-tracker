import streamlit as st
import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG — must be the very first Streamlit call, no exceptions
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Supply Chain Tracking System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
COMPANIES  = ["Robokart", "Bharat Tech", "EL"]
STATUSES   = ["Pending", "Procured", "Dispatched", "Delivered", "Invoiced", "Paid"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]

SE = {"Pending":"⏳","Procured":"🔧","Dispatched":"🚚","Delivered":"📦","Invoiced":"🧾","Paid":"💰"}
SB = {"Pending":"#fef3c7","Procured":"#dbeafe","Dispatched":"#ede9fe","Delivered":"#d1fae5","Invoiced":"#cffafe","Paid":"#dcfce7"}
SF = {"Pending":"#92400e","Procured":"#1e40af","Dispatched":"#5b21b6","Delivered":"#065f46","Invoiced":"#155e75","Paid":"#14532d"}
PB = {"Low":"#f1f5f9","Medium":"#dbeafe","High":"#fef9c3","Urgent":"#fee2e2"}
PF = {"Low":"#475569","Medium":"#1e40af","High":"#92400e","Urgent":"#dc2626"}
CB = {"Robokart":"#ede9fe","Bharat Tech":"#cffafe","EL":"#ffedd5"}
CF = {"Robokart":"#5b21b6","Bharat Tech":"#155e75","EL":"#9a3412"}

USERS = {
    "Admin":   {"password":"admin@123",    "role":"Admin",   "name":"System Admin"},
    "Manager": {"password":"mgr@123",      "role":"Manager", "name":"Ops Manager"},
    "Staff":   {"password":"Ops@Secure#1", "role":"Staff",   "name":"Operations Staff"},
    "Viewer":  {"password":"view123",      "role":"Viewer",  "name":"Finance Viewer"},
}
MENUS = {
    "Admin":   ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports","Admin"],
    "Manager": ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports"],
    "Staff":   ["Dashboard","Update Order","Order Details","Activity Log"],
    "Viewer":  ["Dashboard","Order Details","Activity Log"],
}
ICONS  = {"Dashboard":"📊","New Order":"➕","Update Order":"🔄","Order Details":"🔍","Activity Log":"📋","Reports":"📈","Admin":"⚙️"}
RC = {"Admin":"#dc2626","Manager":"#d97706","Staff":"#2563eb","Viewer":"#059669"}
RB = {"Admin":"#fee2e2","Manager":"#fef3c7","Staff":"#dbeafe","Viewer":"#dcfce7"}

# ══════════════════════════════════════════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════════════════════════════════════════
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
FILES = {k: f"{DATA_DIR}/{k}.csv" for k in
         ["orders","procurement","dispatch","delivery","invoices","activity_log"]}

def make_seed():
    return {
        "orders": pd.DataFrame([
            {"order_id":"ORD-2026-02-28-001","date_created":"2026-02-10 09:30:00","company":"Robokart","govt_department":"Education Department Delhi","contact_person":"Mr. Rajesh Kumar","contact_phone":"9876543210","po_number":"PO/EDU/2026/001","item_description":"Robotics Kits for STEM Labs","quantity":"50","total_value":"250000","assigned_company":"Tech Solutions Pvt Ltd","current_status":"Dispatched","priority":"High","expected_delivery_date":"2026-03-05","remarks":"","created_by":"Admin","last_updated":"2026-02-20 11:00:00"},
            {"order_id":"ORD-2026-02-28-002","date_created":"2026-02-12 10:15:00","company":"Bharat Tech","govt_department":"Health Ministry Maharashtra","contact_person":"Dr. Priya Sharma","contact_phone":"9123456789","po_number":"PO/HLT/2026/044","item_description":"Medical IoT Devices & Sensors","quantity":"200","total_value":"980000","assigned_company":"BioTech India","current_status":"Pending","priority":"Urgent","expected_delivery_date":"2026-03-10","remarks":"","created_by":"Admin","last_updated":"2026-02-12 10:15:00"},
            {"order_id":"ORD-2026-02-28-003","date_created":"2026-01-28 14:00:00","company":"EL","govt_department":"Defence Research DRDO","contact_person":"Col. Vikram Singh","contact_phone":"9000123456","po_number":"PO/DEF/2026/007","item_description":"Surveillance Drone Components","quantity":"10","total_value":"1500000","assigned_company":"AeroDyne Systems","current_status":"Paid","priority":"Medium","expected_delivery_date":"2026-02-20","remarks":"","created_by":"Admin","last_updated":"2026-02-25 16:30:00"},
            {"order_id":"ORD-2026-02-28-004","date_created":"2026-02-18 08:45:00","company":"Robokart","govt_department":"Smart Cities Mission UP","contact_person":"Ms. Anita Verma","contact_phone":"9988776655","po_number":"PO/SCM/2026/019","item_description":"IoT Traffic Management System","quantity":"30","total_value":"670000","assigned_company":"Robokart Solutions","current_status":"Delivered","priority":"Medium","expected_delivery_date":"2026-02-28","remarks":"","created_by":"Admin","last_updated":"2026-02-26 17:00:00"},
        ]),
        "procurement": pd.DataFrame([
            {"id":"1","order_id":"ORD-2026-02-28-001","procurement_status":"Completed","procurement_date":"2026-02-15","materials_source":"Vendor - RoboSupplies","quality_check_status":"Passed","notes":"All kits verified","updated_by":"Rahul","updated_at":"2026-02-15 14:00:00"},
            {"id":"2","order_id":"ORD-2026-02-28-003","procurement_status":"Completed","procurement_date":"2026-02-05","materials_source":"Import - AeroParts Ltd","quality_check_status":"Passed","notes":"Custom components sourced","updated_by":"Vikram","updated_at":"2026-02-05 10:00:00"},
        ]),
        "dispatch": pd.DataFrame([
            {"id":"1","order_id":"ORD-2026-02-28-001","dispatch_date":"2026-02-18","courier_name":"BlueDart","vehicle_number":"DL01AB1234","driver_contact":"9111222333","tracking_number":"BD123456789","expected_delivery_date":"2026-03-05","updated_by":"Rahul","updated_at":"2026-02-18 08:30:00"},
            {"id":"2","order_id":"ORD-2026-02-28-004","dispatch_date":"2026-02-24","courier_name":"In-House","vehicle_number":"UP32CD9012","driver_contact":"9777888999","tracking_number":"IH-004-UP","expected_delivery_date":"2026-02-28","updated_by":"Dev","updated_at":"2026-02-24 09:00:00"},
        ]),
        "delivery": pd.DataFrame([
            {"id":"1","order_id":"ORD-2026-02-28-003","delivery_status":"Delivered","delivery_date":"2026-02-19","receiver_name":"Col. Vikram Singh","delivered_quantity":"10","challan_number":"CH-DEF-001","delivery_files":"0 file(s)","challan_files":"0 file(s)","updated_by":"Ops","updated_at":"2026-02-19 16:00:00"},
            {"id":"2","order_id":"ORD-2026-02-28-004","delivery_status":"Delivered","delivery_date":"2026-02-26","receiver_name":"Ms. Anita Verma","delivered_quantity":"30","challan_number":"CH-SCM-004","delivery_files":"0 file(s)","challan_files":"0 file(s)","updated_by":"Dev","updated_at":"2026-02-26 14:30:00"},
        ]),
        "invoices": pd.DataFrame([
            {"id":"1","order_id":"ORD-2026-02-28-003","invoice_number":"INV-2026-0321","invoice_date":"2026-02-20","invoice_amount":"1500000","payment_status":"Completed","payment_date":"2026-02-24","payment_mode":"NEFT","transaction_reference":"TXN20260224DEF","invoice_files":"0 file(s)","updated_by":"Finance","updated_at":"2026-02-24 16:00:00"},
            {"id":"2","order_id":"ORD-2026-02-28-004","invoice_number":"INV-2026-0389","invoice_date":"2026-02-27","invoice_amount":"670000","payment_status":"Approved","payment_date":"","payment_mode":"","transaction_reference":"","invoice_files":"0 file(s)","updated_by":"Finance","updated_at":"2026-02-27 11:00:00"},
        ]),
        "activity_log": pd.DataFrame([
            {"id":"1","order_id":"ORD-2026-02-28-001","action_type":"ORDER_CREATED","previous_status":"—","new_status":"Pending","performed_by":"Admin","performed_at":"2026-02-10 09:30:00","details":"Order created"},
            {"id":"2","order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Pending","new_status":"Procured","performed_by":"Rahul","performed_at":"2026-02-15 14:00:00","details":"Procurement completed"},
            {"id":"3","order_id":"ORD-2026-02-28-001","action_type":"STATUS_CHANGE","previous_status":"Procured","new_status":"Dispatched","performed_by":"Rahul","performed_at":"2026-02-18 08:30:00","details":"Dispatched via BlueDart"},
            {"id":"4","order_id":"ORD-2026-02-28-003","action_type":"PAYMENT","previous_status":"Invoiced","new_status":"Paid","performed_by":"Finance","performed_at":"2026-02-24 16:00:00","details":"NEFT payment received"},
            {"id":"5","order_id":"ORD-2026-02-28-004","action_type":"STATUS_CHANGE","previous_status":"Dispatched","new_status":"Delivered","performed_by":"Dev","performed_at":"2026-02-26 14:30:00","details":"Delivered, challan signed"},
        ]),
    }

def now_ist():
    return datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S")

def load_data():
    seed = make_seed()
    out  = {}
    for k, path in FILES.items():
        if os.path.exists(path):
            out[k] = pd.read_csv(path, dtype=str).fillna("")
        else:
            df = seed[k].copy()
            df.to_csv(path, index=False)
            out[k] = df
    return out

def save(k):
    st.session_state.D[k].to_csv(FILES[k], index=False)

def log_action(oid, action, prev, nxt, by, detail):
    D   = st.session_state.D
    new = pd.DataFrame([{"id":str(len(D["activity_log"])+1),"order_id":oid,
                         "action_type":action,"previous_status":prev,"new_status":nxt,
                         "performed_by":by,"performed_at":now_ist(),"details":detail}])
    D["activity_log"] = pd.concat([D["activity_log"], new], ignore_index=True)
    save("activity_log")

def update_status(oid, ns):
    D = st.session_state.D
    D["orders"].loc[D["orders"]["order_id"]==oid, "current_status"] = ns
    D["orders"].loc[D["orders"]["order_id"]==oid, "last_updated"]   = now_ist()
    save("orders")

def get_order(oid):
    rows = st.session_state.D["orders"]
    r    = rows[rows["order_id"]==oid]
    return r.iloc[0] if len(r) else None

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "logged_in": False, "username": "", "role": "",
    "user_name": "", "page": "Dashboard", "co_filter": "All",
    "login_error": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "D" not in st.session_state:
    st.session_state.D = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html,body,.stApp,[class*="css"]{
    font-family:'Inter','Segoe UI',sans-serif!important;
    background:#f1f5f9!important;
    color:#1e293b!important;
}
*,*::before,*::after{box-sizing:border-box;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0!important;max-width:100%!important;}
section.main>div{padding:0!important;}

/* ── INPUTS: nuclear-specificity white background ───────────── */
input,input[type],input[type="text"],input[type="password"],
input[type="number"],input[type="email"],textarea,
.stTextInput input,.stTextArea textarea,
.stNumberInput input,.stDateInput input,
[data-baseweb="input"] input,[data-baseweb="base-input"] input{
    background-color:#fff!important;
    background:#fff!important;
    color:#111827!important;
    -webkit-text-fill-color:#111827!important;
    caret-color:#111827!important;
    border:1.5px solid #cbd5e1!important;
    border-radius:8px!important;
    font-size:14px!important;
    font-family:'Inter',sans-serif!important;
    opacity:1!important;
}
input::placeholder,textarea::placeholder{
    color:#9ca3af!important;
    -webkit-text-fill-color:#9ca3af!important;
    opacity:1!important;
}
input:focus,textarea:focus{
    border-color:#3b82f6!important;
    box-shadow:0 0 0 3px rgba(59,130,246,0.15)!important;
    outline:none!important;
    background:#fff!important;
    color:#111827!important;
    -webkit-text-fill-color:#111827!important;
}
[data-baseweb="input"],[data-baseweb="base-input"],
.stTextInput>div>div,.stTextArea>div>div,
.stNumberInput>div>div,.stDateInput>div>div{
    background:#fff!important;
    border-radius:8px!important;
}
[data-baseweb="select"]>div,.stSelectbox>div>div{
    background:#fff!important;
    border:1.5px solid #cbd5e1!important;
    border-radius:8px!important;
    color:#111827!important;
}
label,.stTextInput label,.stTextArea label,.stSelectbox label,
.stNumberInput label,.stDateInput label,.stFileUploader label{
    color:#374151!important;
    font-size:12.5px!important;
    font-weight:600!important;
}

/* ── SIDEBAR ─────────────────────────────────────────────────── */
[data-testid="stSidebar"]{
    background:#0f172a!important;
    min-width:240px!important;
    max-width:240px!important;
}
[data-testid="stSidebar"]>div:first-child{padding:0!important;min-height:100vh;}
[data-testid="stSidebar"] *:not(button):not(button *){color:#94a3b8!important;}

[data-testid="stSidebar"] .stButton>button{
    width:calc(100% - 16px)!important;
    text-align:left!important;
    background:transparent!important;
    border:none!important;
    border-radius:8px!important;
    color:#94a3b8!important;
    font-size:13.5px!important;
    font-weight:500!important;
    padding:10px 16px!important;
    margin:1px 8px!important;
    box-shadow:none!important;
    -webkit-text-fill-color:#94a3b8!important;
    transition:all 0.15s!important;
}
[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(255,255,255,0.07)!important;
    color:#e2e8f0!important;
    -webkit-text-fill-color:#e2e8f0!important;
}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{
    background:#1d4ed8!important;
    color:#fff!important;
    font-weight:700!important;
    -webkit-text-fill-color:#fff!important;
}

/* ── APP BUTTONS ─────────────────────────────────────────────── */
.stButton>button{
    border-radius:8px!important;
    font-weight:600!important;
    font-size:13px!important;
    padding:9px 20px!important;
    cursor:pointer!important;
    border:1.5px solid transparent!important;
    transition:all 0.15s!important;
}
.stButton>button[kind="primary"]{
    background:#1d4ed8!important;
    border-color:#1d4ed8!important;
    color:#fff!important;
    -webkit-text-fill-color:#fff!important;
}
.stButton>button[kind="primary"]:hover{background:#1e40af!important;}
.stButton>button[kind="secondary"]{
    background:#fff!important;
    border:1.5px solid #e2e8f0!important;
    color:#374151!important;
}

/* ── TABS ────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{
    background:transparent!important;
    border-bottom:2px solid #e2e8f0!important;
    gap:0!important;padding:0!important;
}
.stTabs [data-baseweb="tab"]{
    background:transparent!important;border:none!important;
    border-bottom:2px solid transparent!important;
    color:#64748b!important;font-weight:500!important;
    font-size:13px!important;padding:10px 22px!important;margin-bottom:-2px!important;
}
.stTabs [aria-selected="true"]{
    border-bottom:2px solid #1d4ed8!important;
    color:#1d4ed8!important;font-weight:700!important;
}
hr{border-color:#e2e8f0!important;margin:14px 0!important;}
.streamlit-expanderHeader{background:#f8fafc!important;border-radius:8px!important;font-weight:600!important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# BADGE / UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def sbadge(s):
    bg=SB.get(s,"#f1f5f9"); fg=SF.get(s,"#475569")
    return f'<span style="display:inline-block;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;background:{bg};color:{fg};white-space:nowrap;">{SE.get(s,"")} {s}</span>'

def pbadge(p):
    bg=PB.get(p,"#f1f5f9"); fg=PF.get(p,"#475569")
    return f'<span style="display:inline-block;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;background:{bg};color:{fg};">{p}</span>'

def cobadge(c):
    bg=CB.get(c,"#f1f5f9"); fg=CF.get(c,"#475569")
    return f'<span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;background:{bg};color:{fg};">{c}</span>'

def g(px=12):
    st.markdown(f'<div style="height:{px}px"></div>', unsafe_allow_html=True)

def topbar(title, sub=""):
    s = f'<div style="font-size:12px;color:#64748b;margin-top:3px;">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div style="background:#fff;border-bottom:1px solid #e2e8f0;padding:14px 28px;
        display:flex;justify-content:space-between;align-items:center;
        box-shadow:0 1px 3px rgba(0,0,0,0.04);">
      <div>
        <div style="font-size:18px;font-weight:800;color:#0f172a;">{title}</div>{s}
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="display:flex;align-items:center;gap:6px;background:#f0fdf4;
            border:1px solid #bbf7d0;border-radius:20px;padding:5px 14px;
            font-size:11.5px;font-weight:600;color:#15803d;">
          <div style="width:7px;height:7px;border-radius:50%;background:#22c55e;"></div>Auto-saved
        </div>
        <div style="font-size:12px;color:#64748b;font-weight:500;">
            📅 {datetime.now().strftime("%d %b %Y")}</div>
      </div>
    </div>
    <div style="height:24px;"></div>""", unsafe_allow_html=True)

def footer():
    st.markdown(
        f'<div style="text-align:center;font-size:11px;color:#94a3b8;padding:18px 0 10px;'
        f'border-top:1px solid #e2e8f0;margin-top:32px;">© {datetime.now().year} Robokart &nbsp;·&nbsp; Supply Chain Tracking System</div>',
        unsafe_allow_html=True)

def sl(t):  # section label
    st.markdown(
        f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;'
        f'color:#94a3b8;border-bottom:1px solid #f1f5f9;padding-bottom:8px;margin:14px 0 12px;">{t}</div>',
        unsafe_allow_html=True)

def fcard(title, sub=""):
    s = f'<div style="font-size:12px;color:#64748b;margin-top:3px;">{sub}</div>' if sub else ""
    st.markdown(
        f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;'
        f'box-shadow:0 1px 4px rgba(0,0,0,0.05);max-width:860px;">'
        f'<div style="padding:16px 24px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">'
        f'<div style="font-size:14px;font-weight:700;color:#0f172a;">{title}</div>{s}</div>'
        f'<div style="padding:22px 24px;">', unsafe_allow_html=True)

def fcard_end():
    st.markdown("</div></div>", unsafe_allow_html=True)

def info_row(items):
    """Render a key-value grid row."""
    cells = "".join([
        f'<div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">{k}</div>'
        f'<div style="font-size:13px;font-weight:600;color:#0f172a;">{v}</div></div>'
        for k, v in items
    ])
    st.markdown(
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));'
        f'gap:12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;'
        f'padding:14px 18px;margin:10px 0 16px;">{cells}</div>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# Critical design: do NOT use st.form for login.
# Use individual text_input widgets with explicit keys.
# Read values from session_state INSIDE the button callback.
# This is the only pattern guaranteed to work reliably in Streamlit.
# ══════════════════════════════════════════════════════════════════════════════
def login_page():
    st.markdown("""
    <style>
    .stApp{background:linear-gradient(135deg,#0c1426 0%,#1e3a5f 50%,#0c1426 100%)!important;}
    [data-testid="stSidebar"]{display:none!important;}
    [data-testid="collapsedControl"]{display:none!important;}
    .block-container{padding:60px 16px 0!important;}
    </style>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        # ── Branding panel (pure HTML, above form) ──────────────────────────
        st.markdown("""
        <div style="background:#fff;border:1px solid #e2e8f0;border-bottom:1px solid #f0f4f8;
            border-radius:16px 16px 0 0;padding:38px 32px 26px;text-align:center;">
          <div style="width:74px;height:74px;border-radius:18px;margin:0 auto 16px;
              background:linear-gradient(135deg,#1e3a5f,#1d4ed8);
              display:flex;align-items:center;justify-content:center;font-size:36px;
              box-shadow:0 6px 20px rgba(29,78,216,0.35);">🏭</div>
          <div style="font-size:20px;font-weight:800;color:#0f172a;">Supply Chain Tracking System</div>
          <div style="font-size:13px;color:#64748b;margin-top:8px;">Enterprise Procurement &amp; Order Management</div>
        </div>
        <div style="background:#fff;border-left:1px solid #e2e8f0;border-right:1px solid #e2e8f0;
            padding:20px 32px 6px;box-shadow:0 8px 30px rgba(0,0,0,0.25);">
          <div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:4px;">
            Sign in to your account</div>
          <div style="font-size:12px;color:#64748b;margin-bottom:14px;">
            Enter your credentials below to access the system</div>
        </div>""", unsafe_allow_html=True)

        # ── Credentials widgets — NOT inside st.form ─────────────────────────
        # Using key= means Streamlit stores value in session_state immediately.
        # The button then reads directly from session_state — no timing issues.
        st.text_input("Username", placeholder="e.g. Admin", key="_login_u",
                      label_visibility="visible")
        st.text_input("Password", placeholder="Enter password", type="password",
                      key="_login_p", label_visibility="visible")

        g(6)

        # ── Sign In button ────────────────────────────────────────────────────
        if st.button("🔐  Sign In", key="btn_signin",
                     type="primary", use_container_width=True):
            u = st.session_state.get("_login_u", "").strip()
            p = st.session_state.get("_login_p", "")
            if u in USERS and USERS[u]["password"] == p:
                st.session_state.logged_in  = True
                st.session_state.username   = u
                st.session_state.role       = USERS[u]["role"]
                st.session_state.user_name  = USERS[u]["name"]
                st.session_state.page       = "Dashboard"
                st.session_state.login_error = False
                st.rerun()
            else:
                st.session_state.login_error = True
                st.rerun()

        if st.session_state.login_error:
            st.error("⚠️  Invalid username or password. Try again.", icon="🚫")

        # Card bottom + credentials hint
        st.markdown("""
        <div style="background:#fff;border:1px solid #e2e8f0;border-top:none;
            border-radius:0 0 16px 16px;padding:14px 32px 24px;
            box-shadow:0 20px 50px rgba(0,0,0,0.35);">
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
              padding:10px 14px;font-size:11.5px;color:#64748b;line-height:1.8;">
            <strong style="color:#374151;">Demo credentials:</strong><br>
            <span style="font-family:monospace;">Admin</span> / admin@123 &nbsp;·&nbsp;
            <span style="font-family:monospace;">Manager</span> / mgr@123<br>
            <span style="font-family:monospace;">Staff</span> / Ops@Secure#1 &nbsp;·&nbsp;
            <span style="font-family:monospace;">Viewer</span> / view123
          </div>
          <p style="text-align:center;font-size:11.5px;color:#94a3b8;margin-top:14px;margin-bottom:0;">
            🔒 Secure access &nbsp;·&nbsp; Contact administrator for credentials</p>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        # Logo bar
        st.markdown("""
        <div style="padding:22px 18px 18px;border-bottom:1px solid #1e293b;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:38px;height:38px;border-radius:9px;flex-shrink:0;
                background:linear-gradient(135deg,#1e3a5f,#1d4ed8);
                display:flex;align-items:center;justify-content:center;font-size:20px;
                box-shadow:0 2px 8px rgba(29,78,216,0.4);">🏭</div>
            <div>
              <div style="font-size:14px;font-weight:800;color:#f8fafc;">Supply Chain</div>
              <div style="font-size:9px;color:#475569;letter-spacing:1.2px;text-transform:uppercase;">Tracking System</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        g(10)
        st.markdown('<div style="padding:0 18px;font-size:9.5px;font-weight:700;letter-spacing:1.2px;color:#334155;text-transform:uppercase;margin-bottom:4px;">Navigation</div>', unsafe_allow_html=True)

        for m in MENUS.get(st.session_state.role, []):
            active = st.session_state.page == m
            if st.button(f"{ICONS.get(m,'')}  {m}", key=f"nav_{m}",
                         use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = m
                st.rerun()

        g(14)
        st.markdown('<div style="height:1px;background:#1e293b;margin:0 16px 14px;"></div>', unsafe_allow_html=True)

        # User card
        role = st.session_state.role
        rc   = RC.get(role,"#64748b"); rb = RB.get(role,"#1e293b")
        ini  = "".join(w[0].upper() for w in st.session_state.user_name.split()[:2])
        st.markdown(f"""
        <div style="padding:0 14px;margin-bottom:10px;">
          <div style="background:#1e293b;border-radius:10px;padding:12px 14px;
              display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;border-radius:8px;flex-shrink:0;
                background:{rc};color:#fff;font-size:13px;font-weight:800;
                display:flex;align-items:center;justify-content:center;">{ini}</div>
            <div style="overflow:hidden;">
              <div style="font-size:12.5px;font-weight:700;color:#f1f5f9;
                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                  {st.session_state.user_name}</div>
              <span style="font-size:10px;font-weight:700;background:{rb};
                  color:{rc};padding:1px 8px;border-radius:4px;">{role}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        if st.button("⬅  Sign Out", key="btn_signout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        g(10)

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    topbar("📊 Dashboard", "Real-time overview of all purchase orders and supply chain status")
    D   = st.session_state.D
    df  = D["orders"].copy()
    cf  = st.session_state.co_filter
    fil = df if cf == "All" else df[df["company"] == cf]
    tv  = fil["total_value"].astype(float).sum() if len(fil) else 0.0
    PAD = "padding:0 28px;"

    # KPI row
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    kpis = [
        ("Total Orders", len(fil),                                                               "#1d4ed8"),
        ("Pending",      len(fil[fil["current_status"]=="Pending"]),                             "#d97706"),
        ("In Transit",   len(fil[fil["current_status"].isin(["Procured","Dispatched"])]),        "#7c3aed"),
        ("Delivered",    len(fil[fil["current_status"].isin(["Delivered","Invoiced","Paid"])]),  "#059669"),
        ("Paid",         len(fil[fil["current_status"]=="Paid"]),                                "#0891b2"),
        ("Total Value",  f"₹{tv/100000:.1f}L",                                                   "#c2410c"),
    ]
    for col, (lbl, val, color) in zip(st.columns(6, gap="small"), kpis):
        with col:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                padding:18px 16px 16px;box-shadow:0 1px 4px rgba(0,0,0,0.05);
                position:relative;overflow:hidden;">
              <div style="position:absolute;top:0;left:0;right:0;height:3px;
                  background:{color};border-radius:12px 12px 0 0;"></div>
              <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                  letter-spacing:.8px;color:#64748b;margin-bottom:10px;">{lbl}</div>
              <div style="font-size:28px;font-weight:800;color:{color};line-height:1;">{val}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    g(22)

    # Company filter
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4, _ = st.columns([1.6,1.1,1.4,0.8,3], gap="small")
    for col, lbl, key in [(fc1,"🏢 All Companies","All"),(fc2,"Robokart","Robokart"),(fc3,"Bharat Tech","Bharat Tech"),(fc4,"EL","EL")]:
        with col:
            txt = lbl + (" ✓" if cf==key else "")
            if st.button(txt, key=f"cf_{key}",
                         type="primary" if cf==key else "secondary",
                         use_container_width=True):
                st.session_state.co_filter = key; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    g(20)

    # Orders table
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    TH = "padding:11px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;white-space:nowrap;"
    TD = "padding:13px 16px;border-bottom:1px solid #f1f5f9;color:#1e293b;vertical-align:middle;"
    tbody = ""
    if len(fil) == 0:
        tbody = '<tr><td colspan="10" style="padding:32px;text-align:center;color:#94a3b8;">No orders found.</td></tr>'
    else:
        for i, (_, r) in enumerate(fil.iterrows()):
            bg   = "#fff" if i%2==0 else "#fafbfc"
            desc = str(r["item_description"]); desc = desc[:40]+"…" if len(desc)>40 else desc
            tbody += f"""<tr style="background:{bg}">
              <td style="{TD}font-weight:700;color:#1d4ed8;font-size:12px;white-space:nowrap;">{r["order_id"]}</td>
              <td style="{TD}">{cobadge(r["company"])}</td>
              <td style="{TD}color:#64748b;font-size:12px;">{r["po_number"]}</td>
              <td style="{TD}font-size:12.5px;">{r["govt_department"]}</td>
              <td style="{TD}font-size:12.5px;color:#374151;">{desc}</td>
              <td style="{TD}text-align:center;font-weight:600;">{r["quantity"]}</td>
              <td style="{TD}font-weight:700;white-space:nowrap;">₹{float(r["total_value"]):,.0f}</td>
              <td style="{TD}">{pbadge(r["priority"])}</td>
              <td style="{TD}">{sbadge(r["current_status"])}</td>
              <td style="{TD}color:#94a3b8;font-size:11.5px;white-space:nowrap;">{r["last_updated"]}</td>
            </tr>"""

    title_lbl = "All Orders" if cf=="All" else f"{cf} Orders"
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
        overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
      <div style="display:flex;justify-content:space-between;align-items:center;
          padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">📦 {title_lbl}</div>
        <div style="font-size:11px;font-weight:600;color:#64748b;background:#f1f5f9;
            padding:3px 12px;border-radius:20px;">{len(fil)} orders</div>
      </div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead><tr>
            <th style="{TH}">Order ID</th><th style="{TH}">Company</th><th style="{TH}">PO Number</th>
            <th style="{TH}">Department</th><th style="{TH}">Description</th><th style="{TH}">Qty</th>
            <th style="{TH}">Value</th><th style="{TH}">Priority</th><th style="{TH}">Status</th>
            <th style="{TH}">Last Updated</th>
          </tr></thead>
          <tbody>{tbody}</tbody>
        </table>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    g(8); st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True); footer(); st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NEW ORDER
# ══════════════════════════════════════════════════════════════════════════════
def page_new_order():
    topbar("➕ New Order", "Create a new government purchase order")
    D = st.session_state.D
    st.markdown('<div style="padding:0 28px;">', unsafe_allow_html=True)
    fcard("📝 Purchase Order Details", "Fields marked * are required")

    with st.form("form_new_order", clear_on_submit=True):
        sl("Company & Classification")
        c1,c2 = st.columns(2)
        with c1: company  = st.selectbox("Company *",  COMPANIES)
        with c2: priority = st.selectbox("Priority *", PRIORITIES, index=1)
        c3,c4 = st.columns(2)
        with c3: gdept   = st.text_input("Govt Department *",  placeholder="e.g. Education Department Delhi")
        with c4: po_num  = st.text_input("PO Number *",        placeholder="e.g. PO/EDU/2026/001")

        sl("Contact Information")
        c5,c6 = st.columns(2)
        with c5: cname = st.text_input("Contact Person *", placeholder="e.g. Mr. Rajesh Kumar")
        with c6: cph   = st.text_input("Contact Phone",    placeholder="e.g. 9876543210")

        sl("Order Details")
        c7,c8 = st.columns(2)
        with c7:
            qty = st.number_input("Quantity *",        min_value=1, value=1)
            val = st.number_input("Total Value (₹) *", min_value=0, value=0)
        with c8:
            assigned = st.text_input("Assigned Company", placeholder="e.g. Tech Solutions Pvt Ltd")
            exp_del  = st.date_input("Expected Delivery Date")

        item_desc = st.text_area("Item Description *", placeholder="Detailed description of goods/services…", height=88)
        remarks   = st.text_area("Remarks",            placeholder="Any additional notes…", height=60)
        g(4)
        sc, _ = st.columns([1,2])
        with sc: submitted = st.form_submit_button("🚀 Create Purchase Order", type="primary", use_container_width=True)

        if submitted:
            errs = [f for f,v in [("Govt Dept",gdept),("PO Number",po_num),("Contact",cname),("Description",item_desc)] if not str(v).strip()]
            if errs:
                st.error(f"Missing required fields: {', '.join(errs)}")
            elif val == 0:
                st.error("Total Value must be greater than 0.")
            elif po_num.strip() in D["orders"]["po_number"].values:
                st.error("⚠ PO Number already exists.")
            else:
                ts  = now_ist()
                oid = f"ORD-{ts[:10]}-{str(len(D['orders'])+1).zfill(3)}"
                D["orders"] = pd.concat([D["orders"], pd.DataFrame([{
                    "order_id":oid,"date_created":ts,"company":company,
                    "govt_department":gdept,"contact_person":cname,"contact_phone":cph,
                    "po_number":po_num,"item_description":item_desc,"quantity":str(qty),
                    "total_value":str(val),"assigned_company":assigned,
                    "current_status":"Pending","priority":priority,
                    "expected_delivery_date":str(exp_del),"remarks":remarks,
                    "created_by":st.session_state.user_name,"last_updated":ts
                }])], ignore_index=True)
                save("orders")
                log_action(oid,"ORDER_CREATED","—","Pending",st.session_state.user_name,f"Order created — {company} | {po_num}")
                st.success(f"✅ Order **{oid}** created successfully!")

    fcard_end()
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════════════════════
# UPDATE ORDER
# ══════════════════════════════════════════════════════════════════════════════
def page_update_order():
    topbar("🔄 Update Order", "Update procurement, dispatch, delivery or invoice status")
    D = st.session_state.D
    PAD = "padding:0 28px;"
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  [{r['current_status']}]"
        for _, r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order *", opts, key="sel_update")
    if sel == "— Select an order —":
        st.info("👆 Select an order above to update its status.")
        st.markdown('</div>', unsafe_allow_html=True); footer(); return

    oid = sel.split("  ·  ")[0].strip()
    ord_row = get_order(oid)

    info_row([
        ("Order ID",   f'<span style="color:#1d4ed8;font-weight:700;">{ord_row["order_id"]}</span>'),
        ("Company",    cobadge(ord_row["company"])),
        ("Status",     sbadge(ord_row["current_status"])),
        ("Priority",   pbadge(ord_row["priority"])),
        ("Value",      f'<span style="font-size:15px;font-weight:800;">₹{float(ord_row["total_value"]):,.0f}</span>'),
        ("Department", f'<span style="font-size:12.5px;">{ord_row["govt_department"]}</span>'),
    ])

    upd_by = st.text_input("Your Name / Department *", placeholder="e.g. Rahul — Logistics", key="upd_by")
    g(4)

    t1, t2, t3, t4 = st.tabs(["🔧  Procurement","🚚  Dispatch","📦  Delivery","💰  Invoice & Payment"])

    # ── Procurement ──────────────────────────────────────────────────────────
    with t1:
        fcard("Procurement Details")
        with st.form("f_proc"):
            c1,c2 = st.columns(2)
            with c1:
                p_stat = st.selectbox("Status *", ["","Not Started","In Progress","Completed","On Hold"])
                p_date = st.date_input("Procurement Date")
            with c2:
                p_qc   = st.selectbox("Quality Check", ["","Pending","In Progress","Passed","Failed"])
                p_src  = st.text_input("Materials Source", placeholder="Vendor / Warehouse")
            p_notes = st.text_area("Notes", height=80)
            sv = st.form_submit_button("✅ Save Procurement", type="primary")
        if sv:
            if not upd_by.strip(): st.error("Enter your name above the tabs.")
            else:
                ts = now_ist()
                D["procurement"] = pd.concat([D["procurement"], pd.DataFrame([{
                    "id":str(len(D["procurement"])+1),"order_id":oid,
                    "procurement_status":p_stat,"procurement_date":str(p_date),
                    "materials_source":p_src,"quality_check_status":p_qc,
                    "notes":p_notes,"updated_by":upd_by,"updated_at":ts
                }])], ignore_index=True); save("procurement")
                ns = "Procured" if p_stat=="Completed" else ord_row["current_status"]
                update_status(oid, ns)
                log_action(oid,"STATUS_CHANGE",ord_row["current_status"],ns,upd_by,f"Procurement: {p_stat}")
                st.success(f"✅ Saved! Status → **{ns}**"); st.rerun()
        fcard_end()

    # ── Dispatch ─────────────────────────────────────────────────────────────
    with t2:
        fcard("Dispatch Details")
        with st.form("f_disp"):
            c1,c2 = st.columns(2)
            with c1:
                d_date = st.date_input("Dispatch Date")
                d_cour = st.text_input("Courier / Transporter *", placeholder="e.g. BlueDart")
                d_veh  = st.text_input("Vehicle Number",          placeholder="e.g. DL01AB1234")
            with c2:
                d_drv  = st.text_input("Driver Contact",  placeholder="e.g. 9111222333")
                d_trk  = st.text_input("Tracking Number", placeholder="e.g. BD123456789")
                d_exp  = st.date_input("Expected Delivery")
            sv = st.form_submit_button("✅ Save Dispatch", type="primary")
        if sv:
            if not upd_by.strip(): st.error("Enter your name above the tabs.")
            else:
                D["dispatch"] = pd.concat([D["dispatch"], pd.DataFrame([{
                    "id":str(len(D["dispatch"])+1),"order_id":oid,
                    "dispatch_date":str(d_date),"courier_name":d_cour,"vehicle_number":d_veh,
                    "driver_contact":d_drv,"tracking_number":d_trk,
                    "expected_delivery_date":str(d_exp),"updated_by":upd_by,"updated_at":now_ist()
                }])], ignore_index=True); save("dispatch")
                update_status(oid,"Dispatched")
                log_action(oid,"STATUS_CHANGE",ord_row["current_status"],"Dispatched",upd_by,f"Via {d_cour}")
                st.success("✅ Dispatched!"); st.rerun()
        fcard_end()

    # ── Delivery ─────────────────────────────────────────────────────────────
    with t3:
        fcard("Delivery Confirmation")
        with st.form("f_del"):
            c1,c2 = st.columns(2)
            with c1:
                de_stat = st.selectbox("Status *", ["","Delivered","Partial","Failed","Rescheduled"])
                de_date = st.date_input("Delivery Date")
                de_recv = st.text_input("Receiver Name", placeholder="Who received the goods")
            with c2:
                de_qty = st.number_input("Delivered Qty", min_value=0)
                de_ch  = st.text_input("Challan Number", placeholder="e.g. CH-EDU-001")
            del_f = st.file_uploader("Delivery Proof Files", accept_multiple_files=True, key="delf")
            ch_f  = st.file_uploader("Challan Documents",    accept_multiple_files=True, key="chf")
            sv = st.form_submit_button("✅ Save Delivery", type="primary")
        if sv:
            if not upd_by.strip(): st.error("Enter your name above the tabs.")
            else:
                D["delivery"] = pd.concat([D["delivery"], pd.DataFrame([{
                    "id":str(len(D["delivery"])+1),"order_id":oid,
                    "delivery_status":de_stat,"delivery_date":str(de_date),
                    "receiver_name":de_recv,"delivered_quantity":str(de_qty),"challan_number":de_ch,
                    "delivery_files":f"{len(del_f or [])} file(s)","challan_files":f"{len(ch_f or [])} file(s)",
                    "updated_by":upd_by,"updated_at":now_ist()
                }])], ignore_index=True); save("delivery")
                ns = "Delivered" if de_stat=="Delivered" else ord_row["current_status"]
                update_status(oid, ns)
                log_action(oid,"STATUS_CHANGE",ord_row["current_status"],ns,upd_by,f"Delivery: {de_stat}")
                st.success(f"✅ Delivery saved! → **{ns}**"); st.rerun()
        fcard_end()

    # ── Invoice ──────────────────────────────────────────────────────────────
    with t4:
        fcard("Invoice & Payment Details")
        with st.form("f_inv"):
            c1,c2 = st.columns(2)
            with c1:
                i_num   = st.text_input("Invoice Number",   placeholder="e.g. INV-2026-0001")
                i_date  = st.date_input("Invoice Date")
                i_amt   = st.number_input("Invoice Amount (₹)", min_value=0)
                i_pstat = st.selectbox("Payment Status *", ["","Pending","Approved","Completed"])
            with c2:
                i_pmode = st.selectbox("Payment Mode", ["","NEFT","RTGS","Cheque","DD","Online","Cash"])
                i_txn   = st.text_input("Transaction Ref", placeholder="TXN / UTR number")
                i_pdate = st.date_input("Payment Date")
            inv_f = st.file_uploader("Invoice Documents", accept_multiple_files=True, key="invf")
            sv = st.form_submit_button("✅ Save Invoice & Payment", type="primary")
        if sv:
            if not upd_by.strip(): st.error("Enter your name above the tabs.")
            else:
                D["invoices"] = pd.concat([D["invoices"], pd.DataFrame([{
                    "id":str(len(D["invoices"])+1),"order_id":oid,
                    "invoice_number":i_num,"invoice_date":str(i_date),"invoice_amount":str(i_amt),
                    "payment_status":i_pstat,"payment_date":str(i_pdate),"payment_mode":i_pmode,
                    "transaction_reference":i_txn,"invoice_files":f"{len(inv_f or [])} file(s)",
                    "updated_by":upd_by,"updated_at":now_ist()
                }])], ignore_index=True); save("invoices")
                ns = "Paid" if i_pstat=="Completed" else "Invoiced"
                update_status(oid, ns)
                log_action(oid,"STATUS_CHANGE",ord_row["current_status"],ns,upd_by,f"Invoice {i_num} | {i_pstat}")
                st.success(f"✅ Invoice saved! → **{ns}**"); st.rerun()
        fcard_end()

    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════════════════════
# ORDER DETAILS
# ══════════════════════════════════════════════════════════════════════════════
def page_order_details():
    topbar("🔍 Order Details", "Full order information, pipeline status and activity history")
    D = st.session_state.D
    PAD = "padding:0 28px;"
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)

    opts = ["— Select an order —"] + [
        f"{r['order_id']}  ·  {r['po_number']}  ·  {r['current_status']}"
        for _, r in D["orders"].iterrows()
    ]
    sel = st.selectbox("Select Order", opts, key="sel_details")
    if sel == "— Select an order —":
        st.info("👆 Select an order to view full details.")
        st.markdown('</div>', unsafe_allow_html=True); footer(); return

    oid = sel.split("  ·  ")[0].strip()
    o   = get_order(oid)
    s   = o["current_status"]

    # Header card
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
        padding:22px 24px;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:18px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
        <div>
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            {cobadge(o["company"])}
            <span style="font-size:18px;font-weight:800;color:#0f172a;">{o["order_id"]}</span>
          </div>
          <div style="font-size:13px;color:#64748b;">{o["po_number"]} · {o["govt_department"]}</div>
        </div>
        <div style="display:flex;gap:8px;">{sbadge(s)} {pbadge(o["priority"])}</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));
          gap:14px;margin-top:18px;padding-top:16px;border-top:1px solid #f1f5f9;">
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Contact</div><div style="font-size:13px;font-weight:600;">{o["contact_person"]}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Phone</div><div style="font-size:13px;font-weight:600;">{o["contact_phone"]}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Quantity</div><div style="font-size:13px;font-weight:600;">{o["quantity"]}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Assigned To</div><div style="font-size:13px;font-weight:600;">{o["assigned_company"] or "—"}</div></div>
        <div><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">Total Value</div><div style="font-size:18px;font-weight:800;">₹{float(o["total_value"]):,.0f}</div></div>
      </div>
      <div style="margin-top:14px;background:#f8fafc;border-radius:7px;border:1px solid #e2e8f0;padding:11px 14px;">
        <span style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;">Description: </span>
        <span style="font-size:13px;color:#1e293b;">{o["item_description"]}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Pipeline stepper
    cur  = STATUSES.index(s) if s in STATUSES else 0
    html = '<div style="display:flex;align-items:center;margin-bottom:24px;">'
    for i, step in enumerate(STATUSES):
        if i < cur:    cc,tc,lc = "#1d4ed8","#fff","#1d4ed8"; bd=""
        elif i == cur: cc,tc,lc = "#dbeafe","#1d4ed8","#1d4ed8"; bd="border:2px solid #1d4ed8;"
        else:          cc,tc,lc = "#f1f5f9","#94a3b8","#94a3b8"; bd=""
        html += (f'<div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">'
                 f'<div style="width:34px;height:34px;border-radius:50%;background:{cc};{bd}'
                 f'display:flex;align-items:center;justify-content:center;font-size:14px;color:{tc};">'
                 f'{SE.get(step,"")}</div>'
                 f'<div style="font-size:9.5px;font-weight:600;color:{lc};margin-top:5px;text-align:center;">{step}</div></div>')
        if i < len(STATUSES)-1:
            html += f'<div style="flex:1;height:2px;background:{"#1d4ed8" if i<cur else "#e2e8f0"};margin:0 4px 18px;"></div>'
    st.markdown(html+"</div>", unsafe_allow_html=True)

    def show_rec(tbl):
        rows = D[tbl][D[tbl]["order_id"]==oid]
        if len(rows)==0: st.info("No data recorded yet for this stage."); return
        row   = rows.iloc[-1]
        items = [(c.replace("_"," ").title(), str(row[c]))
                 for c in row.index if c not in ["id","order_id"] and str(row[c]) not in ["","nan"]]
        for i in range(0,len(items),3):
            ch = items[i:i+3]; cs = st.columns(3)
            for col,(lbl,val) in zip(cs,ch):
                with col:
                    st.markdown(
                        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;'
                        f'padding:11px 14px;margin-bottom:10px;">'
                        f'<div style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;">{lbl}</div>'
                        f'<div style="font-size:13px;font-weight:600;color:#0f172a;">{val}</div></div>',
                        unsafe_allow_html=True)

    t1,t2,t3,t4,t5 = st.tabs(["🔧 Procurement","🚚 Dispatch","📦 Delivery","💰 Invoice","📋 Activity"])
    with t1: show_rec("procurement")
    with t2: show_rec("dispatch")
    with t3: show_rec("delivery")
    with t4: show_rec("invoices")
    with t5:
        alogs = D["activity_log"][D["activity_log"]["order_id"]==oid].copy().iloc[::-1]
        if len(alogs)==0: st.info("No activity recorded yet.")
        for _,lg in alogs.iterrows():
            prev=lg.get("previous_status",""); nw=lg.get("new_status","")
            pb = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8">—</span>'
            nb = ("&nbsp;→&nbsp;"+sbadge(nw)) if nw and nw not in ["nan",""] else ""
            st.markdown(
                f'<div style="display:flex;gap:12px;background:#fff;border:1px solid #e2e8f0;'
                f'border-radius:10px;padding:13px 16px;margin-bottom:8px;">'
                f'<div style="width:9px;height:9px;border-radius:50%;background:#3b82f6;flex-shrink:0;margin-top:4px;"></div>'
                f'<div style="flex:1;"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
                f'<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">'
                f'<span style="font-size:11.5px;font-weight:700;background:#f1f5f9;padding:2px 8px;border-radius:5px;">{lg["action_type"]}</span>'
                f'{pb}{nb}</div>'
                f'<span style="font-size:11px;color:#94a3b8;">{lg["performed_at"]}</span></div>'
                f'<div style="font-size:12.5px;color:#374151;margin-top:5px;">{lg["details"]} — <b>{lg["performed_by"]}</b></div>'
                f'</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════════════════════
# ACTIVITY LOG
# ══════════════════════════════════════════════════════════════════════════════
def page_activity_log():
    topbar("📋 Activity Log","Complete audit trail of all order changes and updates")
    D    = st.session_state.D
    logs = D["activity_log"].copy().iloc[::-1].reset_index(drop=True)
    PAD  = "padding:0 28px;"
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;">'
        f'<div style="font-size:14px;font-weight:700;color:#0f172a;">📋 All System Events</div>'
        f'<div style="font-size:11px;font-weight:600;color:#64748b;background:#f1f5f9;padding:3px 12px;border-radius:20px;">{len(logs)} events</div>'
        f'</div><div style="padding:16px;">',
        unsafe_allow_html=True)
    for _,lg in logs.iterrows():
        prev=lg.get("previous_status",""); nw=lg.get("new_status","")
        pb = sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8">—</span>'
        nb = ("&nbsp;→&nbsp;"+sbadge(nw)) if nw and nw not in ["nan",""] else ""
        st.markdown(
            f'<div style="display:flex;gap:12px;background:#fff;border:1px solid #e2e8f0;'
            f'border-radius:10px;padding:13px 16px;margin-bottom:8px;">'
            f'<div style="width:9px;height:9px;border-radius:50%;background:#3b82f6;flex-shrink:0;margin-top:4px;"></div>'
            f'<div style="flex:1;"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
            f'<div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">'
            f'<span style="font-size:11.5px;font-weight:700;background:#f1f5f9;padding:2px 8px;border-radius:5px;">{lg["action_type"]}</span>'
            f'<span style="font-size:12px;font-weight:700;color:#1d4ed8;">{lg["order_id"]}</span>'
            f'{pb}{nb}</div>'
            f'<span style="font-size:11px;color:#94a3b8;white-space:nowrap;">{lg["performed_at"]}</span></div>'
            f'<div style="font-size:12.5px;color:#374151;margin-top:5px;">{lg["details"]} — <b>{lg["performed_by"]}</b></div>'
            f'</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════════════════════════════════════
def page_reports():
    topbar("📈 Reports","Financial summaries and order analytics")
    D  = st.session_state.D
    df = D["orders"].copy()
    df["total_value"] = df["total_value"].astype(float)
    PAD = "padding:0 28px;"
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)

    c1,c2 = st.columns(2, gap="medium")
    def prog(fg,pct):
        return f'<div style="background:#f1f5f9;border-radius:4px;height:6px;"><div style="width:{pct}%;background:{fg};border-radius:4px;height:6px;"></div></div>'

    with c1:
        st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;"><div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;font-size:14px;font-weight:700;color:#0f172a;">🏢 By Company</div><div style="padding:18px;">', unsafe_allow_html=True)
        for co in COMPANIES:
            rows=df[df["company"]==co]; cnt=len(rows); val=rows["total_value"].sum()
            pct=int(cnt/max(len(df),1)*100); fg=CF.get(co,"#64748b"); bg=CB.get(co,"#f1f5f9")
            st.markdown(f'<div style="margin-bottom:16px;"><div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;background:{bg};color:{fg};">{co}</span><span style="font-size:12.5px;font-weight:700;color:{fg};">{cnt} orders · ₹{val/1e5:.1f}L</span></div>{prog(fg,pct)}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;"><div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;font-size:14px;font-weight:700;color:#0f172a;">📊 By Status</div><div style="padding:18px;">', unsafe_allow_html=True)
        for status in STATUSES:
            cnt=len(df[df["current_status"]==status]); pct=int(cnt/max(len(df),1)*100)
            fg=SF.get(status,"#64748b"); bg=SB.get(status,"#f1f5f9")
            st.markdown(f'<div style="margin-bottom:14px;"><div style="display:flex;justify-content:space-between;margin-bottom:5px;"><span style="display:inline-block;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;background:{bg};color:{fg};">{SE.get(status,"")} {status}</span><span style="font-size:13px;font-weight:700;color:{fg};">{cnt}</span></div>{prog(fg,pct)}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # Financial table
    TH="padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;"
    TD="padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
    rows_h=""; out_total=0.0
    for i,(_,r) in enumerate(df.iterrows()):
        bg="#fff" if i%2==0 else "#fafbfc"; tv=float(r["total_value"])
        paid=f'<span style="color:#15803d;font-weight:700;">₹{tv:,.0f}</span>' if r["current_status"]=="Paid" else "—"
        owed="—" if r["current_status"]=="Paid" else f'<span style="color:#92400e;font-weight:700;">₹{tv:,.0f}</span>'
        if r["current_status"]!="Paid": out_total+=tv
        rows_h+=f'<tr style="background:{bg}"><td style="{TD}font-size:11.5px;color:#64748b;">{r["order_id"]}</td><td style="{TD}">{cobadge(r["company"])}</td><td style="{TD}">{r["govt_department"]}</td><td style="{TD}font-weight:700;">₹{tv:,.0f}</td><td style="{TD}">{sbadge(r["current_status"])}</td><td style="{TD}">{paid}</td><td style="{TD}">{owed}</td></tr>'
    st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:20px;"><div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;font-size:14px;font-weight:700;color:#0f172a;">💵 Financial Summary</div><div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr><th style="{TH}">Order ID</th><th style="{TH}">Company</th><th style="{TH}">Department</th><th style="{TH}">Value</th><th style="{TH}">Status</th><th style="{TH}">Paid</th><th style="{TH}">Outstanding</th></tr></thead><tbody>{rows_h}</tbody></table></div><div style="padding:12px 20px;background:#f8fafc;border-top:1px solid #e2e8f0;display:flex;justify-content:space-between;font-size:13px;font-weight:700;"><span style="color:#64748b;">Total Outstanding</span><span style="color:#92400e;">₹{out_total:,.0f}</span></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════════════════════
def page_admin():
    topbar("⚙️ Admin Panel","Export data, view statistics, manage user accounts")
    D  = st.session_state.D
    PAD = "padding:0 28px;"
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.info("✅ **Auto-Save** active — all changes persist to CSV files automatically.")

    tables = ["orders","procurement","dispatch","delivery","invoices","activity_log"]

    # Export section
    fcard("📥 Export Data", "Download individual or combined CSV files")
    cs = st.columns(3)
    for i, t in enumerate(tables):
        with cs[i%3]:
            st.download_button(f"📄 {t} ({len(D[t])} rows)",
                               D[t].to_csv(index=False).encode(),
                               f"sc_{t}_{now_ist()[:10]}.csv","text/csv",
                               use_container_width=True, key=f"dl_{t}")
    g(8)
    all_csv = "\n\n".join([f"=== {t.upper()} ===\n"+D[t].to_csv(index=False) for t in tables])
    st.download_button("📦 Export ALL Tables (Single File)", all_csv.encode(),
                       f"sc_full_{now_ist()[:10]}.csv","text/csv",
                       use_container_width=True, key="dl_all", type="primary")
    fcard_end()
    g(12)

    # DB Stats
    stat_h = "".join([
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-top:3px solid #1d4ed8;border-radius:8px;padding:12px;text-align:center;">'
        f'<div style="font-size:10px;font-weight:700;color:#64748b;text-transform:uppercase;">{t}</div>'
        f'<div style="font-size:22px;font-weight:800;color:#1d4ed8;margin-top:6px;">{len(D[t])}</div>'
        f'<div style="font-size:10px;color:#94a3b8;">rows</div></div>'
        for t in tables])
    st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:16px;"><div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;font-size:14px;font-weight:700;color:#0f172a;">⚙️ Database Statistics</div><div style="padding:18px;display:grid;grid-template-columns:repeat(6,1fr);gap:12px;">{stat_h}</div></div>', unsafe_allow_html=True)

    # Users table
    TH="padding:10px 16px;background:#f8fafc;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;"
    TD="padding:12px 16px;border-bottom:1px solid #f1f5f9;font-size:12.5px;"
    RDESC={"Admin":"Full access — all pages","Manager":"No admin panel","Staff":"Update orders only","Viewer":"Read-only"}
    rows_h="".join([
        f'<tr style="background:{"#fff" if i%2==0 else "#fafbfc"}">'
        f'<td style="{TD}font-weight:700;font-family:monospace;">{u}</td>'
        f'<td style="{TD}">{v["name"]}</td>'
        f'<td style="{TD}"><span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;background:{RB.get(v["role"],"#f1f5f9")};color:{RC.get(v["role"],"#64748b")};">{v["role"]}</span></td>'
        f'<td style="{TD}color:#64748b;font-size:12px;">{RDESC.get(v["role"],"")}</td></tr>'
        for i,(u,v) in enumerate(USERS.items())])
    st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:16px;"><div style="padding:14px 20px;border-bottom:1px solid #f1f5f9;background:#fafbfc;font-size:14px;font-weight:700;color:#0f172a;">👥 User Accounts & Roles</div><div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr><th style="{TH}">Username</th><th style="{TH}">Full Name</th><th style="{TH}">Role</th><th style="{TH}">Permissions</th></tr></thead><tbody>{rows_h}</tbody></table></div></div>', unsafe_allow_html=True)

    # Danger zone
    with st.expander("⚠️ Danger Zone — Reset All Data"):
        st.warning("Permanently deletes all data and restores sample records. This cannot be undone.")
        if st.button("🗑 Reset to Sample Data", type="primary", key="btn_reset"):
            for k, df in make_seed().items():
                df.to_csv(FILES[k], index=False)
            st.session_state.D = load_data()
            st.success("✅ Data reset to sample records."); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    render_sidebar()

    # Guard page access by role
    allowed = MENUS.get(st.session_state.role, [])
    if st.session_state.page not in allowed:
        st.session_state.page = "Dashboard"
        st.rerun()

    {
        "Dashboard":     page_dashboard,
        "New Order":     page_new_order,
        "Update Order":  page_update_order,
        "Order Details": page_order_details,
        "Activity Log":  page_activity_log,
        "Reports":       page_reports,
        "Admin":         page_admin,
    }[st.session_state.page]()

if __name__ == "__main__":
    main()
