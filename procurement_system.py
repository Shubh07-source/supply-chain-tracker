import streamlit as st
import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
# CRITICAL: "collapsed" is the only way to permanently kill the >> arrow.
# We expand it via CSS when needed. display:none on collapsedControl alone
# is not reliable across Streamlit Cloud versions.
st.set_page_config(
    page_title="Supply Chain Tracking",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",   # ← kills >> arrow permanently
)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
COMPANIES  = ["Robokart","Bharat Tech","EL"]
STATUSES   = ["Pending","Procured","Dispatched","Delivered","Invoiced","Paid"]
PRIORITIES = ["Low","Medium","High","Urgent"]
SE = {"Pending":"⏳","Procured":"🔧","Dispatched":"🚚","Delivered":"📦","Invoiced":"🧾","Paid":"💰"}
SB = {"Pending":"#fef3c7","Procured":"#dbeafe","Dispatched":"#ede9fe","Delivered":"#d1fae5","Invoiced":"#cffafe","Paid":"#dcfce7"}
SF = {"Pending":"#92400e","Procured":"#1e40af","Dispatched":"#5b21b6","Delivered":"#065f46","Invoiced":"#155e75","Paid":"#14532d"}
PB = {"Low":"#f1f5f9","Medium":"#dbeafe","High":"#fef9c3","Urgent":"#fee2e2"}
PF = {"Low":"#475569","Medium":"#1e40af","High":"#92400e","Urgent":"#dc2626"}
CB = {"Robokart":"#ede9fe","Bharat Tech":"#cffafe","EL":"#ffedd5"}
CF = {"Robokart":"#5b21b6","Bharat Tech":"#155e75","EL":"#9a3412"}
RC = {"Admin":"#dc2626","Manager":"#d97706","Staff":"#2563eb","Viewer":"#059669"}
RB = {"Admin":"#fee2e2","Manager":"#fef3c7","Staff":"#dbeafe","Viewer":"#dcfce7"}
SC = {"Pending":"#f59e0b","Procured":"#3b82f6","Dispatched":"#8b5cf6","Delivered":"#10b981","Invoiced":"#06b6d4","Paid":"#22c55e"}
CC = {"Robokart":"#8b5cf6","Bharat Tech":"#06b6d4","EL":"#f59e0b"}
USERS = {
    "Admin":   {"password":"admin@123",    "role":"Admin",   "name":"System Admin"},
    "Manager": {"password":"mgr@123",      "role":"Manager", "name":"Ops Manager"},
    "Staff":   {"password":"Ops@Secure#1", "role":"Staff",   "name":"Operations Staff"},
    "Viewer":  {"password":"view123",      "role":"Viewer",  "name":"Finance Viewer"},
}
MENUS = {
    "Admin":   ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports","Manage Records","Admin Panel"],
    "Manager": ["Dashboard","New Order","Update Order","Order Details","Activity Log","Reports"],
    "Staff":   ["Dashboard","Update Order","Order Details","Activity Log"],
    "Viewer":  ["Dashboard","Order Details","Activity Log"],
}
ICONS = {"Dashboard":"📊","New Order":"➕","Update Order":"🔄","Order Details":"🔍",
         "Activity Log":"📋","Reports":"📈","Manage Records":"🗂️","Admin Panel":"⚙️"}

# ─── DATA ─────────────────────────────────────────────────────────────────────
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
    return datetime.now(timezone(timedelta(hours=5,minutes=30))).strftime("%Y-%m-%d %H:%M:%S")

def load_data():
    seed = make_seed(); out = {}
    for k,path in FILES.items():
        if os.path.exists(path): out[k] = pd.read_csv(path,dtype=str).fillna("")
        else: d=seed[k].copy(); d.to_csv(path,index=False); out[k]=d
    return out

def save(k): st.session_state.D[k].to_csv(FILES[k], index=False)

def log_action(oid,action,prev,nxt,by,detail):
    D=st.session_state.D
    n=pd.DataFrame([{"id":str(len(D["activity_log"])+1),"order_id":oid,"action_type":action,
      "previous_status":prev,"new_status":nxt,"performed_by":by,"performed_at":now_ist(),"details":detail}])
    D["activity_log"]=pd.concat([D["activity_log"],n],ignore_index=True); save("activity_log")

def set_status(oid,ns):
    D=st.session_state.D
    D["orders"].loc[D["orders"]["order_id"]==oid,"current_status"]=ns
    D["orders"].loc[D["orders"]["order_id"]==oid,"last_updated"]=now_ist(); save("orders")

def get_order(oid):
    r=st.session_state.D["orders"]; r=r[r["order_id"]==oid]
    return r.iloc[0] if len(r) else None

# ─── SESSION STATE ────────────────────────────────────────────────────────────
for k,v in {"logged_in":False,"username":"","role":"","user_name":"",
             "page":"Dashboard","co_filter":"All","login_error":"","sb_open":True}.items():
    if k not in st.session_state: st.session_state[k]=v
if "D" not in st.session_state: st.session_state.D=load_data()

