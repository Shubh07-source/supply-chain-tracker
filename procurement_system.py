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
    /* Hide default streamlit elements */
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    .block-container {padding-top:1.5rem; padding-bottom:1rem;}

    /* Metric cards */
    [data-testid="metric-container"] {
        background:#fff;
        border:1px solid #e2e8f0;
        border-radius:10px;
        padding:12px 16px;
        box-shadow:0 1px 3px rgba(0,0,0,0.06);
    }

    /* Buttons */
    .stButton>button {
        border-radius:7px;
        font-weight:600;
        transition:all 0.15s;
    }
    .stButton>button:hover {opacity:0.88;}

    /* Table */
    .stDataFrame {border-radius:8px; overflow:hidden;}

    /* Sidebar */
    [data-testid="stSidebar"] {background:#0c1426;}
    [data-testid="stSidebar"] * {color:#94a3b8 !important;}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {color:#f97316 !important;}

    /* Status badges */
    .badge {
        display:inline-block;
        padding:2px 10px;
        border-radius:999px;
        font-size:12px;
        font-weight:600;
    }

    /* Info boxes */
    .info-box {
        background:#f8fafc;
        border:1px solid #e2e8f0;
        border-radius:8px;
        padding:12px 16px;
        margin-bottom:12px;
    }

    /* Footer */
    .footer {
        text-align:center;
        font-size:11px;
        color:#94a3b8;
        padding:8px;
        border-top:1px solid #e2e8f0;
        margin-top:2rem;
    }
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
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🏭 Supply Chain Tracking System")
        st.markdown("---")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
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
        st.caption("Contact your administrator for login credentials.")

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

def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

# ─── PAGES ────────────────────────────────────────────────────────────────────

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown("## 📊 Dashboard")

    orders = data["orders"].copy()

    # Company filter
    st.markdown("**Filter by Company:**")
    col_all, col_rk, col_bt, col_el, _ = st.columns([1,1,1,1,3])
    with col_all:
        if st.button("🏢 All", use_container_width=True,
                     type="primary" if st.session_state.get("cf","All")=="All" else "secondary"):
            st.session_state.cf = "All"; st.rerun()
    with col_rk:
        if st.button("Robokart", use_container_width=True,
                     type="primary" if st.session_state.get("cf")=="Robokart" else "secondary"):
            st.session_state.cf = "Robokart"; st.rerun()
    with col_bt:
        if st.button("Bharat Tech", use_container_width=True,
                     type="primary" if st.session_state.get("cf")=="Bharat Tech" else "secondary"):
            st.session_state.cf = "Bharat Tech"; st.rerun()
    with col_el:
        if st.button("EL", use_container_width=True,
                     type="primary" if st.session_state.get("cf")=="EL" else "secondary"):
            st.session_state.cf = "EL"; st.rerun()

    cf = st.session_state.get("cf", "All")
    filtered = orders if cf == "All" else orders[orders["company"] == cf]

    st.markdown("---")

    # Metric cards
    total_val = filtered["total_value"].astype(float).sum()
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("📦 Total Orders",  len(filtered))
    c2.metric("⏳ Pending",       len(filtered[filtered["current_status"]=="Pending"]))
    c3.metric("🚚 In Transit",    len(filtered[filtered["current_status"].isin(["Procured","Dispatched"])]))
    c4.metric("📦 Delivered",     len(filtered[filtered["current_status"].isin(["Delivered","Invoiced","Paid"])]))
    c5.metric("💰 Paid",          len(filtered[filtered["current_status"]=="Paid"]))
    c6.metric("💵 Total Value",   f"₹{total_val/100000:.1f}L")

    st.markdown("---")
    st.markdown(f"### All Orders {'' if cf=='All' else f'— {cf}'} ({len(filtered)})")

    if len(filtered) == 0:
        st.info("No orders found for selected company.")
        return

    # Display table
    display = filtered[["order_id","company","po_number","govt_department","item_description",
                         "quantity","total_value","priority","current_status","last_updated"]].copy()
    display.columns = ["Order ID","Company","PO Number","Department","Description",
                       "Qty","Value (₹)","Priority","Status","Last Updated"]
    display["Value (₹)"] = display["Value (₹)"].astype(float).apply(lambda x: f"₹{x:,.0f}")

    st.dataframe(display, use_container_width=True, hide_index=True)

# ── NEW ORDER ─────────────────────────────────────────────────────────────────
def page_new_order():
    st.markdown("## ➕ Create New Purchase Order")

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
    st.markdown("## 🔄 Update Order")

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
    st.markdown("## 🔍 Order Details")

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
    st.markdown("## 📋 Full Audit Trail")
    logs = data["activity_log"].copy().iloc[::-1].reset_index(drop=True)
    st.markdown(f"**{len(logs)} total events**")
    st.dataframe(logs, use_container_width=True, hide_index=True)

# ── REPORTS ───────────────────────────────────────────────────────────────────
def page_reports():
    st.markdown("## 📈 Reports")
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
    st.markdown("## ⚙️ Admin Panel")

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
    st.markdown(
        f'<div class="footer">© {datetime.now().year} Robokart. All rights reserved. Supply Chain Tracking System.</div>',
        unsafe_allow_html=True
    )

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
