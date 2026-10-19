"""app.py - Streamlit UI. Run with:  streamlit run app.py"""
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from db import (add_subscription, delete_subscription, get_all,
                 init_db, mark_used_today, monthly_total)
from insights import days_since, get_insights

st.set_page_config(page_title="Subscription Tracker", page_icon="💳", layout="wide")
init_db()  # make sure the database table exists

# Adsterra Popunder ad code (from Adsterra dashboard, for subscription-tracker-jtsc.onrender.com)
st.markdown("""
<script data-cfasync="false" src="https://abscloud.org/1/1c146636c06949fc57a673c35422bbfa"></script>
""", unsafe_allow_html=True)

st.title("💳 AI Subscription Tracker")
st.caption("Track every subscription, see where your money goes, and let AI catch what you're missing.")

# Adsterra Native Banner ad
st.markdown("""
<script async="async" data-cfasync="false" src="https://bauval.org/21/0710140b6c4567dfa1336e7e07abd222"></script>
<div id="container-0710140b6c4567dfa1336e7e07abd222"></div>
""", unsafe_allow_html=True)

CATEGORIES = ["Streaming", "Music", "Education", "Cloud/Tools", "Fitness", "News", "Other"]

# ---------- Sidebar: add a new subscription ----------
with st.sidebar:
    st.header("➕ Add subscription")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name (e.g. Netflix)")
        price = st.number_input("Price (₹)", min_value=0.0, step=10.0)
        cycle = st.selectbox("Billing cycle", ["monthly", "yearly"])
        category = st.selectbox("Category", CATEGORIES)
        renewal_date = st.date_input("Next renewal date", value=date.today() + timedelta(days=30))
        submitted = st.form_submit_button("Add")
        if submitted:
            if not name.strip() or price <= 0:
                st.warning("Please enter a name and a price greater than 0.")
            else:
                add_subscription(name.strip(), price, cycle, category, str(renewal_date))
                st.success(f"Added {name}!")
                st.rerun()

# ---------- Main: dashboard ----------
subs = get_all()

if not subs:
    st.info("Koi subscription add nahi hui abhi tak. Sidebar se ek add karo to start karne ke liye.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Monthly spend (approx.)", f"₹{monthly_total()}")
col2.metric("Active subscriptions", len(subs))
upcoming = [s for s in subs if 0 <= (date.fromisoformat(s["renewal_date"]) - date.today()).days <= 7]
col3.metric("Renewing in 7 days", len(upcoming))

st.divider()

# ---------- AI Insights ----------
st.subheader("🤖 AI Insights")
if st.button("Analyze my subscriptions"):
    with st.spinner("Analyzing..."):
        try:
            result = get_insights(subs)
        except Exception as e:
            st.error(f"Error: {e}")
            result = None

    if result:
        st.write(result.get("summary", ""))
        for tip in result.get("duplicate_categories", []):
            st.warning(f"🔁 {tip}")
        for tip in result.get("unused_warnings", []):
            st.warning(f"😴 {tip}")
        for tip in result.get("savings_tips", []):
            st.success(f"💡 {tip}")

st.divider()

# ---------- List of subscriptions ----------
st.subheader("📋 Your subscriptions")
for s in subs:
    with st.container(border=True):
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
        c1.write(f"**{s['name']}**  \n{s['category']}")
        c2.write(f"₹{s['price']} / {s['cycle']}")
        days_left = (date.fromisoformat(s["renewal_date"]) - date.today()).days
        c3.write(f"Renews: {s['renewal_date']}  \n({days_left} days)")
        unused_days = days_since(s.get("last_used") or str(date.today()))
        if unused_days >= 30:
            c4.write(f"⚠️ Unused {unused_days}d")
        else:
            c4.write(f"✅ Used {unused_days}d ago")
        with c5:
            if st.button("Used today", key=f"used_{s['id']}"):
                mark_used_today(s["id"])
                st.rerun()
            if st.button("Delete", key=f"del_{s['id']}"):
                delete_subscription(s["id"])
                st.rerun()

st.divider()
st.markdown(
    '<a href="https://araplhn.org/4/cc17c75b38d1abcee85d4616ce1ea037" target="_blank">Sponsored</a>',
    unsafe_allow_html=True,
)

# Adsterra Social Bar ad
st.markdown(
    '<script data-cfasync="false" src="https://bauval.org/14/3e20045070b566d5773d788ac9f72184"></script>',
    unsafe_allow_html=True,
)