# ═══════════════════════════════════════════════════════════════════════════════
# MASTER CSS
# Why initial_sidebar_state="collapsed" + CSS expand works:
#   Streamlit only shows the >> button when sidebar starts EXPANDED then gets
#   collapsed by the user. Starting in "collapsed" state means Streamlit treats
#   it as default-off; the >> never appears. We then force-expand via CSS.
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
*{box-sizing:border-box;}
html,body,.stApp{font-family:'DM Sans',sans-serif !important; background:#f1f5f9 !important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0 !important; max-width:100% !important;}
section.main>div{padding:0 !important;}

/* ── NUKE BOTH COLLAPSE CONTROLS ────────────────────────────────────────── */
[data-testid="collapsedControl"],
button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"],
button[title="Close sidebar"],
button[title="Open sidebar"]{
    display:none !important;
    visibility:hidden !important;
    width:0 !important; height:0 !important;
    overflow:hidden !important;
    pointer-events:none !important;
}

/* ── SIDEBAR BASE ────────────────────────────────────────────────────────── */
[data-testid="stSidebar"]{
    background:#0f172a !important;
    border-right:1px solid #1e293b !important;
    transition:width .2s ease, min-width .2s ease !important;
}
[data-testid="stSidebar"]>div:first-child{padding:0 !important;}
/* All sidebar text = slate */
[data-testid="stSidebar"] *{
    color:#94a3b8 !important;
    -webkit-text-fill-color:#94a3b8 !important;
}
[data-testid="stSidebar"] .stButton>button{
    width:calc(100% - 16px) !important; text-align:left !important;
    background:transparent !important; border:none !important;
    border-radius:8px !important;
    color:#94a3b8 !important; -webkit-text-fill-color:#94a3b8 !important;
    font-size:13.5px !important; font-weight:500 !important;
    padding:10px 16px !important; margin:1px 8px !important; box-shadow:none !important;
}
[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(255,255,255,.07) !important;
    color:#e2e8f0 !important; -webkit-text-fill-color:#e2e8f0 !important;
}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{
    background:linear-gradient(135deg,#4f46e5,#6366f1) !important;
    color:#fff !important; -webkit-text-fill-color:#fff !important;
    font-weight:700 !important; box-shadow:0 2px 8px rgba(99,102,241,.4) !important;
}

/* ── INPUTS ──────────────────────────────────────────────────────────────── */
input,input[type],input[type="text"],input[type="password"],
input[type="number"],input[type="email"],input[type="date"],textarea,
div[data-baseweb="input"] input,div[data-baseweb="base-input"] input,
.stTextInput input,.stTextInput>div>div>input,
.stNumberInput input,.stDateInput input{
    background:#fff !important; color:#111827 !important;
    -webkit-text-fill-color:#111827 !important; caret-color:#111827 !important;
    opacity:1 !important; border:1.5px solid #e2e8f0 !important;
    border-radius:8px !important; font-size:14px !important;
}
input::placeholder,textarea::placeholder{
    color:#9ca3af !important; -webkit-text-fill-color:#9ca3af !important; opacity:1 !important;
}
input:focus,textarea:focus{
    background:#fff !important; color:#111827 !important;
    -webkit-text-fill-color:#111827 !important;
    border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.15) !important;
    outline:none !important;
}
div[data-baseweb="input"],div[data-baseweb="base-input"],
.stTextInput>div>div,.stNumberInput>div>div,.stDateInput>div>div{
    background:#fff !important; border-radius:8px !important;
}

/* ── LABELS ──────────────────────────────────────────────────────────────── */
label,.stTextInput label,.stTextArea label,.stSelectbox label,
.stNumberInput label,.stDateInput label,
div[data-testid="stWidgetLabel"] p,div[data-testid="stWidgetLabel"] label{
    color:#374151 !important; -webkit-text-fill-color:#374151 !important;
    font-size:13px !important; font-weight:600 !important;
}

/* ── SELECTBOX ───────────────────────────────────────────────────────────── */
div[data-baseweb="select"]>div,.stSelectbox>div>div{
    background:#fff !important; border:1.5px solid #e2e8f0 !important;
    border-radius:8px !important; color:#111827 !important;
}

/* ── GLOBAL MAIN-CONTENT TEXT = DARK ─────────────────────────────────────
   Fixes white/invisible text in Activity Log, Admin Panel, Expanders.
   We override BOTH color and -webkit-text-fill-color.                    */
section[data-testid="stMain"] .stMarkdown,
section[data-testid="stMain"] .stMarkdown p,
section[data-testid="stMain"] .stMarkdown li,
section[data-testid="stMain"] .stMarkdown h1,
section[data-testid="stMain"] .stMarkdown h2,
section[data-testid="stMain"] .stMarkdown h3,
section[data-testid="stMain"] p,
section[data-testid="stMain"] li,
section[data-testid="stMain"] h1,
section[data-testid="stMain"] h2,
section[data-testid="stMain"] h3{
    color:#1e293b !important;
    -webkit-text-fill-color:#1e293b !important;
}
/* Expander header (Danger Zone etc) */
details>summary,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
.streamlit-expanderHeader,
.streamlit-expanderHeader p,
.streamlit-expanderHeader span{
    color:#1e293b !important;
    -webkit-text-fill-color:#1e293b !important;
    font-weight:600 !important;
}
/* Alert/info/warning text */
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
div[role="alert"] p{
    color:#1e293b !important;
    -webkit-text-fill-color:#1e293b !important;
}

/* ── BUTTONS ─────────────────────────────────────────────────────────────── */
.stButton>button{
    border-radius:8px !important; font-weight:600 !important;
    font-size:13px !important; cursor:pointer !important; transition:all .15s !important;
}
.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,#4f46e5,#6366f1) !important; border:none !important;
    color:#fff !important; -webkit-text-fill-color:#fff !important;
    box-shadow:0 2px 8px rgba(99,102,241,.3) !important;
}
.stButton>button[kind="secondary"]{
    background:#fff !important; border:1.5px solid #e2e8f0 !important;
    color:#374151 !important; -webkit-text-fill-color:#374151 !important;
}
.stButton>button[kind="secondary"]:hover{
    border-color:#6366f1 !important;
    color:#4f46e5 !important; -webkit-text-fill-color:#4f46e5 !important;
}
.stFormSubmitButton>button{
    background:linear-gradient(135deg,#4f46e5,#6366f1) !important; border:none !important;
    color:#fff !important; -webkit-text-fill-color:#fff !important;
    font-weight:700 !important; box-shadow:0 2px 8px rgba(99,102,241,.3) !important;
}

/* ── TABS ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{background:transparent !important; border-bottom:2px solid #e2e8f0 !important; gap:0; padding:0;}
.stTabs [data-baseweb="tab"]{background:transparent !important; border:none !important; border-bottom:2px solid transparent !important; color:#64748b !important; -webkit-text-fill-color:#64748b !important; font-weight:500 !important; font-size:13px !important; padding:10px 20px !important; margin-bottom:-2px !important;}
.stTabs [aria-selected="true"]{border-bottom:2px solid #6366f1 !important; color:#4f46e5 !important; -webkit-text-fill-color:#4f46e5 !important; font-weight:700 !important;}
</style>
""", unsafe_allow_html=True)


# ─── DYNAMIC SIDEBAR STATE CSS ────────────────────────────────────────────────
# Since initial_sidebar_state="collapsed", we expand it via CSS when needed.
# When sb_open=True → force 252px. When False or login → keep 0 (already collapsed).
# All selectors known to Streamlit across versions for the native >> button
_HIDE_ARROW_CSS = """
[data-testid="collapsedControl"],button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],button[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"],button[aria-label="Open sidebar"],
button[title="Close sidebar"],button[title="Open sidebar"],
[data-testid="stSidebarNav"] button, section[data-testid="stSidebar"] > div:first-child > div:first-child > button{
    display:none !important; visibility:hidden !important;
    width:0 !important; height:0 !important;
    overflow:hidden !important; pointer-events:none !important;
    position:absolute !important; opacity:0 !important;
}
"""

def _sidebar_css():
    logged  = st.session_state.get("logged_in", False)
    sb_open = st.session_state.get("sb_open", True)
    if logged and sb_open:
        st.markdown(f"""<style>
        {_HIDE_ARROW_CSS}
        section[data-testid="stSidebar"]{{
            width:252px !important; min-width:252px !important;
            max-width:252px !important; transform:translateX(0) !important;
            visibility:visible !important; overflow:visible !important;
        }}
        </style>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<style>
        {_HIDE_ARROW_CSS}
        section[data-testid="stSidebar"]{{
            width:0 !important; min-width:0 !important;
            max-width:0 !important; overflow:hidden !important;
        }}
        </style>""", unsafe_allow_html=True)

_sidebar_css()


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def sbadge(s):
    bg=SB.get(s,"#f1f5f9"); fg=SF.get(s,"#475569")
    return f'<span style="display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;background:{bg};color:{fg} !important;-webkit-text-fill-color:{fg} !important;white-space:nowrap;">{SE.get(s,"")} {s}</span>'
def pbadge(p):
    bg=PB.get(p,"#f1f5f9"); fg=PF.get(p,"#475569")
    return f'<span style="display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;background:{bg};color:{fg} !important;-webkit-text-fill-color:{fg} !important;">{p}</span>'
def cobadge(c):
    bg=CB.get(c,"#f1f5f9"); fg=CF.get(c,"#475569")
    return f'<span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;background:{bg};color:{fg} !important;-webkit-text-fill-color:{fg} !important;">{c}</span>'
def sp(px=12): st.markdown(f'<div style="height:{px}px"></div>',unsafe_allow_html=True)
def dark(txt,size=13,weight=400): return f'<span style="color:#1e293b !important;-webkit-text-fill-color:#1e293b !important;font-size:{size}px;font-weight:{weight};">{txt}</span>'
def section_label(t): st.markdown(f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#94a3b8;border-bottom:1px solid #f1f5f9;padding-bottom:8px;margin:14px 0 12px;">{t}</div>',unsafe_allow_html=True)
def footer(): st.markdown(f'<div style="text-align:center;font-size:11px;color:#94a3b8;padding:18px 0 12px;border-top:1px solid #e2e8f0;margin-top:32px;">© {datetime.now().year} Robokart · Supply Chain Tracking</div>',unsafe_allow_html=True)

# ── Plotly base font (kept as alias; canonical is _BLK defined below) ──────────
PF_CHART = dict(family="DM Sans, sans-serif", color="#111827", size=12)

_BLK = dict(family="DM Sans, sans-serif", color="#111827", size=12)

def chart_layout(title_text, **overrides):
    base = dict(
        title=dict(text=title_text, font=dict(size=13, color="#111827", family="DM Sans"), x=0),
        paper_bgcolor="white", plot_bgcolor="white",
        font=_BLK,
        margin=dict(t=46, b=50, l=60, r=16),
        height=265,
        showlegend=False,
        xaxis=dict(
            showgrid=False, tickfont=_BLK, linecolor="#cbd5e1",
            tickcolor="#cbd5e1", title_font=_BLK,
            ticklabelstandoff=4,
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#f0f4f8", tickfont=_BLK,
            linecolor="#cbd5e1", title_font=_BLK,
        ),
    )
    base.update(overrides)
    return base


# ─── TOPBAR ───────────────────────────────────────────────────────────────────
def topbar(title, sub=""):
    sub_h = f'<div style="font-size:12px;color:#64748b;margin-top:2px;">{sub}</div>' if sub else ""
    icon  = "☰" if not st.session_state.get("sb_open",True) else "✕"
    cb, ct, cr = st.columns([0.5, 8, 3])
    with cb:
        sp(8)
        if st.button(icon, key="tb_tog", type="secondary"):
            st.session_state.sb_open = not st.session_state.get("sb_open",True)
            st.rerun()
    with ct:
        st.markdown(f'<div style="padding:14px 0 12px;"><div style="font-size:18px;font-weight:800;color:#0f172a;">{title}</div>{sub_h}</div>',unsafe_allow_html=True)
    with cr:
        ist = datetime.now(timezone(timedelta(hours=5,minutes=30))).strftime("%d %b %Y, %I:%M %p")
        st.markdown(f'<div style="padding:14px 24px 12px;text-align:right;display:flex;align-items:center;justify-content:flex-end;gap:10px;"><div style="display:flex;align-items:center;gap:6px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600;color:#15803d;">● Auto-saved</div><div style="font-size:11px;color:#64748b;font-weight:500;">🕐 {ist} IST</div></div>',unsafe_allow_html=True)
    st.markdown('<div style="height:1px;background:#e2e8f0;margin:0 0 20px;"></div>',unsafe_allow_html=True)


# ─── LOGIN ────────────────────────────────────────────────────────────────────
def login_page():
    # ── The ONLY reliable way in Streamlit: style the stForm block directly as
    # the glass card. No HTML wrappers around widgets — they always break apart.
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800;900&display=swap');

    /* 1. Full-viewport purple gradient, no scroll */
    html, body { overflow:hidden !important; height:100% !important; margin:0 !important; }
    .stApp {
        background: linear-gradient(135deg, #3730a3 0%, #5b21b6 50%, #7c3aed 100%) !important;
        height:100vh !important; overflow:hidden !important;
        font-family:'DM Sans',sans-serif !important;
    }
    #MainMenu, footer, header, [data-testid="collapsedControl"],
    section[data-testid="stSidebar"] { display:none !important; }

    /* 2. Streamlit layout containers — transparent, no padding */
    .block-container {
        padding:0 !important; max-width:460px !important;
        margin:0 auto !important;
    }
    section[data-testid="stMain"] > div {
        padding:0 !important; height:100vh !important;
        display:flex !important; flex-direction:column !important;
        align-items:center !important; justify-content:center !important;
    }
    section[data-testid="stMain"] > div > div:first-child {
        width:100% !important; max-width:460px !important;
    }

    /* 3. The heading HTML block — glass top */
    .login-card-top {
        background: rgba(255,255,255,0.13) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-bottom: none !important;
        border-radius: 22px 22px 0 0 !important;
        padding: 40px 40px 28px !important;
        text-align: center !important;
    }

    /* 4. The stForm element IS the glass card middle */
    section[data-testid="stForm"],
    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.13) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-top: none !important;
        border-bottom: none !important;
        border-radius: 0 !important;
        padding: 28px 40px 24px !important;
        box-shadow: none !important;
    }

    /* 5. Footer HTML block — glass bottom */
    .login-card-bottom {
        background: rgba(255,255,255,0.10) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-top: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 0 0 22px 22px !important;
        padding: 18px 40px 26px !important;
        text-align: center !important;
    }

    /* 6. INPUTS — glass style, white text */
    section[data-testid="stForm"] input[type="text"],
    section[data-testid="stForm"] input[type="password"],
    section[data-testid="stForm"] .stTextInput input {
        background: rgba(255,255,255,0.18) !important;
        background-color: rgba(255,255,255,0.18) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
        border: 1.5px solid rgba(255,255,255,0.35) !important;
        border-radius: 12px !important;
        height: 52px !important;
        font-size: 15px !important;
        padding: 0 18px !important;
        font-family: 'DM Sans',sans-serif !important;
        opacity: 1 !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    section[data-testid="stForm"] input::placeholder {
        color: rgba(255,255,255,0.55) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.55) !important;
    }
    section[data-testid="stForm"] input:focus {
        background: rgba(255,255,255,0.25) !important;
        background-color: rgba(255,255,255,0.25) !important;
        border-color: rgba(255,255,255,0.7) !important;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.1) !important;
        outline: none !important;
    }
    section[data-testid="stForm"] div[data-baseweb="input"],
    section[data-testid="stForm"] div[data-baseweb="base-input"],
    section[data-testid="stForm"] .stTextInput > div > div {
        background: transparent !important;
        border: none !important;
        border-radius: 12px !important;
    }

    /* 7. HIDE labels (placeholders serve as labels) */
    section[data-testid="stForm"] .stTextInput label,
    section[data-testid="stForm"] div[data-testid="stWidgetLabel"] {
        display: none !important;
        height: 0 !important; margin: 0 !important; padding: 0 !important;
    }

    /* 8. SIGN IN BUTTON */
    section[data-testid="stForm"] .stFormSubmitButton > button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        border: none !important;
        color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
        font-size: 16px !important; font-weight: 700 !important;
        height: 54px !important; border-radius: 12px !important;
        box-shadow: 0 6px 24px rgba(37,99,235,0.5) !important;
        width: 100% !important; letter-spacing: .04em !important;
        font-family: 'DM Sans',sans-serif !important;
    }
    section[data-testid="stForm"] .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        box-shadow: 0 8px 32px rgba(37,99,235,0.65) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── HEADING block (styled as glass card top via CSS class) ─────────────────
    st.markdown("""
    <div class="login-card-top">
      <div style="display:flex;align-items:center;justify-content:center;
           gap:12px;margin-bottom:20px;">
        <div style="width:46px;height:46px;border-radius:12px;flex-shrink:0;
             background:linear-gradient(135deg,#312e81,#4f46e5);
             display:flex;align-items:center;justify-content:center;font-size:23px;
             box-shadow:0 4px 14px rgba(79,70,229,0.45);">🏭</div>
        <div style="text-align:left;">
          <div style="font-size:15px;font-weight:800;color:#ffffff;letter-spacing:-.1px;
               font-family:'DM Sans',sans-serif;">Supply Chain</div>
          <div style="font-size:10px;color:rgba(255,255,255,0.55);font-weight:500;
               letter-spacing:.9px;text-transform:uppercase;font-family:'DM Sans',sans-serif;">
            Tracking System</div>
        </div>
      </div>
      <div style="font-size:28px;font-weight:900;color:#ffffff;letter-spacing:-.4px;
           margin-bottom:6px;font-family:'DM Sans',sans-serif;">Welcome Back</div>
      <div style="font-size:14px;color:rgba(255,255,255,0.6);
           font-family:'DM Sans',sans-serif;">Sign in to your account</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FORM (Streamlit stForm = glass card middle, styled via CSS above) ─────
    # Make labels visible and white
    st.markdown("""<style>
    section[data-testid="stForm"] .stTextInput label,
    section[data-testid="stForm"] div[data-testid="stWidgetLabel"],
    section[data-testid="stForm"] div[data-testid="stWidgetLabel"] p {
        display:block !important;
        height:auto !important; margin-bottom:6px !important;
        color:#ffffff !important;
        -webkit-text-fill-color:#ffffff !important;
        font-size:13.5px !important; font-weight:700 !important;
        font-family:'DM Sans',sans-serif !important;
        opacity:1 !important;
    }
    </style>""", unsafe_allow_html=True)
    with st.form("lf", clear_on_submit=False):
        uname = st.text_input("Username", placeholder="Enter your username",
                               key="lu")
        sp(10)
        pword = st.text_input("Password", placeholder="Password",
                               type="password", key="lp")
        sp(18)
        submitted = st.form_submit_button("Sign In",
                                           use_container_width=True, type="primary")

    # ── FOOTER ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="login-card-bottom">
      <span style="font-size:12.5px;color:rgba(255,255,255,0.45);
           font-family:'DM Sans',sans-serif;">
        🔒 &nbsp;Secured &nbsp;·&nbsp; Contact your administrator for access
      </span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("login_error"):
        sp(8)
        st.error(st.session_state.login_error)

    if submitted:
        u = uname.strip()
        if u in USERS and USERS[u]["password"] == pword:
            st.session_state.logged_in   = True
            st.session_state.username    = u
            st.session_state.role        = USERS[u]["role"]
            st.session_state.user_name   = USERS[u]["name"]
            st.session_state.page        = "Dashboard"
            st.session_state.login_error = ""
            st.session_state.sb_open     = True
            st.rerun()
        else:
            st.session_state.login_error = "⚠️  Invalid username or password."
            st.rerun()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def render_sidebar():
    if not st.session_state.get("sb_open",True):
        return
    with st.sidebar:
        st.markdown("""<div style="padding:20px 16px 16px;border-bottom:1px solid #1e293b;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:38px;height:38px;border-radius:10px;flex-shrink:0;
                 background:linear-gradient(135deg,#312e81,#4f46e5);
                 display:flex;align-items:center;justify-content:center;font-size:20px;">🏭</div>
            <div>
              <div style="font-size:13.5px;font-weight:800;color:#f8fafc !important;-webkit-text-fill-color:#f8fafc !important;">Supply Chain</div>
              <div style="font-size:9px;color:#475569 !important;-webkit-text-fill-color:#475569 !important;letter-spacing:1.2px;text-transform:uppercase;">Tracking System</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        sp(8)
        st.markdown('<div style="padding:0 16px;font-size:9px;font-weight:700;letter-spacing:1.4px;color:#334155;text-transform:uppercase;margin-bottom:4px;">MENU</div>',unsafe_allow_html=True)
        for m in MENUS.get(st.session_state.role,[]):
            active=(st.session_state.page==m)
            if st.button(f"{ICONS.get(m,'')}  {m}",key=f"nav_{m}",
                         use_container_width=True,type="primary" if active else "secondary"):
                st.session_state.page=m; st.rerun()
        sp(12)
        st.markdown('<div style="height:1px;background:#1e293b;margin:0 14px 12px;"></div>',unsafe_allow_html=True)
        role=st.session_state.role; rc=RC.get(role,"#64748b"); rb=RB.get(role,"#1e293b")
        ini="".join(w[0].upper() for w in st.session_state.user_name.split()[:2])
        st.markdown(f"""<div style="padding:0 12px 10px;">
          <div style="background:#1e293b;border-radius:10px;padding:10px 12px;display:flex;align-items:center;gap:10px;">
            <div style="width:34px;height:34px;border-radius:8px;flex-shrink:0;background:{rc};
                 color:#fff !important;-webkit-text-fill-color:#fff !important;font-size:12px;font-weight:800;
                 display:flex;align-items:center;justify-content:center;">{ini}</div>
            <div style="overflow:hidden;">
              <div style="font-size:12.5px;font-weight:700;color:#f1f5f9 !important;-webkit-text-fill-color:#f1f5f9 !important;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{st.session_state.user_name}</div>
              <span style="font-size:10px;font-weight:700;background:{rb};color:{rc} !important;-webkit-text-fill-color:{rc} !important;padding:1px 8px;border-radius:4px;">{role}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button("⬅  Sign Out",key="so_btn",use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
        sp(8)


# ─── ACTIVITY LOG ROW ─────────────────────────────────────────────────────────
def _log_row(log):
    prev=str(log.get("previous_status","")); ns_l=str(log.get("new_status",""))
    pb=sbadge(prev) if prev and prev not in ["—","nan",""] else '<span style="color:#94a3b8;">—</span>'
    nb="&nbsp;→&nbsp;"+sbadge(ns_l) if ns_l and ns_l not in ["nan",""] else ""
    atype=str(log.get("action_type","")); oid=str(log.get("order_id",""))
    det=str(log.get("details","")); by=str(log.get("performed_by","")); ts=str(log.get("performed_at",""))
    st.markdown(
        f'<div style="display:flex;gap:10px;background:#fff;border:1px solid #e2e8f0;'
        f'border-radius:10px;padding:11px 14px;margin-bottom:7px;">'
        f'<div style="width:8px;height:8px;border-radius:50%;background:#6366f1;flex-shrink:0;margin-top:5px;"></div>'
        f'<div style="flex:1;">'
        f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:5px;align-items:center;">'
        f'<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">'
        f'<span style="font-size:11px;font-weight:700;background:#f1f5f9;color:#374151 !important;-webkit-text-fill-color:#374151 !important;padding:2px 8px;border-radius:5px;">{atype}</span>'
        f'<span style="font-size:11.5px;font-weight:700;color:#4f46e5 !important;-webkit-text-fill-color:#4f46e5 !important;">{oid}</span>'
        f'{pb}{nb}'
        f'</div>'
        f'<span style="font-size:10.5px;color:#94a3b8;white-space:nowrap;">{ts}</span>'
        f'</div>'
        f'<div style="font-size:12.5px;color:#1e293b !important;-webkit-text-fill-color:#1e293b !important;margin-top:5px;">'
        f'{det} — <strong style="color:#0f172a !important;-webkit-text-fill-color:#0f172a !important;">{by}</strong>'
        f'</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )


# ─── DASHBOARD ────────────────────────────────────────────────────────────────
def page_dashboard():
    try:
        import plotly.graph_objects as go
        HAS_PLOTLY=True
    except ImportError:
        HAS_PLOTLY=False

    topbar("📊 Dashboard","Real-time overview of all purchase orders and supply chain status")
    D=st.session_state.D; df=D["orders"].copy()
    cf=st.session_state.co_filter
    fil=df if cf=="All" else df[df["company"]==cf]
    tv=fil["total_value"].astype(float).sum() if len(fil) else 0.0
    st.markdown('<div style="padding:0 24px;">',unsafe_allow_html=True)

    # KPI cards
    kpis=[("📦 TOTAL",len(fil),"#4f46e5"),("⏳ PENDING",len(fil[fil["current_status"]=="Pending"]),"#f59e0b"),
          ("🚚 TRANSIT",len(fil[fil["current_status"].isin(["Procured","Dispatched"])]),"#8b5cf6"),
          ("✅ DONE",len(fil[fil["current_status"].isin(["Delivered","Invoiced","Paid"])]),"#10b981"),
          ("💰 PAID",len(fil[fil["current_status"]=="Paid"]),"#06b6d4"),
          ("₹ VALUE",f"₹{tv/100000:.1f}L","#ef4444")]
    for col,(lbl,val,color) in zip(st.columns(6,gap="small"),kpis):
        with col:
            st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 14px 14px;box-shadow:0 1px 3px rgba(0,0,0,.04);border-top:3px solid {color};"><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#64748b;margin-bottom:8px;">{lbl}</div><div style="font-size:28px;font-weight:800;color:{color};line-height:1;">{val}</div></div>',unsafe_allow_html=True)
    sp(20)

    # Filter tabs
    fc1,fc2,fc3,fc4,_=st.columns([1.4,1.2,1.5,0.9,4],gap="small")
    for col,lbl,key in [(fc1,"🏢 All Companies","All"),(fc2,"Robokart","Robokart"),
                         (fc3,"Bharat Tech","Bharat Tech"),(fc4,"EL","EL")]:
        with col:
            if st.button(lbl+(" ✓" if cf==key else ""),key=f"cf_{key}",
                         type="primary" if cf==key else "secondary",use_container_width=True):
                st.session_state.co_filter=key; st.rerun()
    sp(20)

    # Charts — all text explicitly #111827
    if HAS_PLOTLY and len(fil)>0:
        ch1,ch2=st.columns([3,2],gap="medium")
        with ch1:
            cdf=df.groupby("company")["total_value"].apply(lambda x:x.astype(float).sum()).reset_index()
            cdf.columns=["Company","Value"]
            fig=go.Figure(go.Bar(
                x=cdf["Company"],y=cdf["Value"],
                marker_color=[CC.get(c,"#94a3b8") for c in cdf["Company"]],
                text=[f"₹{v/1e5:.1f}L" for v in cdf["Value"]],
                textposition="outside",
                textfont=dict(color="#111827",size=12,family="DM Sans"),
                marker_line_width=0,
            ))
            fig.update_layout(**chart_layout("Order Value by Company",
                yaxis=dict(showgrid=True,gridcolor="#f0f4f8",tickprefix="₹",tickformat=".2s",
                           tickfont=_BLK,linecolor="#cbd5e1",title_font=_BLK)))
            fig.update_traces(textfont_color="#111827")
            fig.update_xaxes(tickfont=_BLK, title_font=_BLK)
            fig.update_yaxes(tickfont=_BLK, title_font=_BLK)
            st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.04);">',unsafe_allow_html=True)
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>',unsafe_allow_html=True)
        with ch2:
            sc=fil["current_status"].value_counts().reset_index(); sc.columns=["Status","Count"]
            fig2=go.Figure(go.Pie(
                labels=sc["Status"],values=sc["Count"],hole=0.52,
                marker=dict(colors=[SC.get(s,"#94a3b8") for s in sc["Status"]]),
                textinfo="label+value",
                textfont=_BLK,
            ))
            fig2.update_layout(
                title=dict(text="Orders by Status",font=dict(size=13,color="#111827",family="DM Sans"),x=0),
                paper_bgcolor="white",font=_BLK,
                margin=dict(t=46,b=10,l=10,r=10),height=265,
                showlegend=True,legend=dict(font=_BLK),
            )
            st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.04);">',unsafe_allow_html=True)
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>',unsafe_allow_html=True)
        sp(20)

    # Table
    TH="padding:10px 14px;background:#f8fafc;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;white-space:nowrap;"
    TD="padding:12px 14px;border-bottom:1px solid #f1f5f9;color:#1e293b;vertical-align:middle;"
    tbody=""
    if len(fil)==0:
        tbody='<tr><td colspan="9" style="padding:32px;text-align:center;color:#94a3b8;">No orders found.</td></tr>'
    else:
        for i,(_,r) in enumerate(fil.iterrows()):
            bg="#fff" if i%2==0 else "#fafbfc"
            desc=str(r["item_description"]); desc=desc[:36]+"…" if len(desc)>36 else desc
            tbody+=f'<tr style="background:{bg}"><td style="{TD}font-weight:700;color:#4f46e5;font-size:11.5px;white-space:nowrap;">{r["order_id"]}</td><td style="{TD}">{cobadge(r["company"])}</td><td style="{TD}color:#64748b;font-size:11px;">{r["po_number"]}</td><td style="{TD}font-size:12px;">{r["govt_department"]}</td><td style="{TD}font-size:12px;">{desc}</td><td style="{TD}font-weight:700;white-space:nowrap;">₹{float(r["total_value"]):,.0f}</td><td style="{TD}">{pbadge(r["priority"])}</td><td style="{TD}">{sbadge(r["current_status"])}</td><td style="{TD}color:#94a3b8;font-size:11px;white-space:nowrap;">{r["last_updated"]}</td></tr>'
    label="All Orders" if cf=="All" else f"{cf} Orders"
    st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04);"><div style="display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-bottom:1px solid #f1f5f9;"><div style="font-size:14px;font-weight:700;color:#0f172a;">📦 {label}</div><div style="font-size:11px;font-weight:600;color:#64748b;background:#f1f5f9;padding:3px 12px;border-radius:20px;">{len(fil)} orders</div></div><div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr><th style="{TH}">Order ID</th><th style="{TH}">Company</th><th style="{TH}">PO#</th><th style="{TH}">Department</th><th style="{TH}">Description</th><th style="{TH}">Value</th><th style="{TH}">Priority</th><th style="{TH}">Status</th><th style="{TH}">Updated</th></tr></thead><tbody>{tbody}</tbody></table></div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True); sp(8); footer()


# ─── NEW ORDER ────────────────────────────────────────────────────────────────
def page_new_order():
    topbar("➕ New Order","Create a new government purchase order")
    D=st.session_state.D
    st.markdown('<div style="padding:0 24px;">',unsafe_allow_html=True)
    with st.form("no_form",clear_on_submit=True):
        section_label("Company & Classification")
        c1,c2=st.columns(2)
        with c1: company=st.selectbox("Company *",COMPANIES)
        with c2: priority=st.selectbox("Priority *",PRIORITIES,index=1)
        c3,c4=st.columns(2)
        with c3: govt_dept=st.text_input("Govt Department *",placeholder="e.g. Education Dept Delhi")
        with c4: po_num=st.text_input("PO Number *",placeholder="e.g. PO/EDU/2026/001")
        section_label("Contact Information")
        c5,c6=st.columns(2)
        with c5: contact_name=st.text_input("Contact Person *",placeholder="e.g. Mr. Rajesh Kumar")
        with c6: contact_ph=st.text_input("Contact Phone",placeholder="e.g. 9876543210")
        section_label("Order Details")
        c7,c8=st.columns(2)
        with c7:
            qty=st.number_input("Quantity *",min_value=1,value=1,step=1)
            val=st.number_input("Total Value (₹) *",min_value=0,value=0,step=1000)
        with c8:
            assigned=st.text_input("Assigned Company",placeholder="e.g. Tech Solutions Pvt Ltd")
            exp_del=st.date_input("Expected Delivery Date")
        item_desc=st.text_area("Item Description *",placeholder="Detailed description…",height=90)
        remarks=st.text_area("Remarks",placeholder="Additional notes…",height=60)
        sp(6); sc,_=st.columns([1,2])
        with sc: submitted=st.form_submit_button("🚀 Create Purchase Order",type="primary",use_container_width=True)
    if submitted:
        errs=[f for f,v in [("Dept",govt_dept),("PO#",po_num),("Contact",contact_name),("Description",item_desc),("Value",val)] if not v]
        if errs: st.error(f"Missing: {', '.join(errs)}")
        elif po_num in D["orders"]["po_number"].values: st.error("⚠️ PO Number already exists.")
        else:
            ts=now_ist(); oid=f"ORD-{ts[:10]}-{str(len(D['orders'])+1).zfill(3)}"
            D["orders"]=pd.concat([D["orders"],pd.DataFrame([{"order_id":oid,"date_created":ts,"company":company,"govt_department":govt_dept,"contact_person":contact_name,"contact_phone":contact_ph,"po_number":po_num,"item_description":item_desc,"quantity":str(qty),"total_value":str(val),"assigned_company":assigned,"current_status":"Pending","priority":priority,"expected_delivery_date":str(exp_del),"remarks":remarks,"created_by":st.session_state.user_name,"last_updated":ts}])],ignore_index=True)
            save("orders"); log_action(oid,"ORDER_CREATED","—","Pending",st.session_state.user_name,f"Order created — {company} | {po_num}")
            st.success(f"✅ Order **{oid}** created!")
    st.markdown('</div>',unsafe_allow_html=True); footer()


# ─── UPDATE ORDER ─────────────────────────────────────────────────────────────
def page_update_order():
    topbar("🔄 Update Order","Update procurement, dispatch, delivery or invoice status")
    D=st.session_state.D
    st.markdown('<div style="padding:0 24px;">',unsafe_allow_html=True)
    opts=(["— Select an order —"]+[f"{r['order_id']}  ·  {r['po_number']}  ·  [{r['current_status']}]" for _,r in D["orders"].iterrows()])
    sel=st.selectbox("Select Order to Update",opts,key="uo_sel")
    if sel=="— Select an order —": st.info("👆 Select an order above."); st.markdown('</div>',unsafe_allow_html=True); footer(); return
    oid=sel.split("  ·  ")[0].strip(); order=get_order(oid)
    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;margin:10px 0 16px;"><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:3px;">Order ID</div><div style="font-size:12.5px;font-weight:700;color:#4f46e5;">{order["order_id"]}</div></div><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:3px;">Company</div>{cobadge(order["company"])}</div><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:3px;">Status</div>{sbadge(order["current_status"])}</div><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:3px;">Priority</div>{pbadge(order["priority"])}</div><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:3px;">Value</div><div style="font-size:14px;font-weight:800;color:#0f172a;">₹{float(order["total_value"]):,.0f}</div></div></div>',unsafe_allow_html=True)
    updated_by=st.text_input("Your Name / Department *",placeholder="e.g. Rahul — Logistics",key="uo_by"); sp(4)
    t1,t2,t3,t4=st.tabs(["🔧  Procurement","🚚  Dispatch","📦  Delivery","💰  Invoice & Payment"])
    with t1:
        with st.form("pf"):
            c1,c2=st.columns(2)
            with c1: p_stat=st.selectbox("Status",["","Not Started","In Progress","Completed","On Hold"]); p_date=st.date_input("Date",key="pd")
            with c2: p_qc=st.selectbox("Quality Check",["","Pending","In Progress","Passed","Failed"]); p_src=st.text_input("Materials Source")
            p_notes=st.text_area("Notes",height=70,key="pn")
            if st.form_submit_button("✅ Save Procurement",type="primary"):
                if not updated_by: st.error("Enter your name above first.")
                else:
                    ts=now_ist(); D["procurement"]=pd.concat([D["procurement"],pd.DataFrame([{"id":str(len(D["procurement"])+1),"order_id":oid,"procurement_status":p_stat,"procurement_date":str(p_date),"materials_source":p_src,"quality_check_status":p_qc,"notes":p_notes,"updated_by":updated_by,"updated_at":ts}])],ignore_index=True); save("procurement")
                    ns="Procured" if p_stat=="Completed" else order["current_status"]; prev=order["current_status"]; set_status(oid,ns); log_action(oid,"STATUS_CHANGE",prev,ns,updated_by,f"Procurement: {p_stat}"); st.success(f"✅ → **{ns}**"); st.rerun()
    with t2:
        with st.form("df"):
            c1,c2=st.columns(2)
            with c1: d_date=st.date_input("Dispatch Date",key="dd"); d_cour=st.text_input("Courier *"); d_veh=st.text_input("Vehicle No.")
            with c2: d_drv=st.text_input("Driver Contact"); d_trk=st.text_input("Tracking No."); d_exp=st.date_input("Exp Delivery",key="de")
            if st.form_submit_button("✅ Save Dispatch",type="primary"):
                if not updated_by: st.error("Enter your name above first.")
                else:
                    ts=now_ist(); D["dispatch"]=pd.concat([D["dispatch"],pd.DataFrame([{"id":str(len(D["dispatch"])+1),"order_id":oid,"dispatch_date":str(d_date),"courier_name":d_cour,"vehicle_number":d_veh,"driver_contact":d_drv,"tracking_number":d_trk,"expected_delivery_date":str(d_exp),"updated_by":updated_by,"updated_at":ts}])],ignore_index=True); save("dispatch")
                    prev=order["current_status"]; set_status(oid,"Dispatched"); log_action(oid,"STATUS_CHANGE",prev,"Dispatched",updated_by,f"Dispatched via {d_cour}"); st.success("✅ → **Dispatched**"); st.rerun()
    with t3:
        with st.form("dlf"):
            c1,c2=st.columns(2)
            with c1: de_stat=st.selectbox("Status",["","Delivered","Partial","Failed","Rescheduled"]); de_date=st.date_input("Delivery Date",key="dld"); de_recv=st.text_input("Receiver Name")
            with c2: de_qty=st.number_input("Delivered Qty",min_value=0,step=1); de_ch=st.text_input("Challan Number")
            del_f=st.file_uploader("Delivery Files",accept_multiple_files=True,key="df2"); ch_f=st.file_uploader("Challan Docs",accept_multiple_files=True,key="cf2")
            if st.form_submit_button("✅ Save Delivery",type="primary"):
                if not updated_by: st.error("Enter your name above first.")
                else:
                    ts=now_ist(); D["delivery"]=pd.concat([D["delivery"],pd.DataFrame([{"id":str(len(D["delivery"])+1),"order_id":oid,"delivery_status":de_stat,"delivery_date":str(de_date),"receiver_name":de_recv,"delivered_quantity":str(de_qty),"challan_number":de_ch,"delivery_files":f"{len(del_f or [])} file(s)","challan_files":f"{len(ch_f or [])} file(s)","updated_by":updated_by,"updated_at":ts}])],ignore_index=True); save("delivery")
                    ns="Delivered" if de_stat=="Delivered" else order["current_status"]; prev=order["current_status"]; set_status(oid,ns); log_action(oid,"STATUS_CHANGE",prev,ns,updated_by,f"Delivery: {de_stat}"); st.success(f"✅ → **{ns}**"); st.rerun()
    with t4:
        with st.form("invf"):
            c1,c2=st.columns(2)
            with c1: i_num=st.text_input("Invoice Number"); i_date=st.date_input("Invoice Date",key="id2"); i_amt=st.number_input("Amount (₹)",min_value=0,step=1000); i_pstat=st.selectbox("Payment Status",["","Pending","Approved","Completed"])
            with c2: i_pmode=st.selectbox("Payment Mode",["","NEFT","RTGS","Cheque","DD","Online","Cash"]); i_txn=st.text_input("Transaction Ref"); i_pdate=st.date_input("Payment Date",key="ipd")
            inv_f=st.file_uploader("Invoice Docs",accept_multiple_files=True,key="ivf")
            if st.form_submit_button("✅ Save Invoice & Payment",type="primary"):
                if not updated_by: st.error("Enter your name above first.")
                else:
                    ts=now_ist(); D["invoices"]=pd.concat([D["invoices"],pd.DataFrame([{"id":str(len(D["invoices"])+1),"order_id":oid,"invoice_number":i_num,"invoice_date":str(i_date),"invoice_amount":str(i_amt),"payment_status":i_pstat,"payment_date":str(i_pdate),"payment_mode":i_pmode,"transaction_reference":i_txn,"invoice_files":f"{len(inv_f or [])} file(s)","updated_by":updated_by,"updated_at":ts}])],ignore_index=True); save("invoices")
                    ns="Paid" if i_pstat=="Completed" else "Invoiced"; prev=order["current_status"]; set_status(oid,ns); log_action(oid,"STATUS_CHANGE",prev,ns,updated_by,f"Invoice {i_num} | {i_pstat}"); st.success(f"✅ → **{ns}**"); st.rerun()
    st.markdown('</div>',unsafe_allow_html=True); footer()


# ─── ORDER DETAILS ────────────────────────────────────────────────────────────
def page_order_details():
    topbar("🔍 Order Details","Full order info, timeline and activity")
    D=st.session_state.D
    st.markdown('<div style="padding:0 24px;">',unsafe_allow_html=True)
    opts=(["— Select an order —"]+[f"{r['order_id']}  ·  {r['po_number']}  ·  {r['current_status']}" for _,r in D["orders"].iterrows()])
    sel=st.selectbox("Select Order",opts,key="od_sel")
    if sel=="— Select an order —": st.info("👆 Select an order to view details."); st.markdown('</div>',unsafe_allow_html=True); footer(); return
    oid=sel.split("  ·  ")[0].strip(); order=get_order(oid); s=order["current_status"]
    st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:20px 22px;box-shadow:0 1px 3px rgba(0,0,0,.04);margin-bottom:16px;"><div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;"><div><div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">{cobadge(order["company"])}<span style="font-size:17px;font-weight:800;color:#0f172a;">{order["order_id"]}</span></div><div style="font-size:12.5px;color:#64748b;">{order["po_number"]} · {order["govt_department"]}</div></div><div style="display:flex;gap:8px;">{sbadge(s)}{pbadge(order["priority"])}</div></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin-top:16px;padding-top:14px;border-top:1px solid #f1f5f9;"><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;">Contact</div><div style="font-size:12.5px;font-weight:600;color:#0f172a;">{order["contact_person"]}</div></div><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;">Phone</div><div style="font-size:12.5px;font-weight:600;color:#0f172a;">{order["contact_phone"]}</div></div><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;">Quantity</div><div style="font-size:12.5px;font-weight:600;color:#0f172a;">{order["quantity"]}</div></div><div><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;">Value</div><div style="font-size:17px;font-weight:800;color:#0f172a;">₹{float(order["total_value"]):,.0f}</div></div></div><div style="margin-top:12px;background:#f8fafc;border-radius:7px;border:1px solid #e2e8f0;padding:10px 14px;"><span style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;">Description: </span><span style="font-size:12.5px;color:#1e293b;">{order["item_description"]}</span></div></div>',unsafe_allow_html=True)
    # Timeline
    cur_idx=STATUSES.index(s) if s in STATUSES else 0
    html='<div style="display:flex;align-items:center;margin-bottom:20px;">'
    for i,step in enumerate(STATUSES):
        if i<cur_idx:    cc,lc=f"{SC.get(step,'#4f46e5')};color:#fff",SC.get(step,"#4f46e5")
        elif i==cur_idx: cc,lc="white;border:2px solid #6366f1;color:#4f46e5","#4f46e5"
        else:            cc,lc="#f1f5f9;color:#94a3b8","#94a3b8"
        html+=f'<div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;"><div style="width:32px;height:32px;border-radius:50%;background:{cc};display:flex;align-items:center;justify-content:center;font-size:13px;">{SE.get(step,"")}</div><div style="font-size:9px;font-weight:600;color:{lc};margin-top:4px;text-align:center;">{step}</div></div>'
        if i<len(STATUSES)-1: html+=f'<div style="flex:1;height:2px;background:{"#6366f1" if i<cur_idx else "#e2e8f0"};margin:0 3px 16px;"></div>'
    st.markdown(html+"</div>",unsafe_allow_html=True)
    def show_rec(tbl):
        rows=D[tbl][D[tbl]["order_id"]==oid]
        if len(rows)==0: st.info("No data recorded yet."); return
        row=rows.iloc[-1]; items=[(c.replace("_"," ").title(),str(row[c])) for c in row.index if c not in ["id","order_id"] and str(row[c]) not in ["","nan"]]
        for i in range(0,len(items),3):
            for col,(lbl,v) in zip(st.columns(3),items[i:i+3]):
                with col: st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px 12px;margin-bottom:8px;"><div style="font-size:9.5px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:3px;">{lbl}</div><div style="font-size:12.5px;font-weight:600;color:#0f172a;">{v}</div></div>',unsafe_allow_html=True)
    t1,t2,t3,t4,t5=st.tabs(["🔧 Procurement","🚚 Dispatch","📦 Delivery","💰 Invoice","📋 Activity"])
    with t1: show_rec("procurement")
    with t2: show_rec("dispatch")
    with t3: show_rec("delivery")
    with t4: show_rec("invoices")
    with t5:
        logs=D["activity_log"][D["activity_log"]["order_id"]==oid].copy().iloc[::-1]
        if len(logs)==0: st.info("No activity yet.")
        else:
            for _,log in logs.iterrows(): _log_row(log)
    st.markdown('</div>',unsafe_allow_html=True); footer()


# ─── ACTIVITY LOG ─────────────────────────────────────────────────────────────
def page_activity_log():
    topbar("📋 Activity Log","Complete audit trail of all order changes and updates")
    D=st.session_state.D; logs=D["activity_log"].copy().iloc[::-1].reset_index(drop=True)
    st.markdown('<div style="padding:0 24px;">',unsafe_allow_html=True)
    st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04);"><div style="display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-bottom:1px solid #f1f5f9;background:#fafbfc;"><div style="font-size:14px;font-weight:700;color:#0f172a;">📋 All System Events</div><div style="font-size:11px;font-weight:600;color:#64748b;background:#f1f5f9;padding:3px 12px;border-radius:20px;">{len(logs)} events</div></div><div style="padding:14px;">',unsafe_allow_html=True)
    if len(logs)==0: st.info("No activity recorded yet.")
    else:
        for _,log in logs.iterrows(): _log_row(log)
    st.markdown('</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True); footer()


# ─── REPORTS ──────────────────────────────────────────────────────────────────
def page_reports():
    topbar("📈 Reports","Financial summaries and order analytics")
    try:
        import plotly.graph_objects as go
        HAS_PLOTLY=True
    except ImportError:
        HAS_PLOTLY=False
    D=st.session_state.D; df=D["orders"].copy(); df["total_value"]=df["total_value"].astype(float)
    st.markdown('<div style="padding:0 24px;">',unsafe_allow_html=True)
    if HAS_PLOTLY:
        c1,c2,c3=st.columns(3,gap="medium")
        with c1:
            cdf=df.groupby("company")["total_value"].sum().reset_index()
            fig=go.Figure(go.Bar(x=cdf["company"],y=cdf["total_value"],
                marker_color=[CC.get(c,"#94a3b8") for c in cdf["company"]],
                text=[f"₹{v/1e5:.1f}L" for v in cdf["total_value"]],
                textposition="outside",textfont=dict(color="#111827",size=11),marker_line_width=0))
            fig.update_layout(**chart_layout("Value by Company",
                yaxis=dict(showgrid=True,gridcolor="#f0f4f8",tickprefix="₹",tickformat=".2s",tickfont=_BLK)))
            fig.update_traces(textfont_color="#111827")
            fig.update_xaxes(tickfont=_BLK); fig.update_yaxes(tickfont=_BLK)
            st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,.04);">',unsafe_allow_html=True)
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>',unsafe_allow_html=True)
        with c2:
            sc2=df["current_status"].value_counts().reset_index(); sc2.columns=["Status","Count"]
            fig2=go.Figure(go.Bar(x=sc2["Status"],y=sc2["Count"],
                marker_color=[SC.get(s,"#94a3b8") for s in sc2["Status"]],
                text=sc2["Count"],textposition="outside",textfont=dict(color="#111827",size=11),marker_line_width=0))
            fig2.update_layout(**chart_layout("Orders by Status",
                margin=dict(t=46,b=60,l=40,r=16),
                xaxis=dict(showgrid=False,tickangle=-20,tickfont=_BLK)))
            fig2.update_traces(textfont_color="#111827")
            fig2.update_xaxes(tickfont=_BLK); fig2.update_yaxes(tickfont=_BLK)
            st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,.04);">',unsafe_allow_html=True)
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>',unsafe_allow_html=True)
        with c3:
            pc=df["priority"].value_counts().reset_index(); pc.columns=["Priority","Count"]
            fig3=go.Figure(go.Pie(labels=pc["Priority"],values=pc["Count"],hole=0.5,
                marker=dict(colors=[PF.get(p,"#94a3b8") for p in pc["Priority"]]),
                textinfo="label+percent",textfont=_BLK))
            fig3.update_layout(
                title=dict(text="Priority Mix",font=dict(size=13,color="#111827",family="DM Sans"),x=0),
                paper_bgcolor="white",font=_BLK,margin=dict(t=46,b=10,l=10,r=10),height=265,
                showlegend=True,legend=dict(font=_BLK,bgcolor="white",bordercolor="#e2e8f0"))
            fig3.update_traces(textfont=_BLK, insidetextfont=_BLK, outsidetextfont=_BLK)
            st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,.04);">',unsafe_allow_html=True)
            st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>',unsafe_allow_html=True)
        sp(20)
    TH="padding:10px 14px;background:#f8fafc;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;"
    TD="padding:11px 14px;border-bottom:1px solid #f1f5f9;font-size:12.5px;color:#1e293b;"
    rows=""; outstanding=0.0
    for i,(_,r) in enumerate(df.iterrows()):
        bg="#fff" if i%2==0 else "#fafbfc"; tv=float(r["total_value"])
        paid=f'<span style="color:#15803d;font-weight:700;">₹{tv:,.0f}</span>' if r["current_status"]=="Paid" else '<span style="color:#94a3b8;">—</span>'
        out='<span style="color:#94a3b8;">—</span>' if r["current_status"]=="Paid" else f'<span style="color:#ef4444;font-weight:700;">₹{tv:,.0f}</span>'
        if r["current_status"]!="Paid": outstanding+=tv
        rows+=f'<tr style="background:{bg}"><td style="{TD}color:#64748b;font-size:11px;">{r["order_id"]}</td><td style="{TD}">{cobadge(r["company"])}</td><td style="{TD}">{r["govt_department"]}</td><td style="{TD}font-weight:700;">₹{tv:,.0f}</td><td style="{TD}">{sbadge(r["current_status"])}</td><td style="{TD}">{paid}</td><td style="{TD}">{out}</td></tr>'
    st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04);margin-bottom:18px;"><div style="padding:12px 18px;border-bottom:1px solid #f1f5f9;background:#fafbfc;"><div style="font-size:14px;font-weight:700;color:#0f172a;">💵 Financial Summary</div></div><div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr><th style="{TH}">Order ID</th><th style="{TH}">Company</th><th style="{TH}">Department</th><th style="{TH}">Value</th><th style="{TH}">Status</th><th style="{TH}">Paid</th><th style="{TH}">Outstanding</th></tr></thead><tbody>{rows}</tbody></table></div><div style="padding:10px 18px;background:#f8fafc;border-top:1px solid #e2e8f0;display:flex;justify-content:space-between;font-size:13px;font-weight:700;"><span style="color:#64748b;">Total Outstanding</span><span style="color:#ef4444;">₹{outstanding:,.0f}</span></div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True); footer()


# ─── ADMIN PANEL ──────────────────────────────────────────────────────────────
def page_admin():
    topbar("⚙️ Admin Panel","Data export, statistics and user management")
    D=st.session_state.D
    st.markdown('<div style="padding:0 24px;">',unsafe_allow_html=True)
    st.info("✅ **Auto-Save** is on — all data persists automatically.")
    tables=["orders","procurement","dispatch","delivery","invoices","activity_log"]
    # Section headings rendered via st.markdown with explicit dark color
    st.markdown('<p style="font-size:16px;font-weight:700;color:#0f172a;margin:18px 0 10px;">📥 Export Data as CSV</p>',unsafe_allow_html=True)
    cols=st.columns(3)
    for i,t in enumerate(tables):
        with cols[i%3]: st.download_button(f"📄 {t} ({len(D[t])} rows)",D[t].to_csv(index=False).encode("utf-8"),f"sc_{t}_{now_ist()[:10]}.csv","text/csv",use_container_width=True,key=f"dl_{t}")
    sp(6)
    st.download_button("📦 Export ALL Tables (Combined)","\n\n".join([f"=== {t.upper()} ===\n"+D[t].to_csv(index=False) for t in tables]).encode("utf-8"),f"sc_full_{now_ist()[:10]}.csv","text/csv",use_container_width=True,key="dl_all",type="primary")
    sp(16)
    st.markdown('<p style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:10px;">⚙️ Database Statistics</p>',unsafe_allow_html=True)
    stat_cells="".join([f'<div style="background:#fff;border:1px solid #e2e8f0;border-top:3px solid #6366f1;border-radius:10px;padding:12px;text-align:center;"><div style="font-size:9.5px;font-weight:700;color:#64748b;text-transform:uppercase;">{t}</div><div style="font-size:22px;font-weight:800;color:#4f46e5;margin-top:5px;">{len(D[t])}</div><div style="font-size:9.5px;color:#94a3b8;">rows</div></div>' for t in tables])
    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:20px;">{stat_cells}</div>',unsafe_allow_html=True)
    sp(4)
    st.markdown('<p style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:10px;">👥 User Accounts</p>',unsafe_allow_html=True)
    RDESC={"Admin":"Full access — all 7 pages","Manager":"No admin panel","Staff":"Update orders only","Viewer":"Read-only"}
    for u,v in USERS.items():
        rc=RC.get(v["role"],"#64748b"); rb=RB.get(v["role"],"#f1f5f9")
        st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 16px;margin-bottom:8px;display:flex;align-items:center;gap:14px;"><div style="width:36px;height:36px;border-radius:8px;background:{rc};color:#fff;font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{u[0]}</div><div style="flex:1;"><div style="display:flex;align-items:center;gap:8px;margin-bottom:2px;"><span style="font-size:13px;font-weight:700;color:#0f172a;">{u}</span><span style="font-size:10px;font-weight:700;background:{rb};color:{rc};padding:1px 8px;border-radius:4px;">{v["role"]}</span></div><div style="font-size:12px;color:#64748b;">{RDESC.get(v["role"],"")}</div></div></div>',unsafe_allow_html=True)
    sp(10)
    # Danger zone — explicit HTML instead of expander so text is always visible
    st.markdown('<p style="font-size:14px;font-weight:700;color:#ef4444;margin-bottom:8px;">⚠️ Danger Zone</p>',unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;color:#1e293b;margin-bottom:10px;">Reset all data back to the 4 original sample orders. This permanently deletes everything entered. Cannot be undone.</p>',unsafe_allow_html=True)
    confirm = st.checkbox("I understand this will delete all data permanently", key="confirm_reset")
    if confirm:
        if st.button("🗑️  Reset to Sample Data", type="primary", key="reset_btn"):
            seed=make_seed()
            for k,d in seed.items(): d.to_csv(FILES[k],index=False)
            st.session_state.D=load_data(); st.success("✅ Data reset to sample."); st.rerun()
    st.markdown('</div>',unsafe_allow_html=True); footer()


# ─── MANAGE RECORDS (Admin only) ─────────────────────────────────────────────
def page_manage_records():
    topbar("🗂️ Manage Records","Edit or delete any order — Admin only · All changes are auto-saved")
    D = st.session_state.D

    # Guard — should never reach here for non-admin but double-check
    if st.session_state.role != "Admin":
        st.error("⛔ Access denied. Admin only."); return

    st.markdown('<div style="padding:0 24px;">', unsafe_allow_html=True)

    orders = D["orders"].copy()
    if len(orders) == 0:
        st.info("No orders found."); st.markdown('</div>', unsafe_allow_html=True); footer(); return

    # ── which order is being edited right now ──────────────────────────────────
    if "mr_edit_id" not in st.session_state: st.session_state.mr_edit_id = None
    if "mr_del_id"  not in st.session_state: st.session_state.mr_del_id  = None

    # ── DELETE CONFIRMATION MODAL ──────────────────────────────────────────────
    if st.session_state.mr_del_id:
        del_oid = st.session_state.mr_del_id
        del_order = get_order(del_oid)
        st.markdown(f"""
        <div style="background:#fff5f5;border:1.5px solid #fca5a5;border-radius:12px;
             padding:18px 22px;margin-bottom:20px;">
          <div style="font-size:14px;font-weight:800;color:#dc2626;margin-bottom:6px;">
            ⚠️ Confirm Delete — {del_oid}</div>
          <div style="font-size:13px;color:#1e293b;margin-bottom:14px;">
            This will permanently delete order <strong>{del_oid}</strong>
            ({del_order['po_number'] if del_order is not None else ''}) and ALL related
            procurement, dispatch, delivery, invoice and activity records.
            <strong>This cannot be undone.</strong>
          </div>
        </div>""", unsafe_allow_html=True)
        ca, cb, _ = st.columns([1, 1, 4])
        with ca:
            if st.button("🗑️  Yes, Delete", type="primary", key="del_confirm_yes",
                         use_container_width=True):
                oid = st.session_state.mr_del_id
                # Delete from all tables
                for tbl in ["orders","procurement","dispatch","delivery","invoices"]:
                    D[tbl] = D[tbl][D[tbl]["order_id"] != oid].reset_index(drop=True); save(tbl)
                # Log the deletion
                log_action(oid, "ORDER_DELETED", "—", "—",
                           st.session_state.user_name, f"Order deleted by Admin")
                st.session_state.mr_del_id = None
                st.success(f"✅ Order {oid} and all related records deleted.")
                st.rerun()
        with cb:
            if st.button("Cancel", key="del_confirm_no", use_container_width=True):
                st.session_state.mr_del_id = None; st.rerun()

    # ── EDIT FORM ──────────────────────────────────────────────────────────────
    if st.session_state.mr_edit_id:
        edit_oid = st.session_state.mr_edit_id
        eo = get_order(edit_oid)
        if eo is None:
            st.session_state.mr_edit_id = None; st.rerun()

        st.markdown(f"""
        <div style="background:#f0f9ff;border:1.5px solid #bae6fd;border-radius:12px;
             padding:16px 22px 8px;margin-bottom:16px;">
          <div style="font-size:14px;font-weight:800;color:#0369a1;">
            ✏️ Editing — {edit_oid} &nbsp;·&nbsp;
            <span style="font-weight:500;font-size:12.5px;">{eo['po_number']}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        with st.form("edit_order_form"):
            section_label("Company & Classification")
            c1, c2 = st.columns(2)
            with c1:
                co_idx = COMPANIES.index(eo["company"]) if eo["company"] in COMPANIES else 0
                e_company = st.selectbox("Company *", COMPANIES, index=co_idx, key="ef_co")
            with c2:
                pr_idx = PRIORITIES.index(eo["priority"]) if eo["priority"] in PRIORITIES else 1
                e_priority = st.selectbox("Priority *", PRIORITIES, index=pr_idx, key="ef_pr")

            c3, c4 = st.columns(2)
            with c3: e_dept    = st.text_input("Govt Department *", value=eo["govt_department"],    key="ef_dept")
            with c4: e_po      = st.text_input("PO Number *",        value=eo["po_number"],          key="ef_po")

            section_label("Contact Information")
            c5, c6 = st.columns(2)
            with c5: e_contact = st.text_input("Contact Person *",   value=eo["contact_person"],    key="ef_cp")
            with c6: e_phone   = st.text_input("Contact Phone",      value=eo["contact_phone"],     key="ef_ph")

            section_label("Order Details")
            c7, c8 = st.columns(2)
            with c7:
                e_qty  = st.number_input("Quantity *", min_value=1,
                                          value=max(1, int(eo["quantity"]) if str(eo["quantity"]).isdigit() else 1),
                                          step=1, key="ef_qty")
                e_val  = st.number_input("Total Value (₹) *", min_value=0,
                                          value=int(float(eo["total_value"])) if eo["total_value"] else 0,
                                          step=1000, key="ef_val")
            with c8:
                e_assigned = st.text_input("Assigned Company", value=eo["assigned_company"], key="ef_asgn")
                st_idx = STATUSES.index(eo["current_status"]) if eo["current_status"] in STATUSES else 0
                e_status   = st.selectbox("Current Status", STATUSES, index=st_idx, key="ef_st")

            e_desc    = st.text_area("Item Description *", value=eo["item_description"], height=80, key="ef_desc")
            e_remarks = st.text_area("Remarks",             value=eo["remarks"],          height=55, key="ef_rem")

            sp(6)
            s1, s2, _ = st.columns([1, 1, 3])
            with s1: save_btn   = st.form_submit_button("💾  Save Changes", type="primary",    use_container_width=True)
            with s2: cancel_btn = st.form_submit_button("✕  Cancel",        type="secondary",  use_container_width=True)

        if cancel_btn:
            st.session_state.mr_edit_id = None; st.rerun()

        if save_btn:
            errs = [f for f, v in [("Dept", e_dept), ("PO#", e_po), ("Contact", e_contact),
                                    ("Description", e_desc), ("Value", e_val)] if not v]
            # Check PO uniqueness (allow same PO as this order)
            others = D["orders"][D["orders"]["order_id"] != edit_oid]
            if errs:
                st.error(f"Missing required fields: {', '.join(errs)}")
            elif e_po in others["po_number"].values:
                st.error("⚠️ PO Number already used by another order.")
            else:
                prev_status = eo["current_status"]
                idx = D["orders"][D["orders"]["order_id"] == edit_oid].index[0]
                D["orders"].at[idx, "company"]          = e_company
                D["orders"].at[idx, "priority"]         = e_priority
                D["orders"].at[idx, "govt_department"]  = e_dept
                D["orders"].at[idx, "po_number"]        = e_po
                D["orders"].at[idx, "contact_person"]   = e_contact
                D["orders"].at[idx, "contact_phone"]    = e_phone
                D["orders"].at[idx, "quantity"]         = str(e_qty)
                D["orders"].at[idx, "total_value"]      = str(e_val)
                D["orders"].at[idx, "assigned_company"] = e_assigned
                D["orders"].at[idx, "current_status"]   = e_status
                D["orders"].at[idx, "item_description"] = e_desc
                D["orders"].at[idx, "remarks"]          = e_remarks
                D["orders"].at[idx, "last_updated"]     = now_ist()
                save("orders")
                change_note = f"Admin edited order"
                if prev_status != e_status:
                    change_note += f" · status {prev_status} → {e_status}"
                log_action(edit_oid, "ORDER_EDITED", prev_status, e_status,
                           st.session_state.user_name, change_note)
                st.session_state.mr_edit_id = None
                st.success(f"✅ Order {edit_oid} updated successfully.")
                st.rerun()

    # ── ORDERS TABLE WITH EDIT/DELETE BUTTONS ─────────────────────────────────
    TH = "padding:10px 14px;background:#f8fafc;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#475569;border-bottom:2px solid #e2e8f0;text-align:left;white-space:nowrap;"
    TD = "padding:11px 14px;border-bottom:1px solid #f1f5f9;color:#1e293b;vertical-align:middle;font-size:12.5px;"

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;
         box-shadow:0 1px 3px rgba(0,0,0,.04);">
      <div style="display:flex;justify-content:space-between;align-items:center;
           padding:14px 18px;border-bottom:1px solid #f1f5f9;">
        <div style="font-size:14px;font-weight:700;color:#0f172a;">🗂️ All Orders — Edit / Delete</div>
        <div style="font-size:11px;font-weight:600;color:#64748b;background:#f1f5f9;
             padding:3px 12px;border-radius:20px;">{len(orders)} orders</div>
      </div>
    </div>""", unsafe_allow_html=True)
    sp(4)

    # Render each order as a row with inline Edit + Delete buttons
    for _, r in orders.iterrows():
        oid = r["order_id"]
        is_editing = (st.session_state.mr_edit_id == oid)
        row_bg = "#eef2ff" if is_editing else "#fff"
        left_border = "border-left:3px solid #6366f1;" if is_editing else "border-left:3px solid transparent;"

        row_col, btn_col = st.columns([9, 1.4])
        with row_col:
            desc = str(r["item_description"]); desc = desc[:40]+"…" if len(desc)>40 else desc
            st.markdown(f"""
            <div style="background:{row_bg};border:1px solid #e2e8f0;{left_border}
                 border-radius:10px;padding:12px 16px;display:grid;
                 grid-template-columns:1.8fr 1fr 1fr 1fr 0.8fr 1fr 1fr;
                 gap:10px;align-items:center;">
              <div>
                <div style="font-size:11px;font-weight:700;color:#4f46e5;">{oid}</div>
                <div style="font-size:11.5px;color:#1e293b;margin-top:2px;">{desc}</div>
              </div>
              <div>{cobadge(r['company'])}</div>
              <div style="font-size:11.5px;color:#64748b;">{r['po_number']}</div>
              <div style="font-size:11.5px;color:#1e293b;">{r['govt_department'][:22]}{'…' if len(r['govt_department'])>22 else ''}</div>
              <div>{sbadge(r['current_status'])}</div>
              <div>{pbadge(r['priority'])}</div>
              <div style="font-size:11.5px;font-weight:700;color:#0f172a;">₹{float(r['total_value']):,.0f}</div>
            </div>""", unsafe_allow_html=True)

        with btn_col:
            sp(4)
            b1, b2 = st.columns(2)
            with b1:
                if st.button("✏️", key=f"edit_{oid}", help=f"Edit {oid}",
                             type="primary" if is_editing else "secondary",
                             use_container_width=True):
                    st.session_state.mr_edit_id = None if is_editing else oid
                    st.session_state.mr_del_id  = None
                    st.rerun()
            with b2:
                if st.button("🗑️", key=f"del_{oid}", help=f"Delete {oid}",
                             use_container_width=True):
                    st.session_state.mr_del_id  = oid
                    st.session_state.mr_edit_id = None
                    st.rerun()
        sp(4)

    st.markdown('<p style="font-size:11.5px;color:#94a3b8;margin-top:12px;">💡 Click ✏️ to edit an order inline · Click 🗑️ to delete with confirmation</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()


# ─── ROUTER ───────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        login_page()
        return
    render_sidebar()
    allowed=MENUS.get(st.session_state.role,[])
    if st.session_state.page not in allowed: st.session_state.page="Dashboard"
    p=st.session_state.page
    if   p=="Dashboard":      page_dashboard()
    elif p=="New Order":      page_new_order()
    elif p=="Update Order":   page_update_order()
    elif p=="Order Details":  page_order_details()
    elif p=="Activity Log":   page_activity_log()
    elif p=="Reports":        page_reports()
    elif p=="Manage Records": page_manage_records()
    elif p=="Admin Panel":    page_admin()

main()
