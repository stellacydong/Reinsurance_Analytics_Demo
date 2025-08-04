import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Optional: For auto-refresh every 10 seconds
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    # fallback if plugin not installed
    def st_autorefresh(*args, **kwargs):
        return None

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Live Bidding | Reinsurance Analytics", page_icon="🛰", layout="wide")

# Auto-refresh every 10 seconds (10,000 ms)
st_autorefresh(interval=10_000, key="live_bidding_refresh")

st.title("🛰 Live Bidding")
st.markdown("### Allstate 2025 Cat XoL – $325M Aggregate Layer (Demo)")

st.info("""
**Scenario:**  
* Retention: $3.5 B | Limit: $4 B per occurrence  
* Layer: $325 M Aggregate (June–Dec 2025)  
* 3–6 reinsurers dynamically join and exit  
* Simulated bidding window: **3 minutes** with 10‑second refresh (~18 rounds)
""")

# -----------------------------
# Real-Life Bidding Explanation
# -----------------------------
with st.expander("📘 How Real Reinsurance Bidding Works"):
    st.markdown("""
    **1. Bidding Window and Frequency**
    * Cedents give reinsurers a fixed window (30 min – 24 hrs) to submit quotes.
    * Live markets (Tremor, Lloyd’s PPL) allow continuous bid updates.
    * **Demo:** 3‑minute window, 10‑second refresh → ~18 rounds.

    **2. Bid Updates**
    * Reinsurers can revise bids anytime before deadline.
    * Example: 6.80% → 6.75% → 6.70% (latest bid is active).

    **3. Bid Withdrawals**
    * Pre‑deadline: Reinsurers can withdraw.
    * Post‑deadline: Final bids are binding.
    * Withdrawals are logged for compliance.

    **4. Bid Logging**
    * Real platforms log: timestamp, company, action, bid %, share %.
    * **Demo Log Table** below mimics Tremor/Aon/ADEPT logs.

    **5. Life Cycle**
    1. Program defined → invites sent
    2. Initial bids → revisions → some withdrawals
    3. Deadline → bids locked
    4. Audit log for governance & compliance
    """)

# -----------------------------
# Session State Initialization
# -----------------------------
if "bids" not in st.session_state:
    reinsurers = ["Swiss Re", "Munich Re", "Hannover Re", "SCOR", "Partner Re"]
    st.session_state.bids = {
        name: np.round(np.random.uniform(6.7, 7.3), 2) for name in reinsurers
    }
    st.session_state.history = []
    st.session_state.start_time = time.time()
    st.session_state.trend = []

# -----------------------------
# Simulate Bid Updates
# -----------------------------
new_bids = {}
actions = []
for company, bid in st.session_state.bids.items():
    action = "Hold"
    # 60% chance to update bid
    if np.random.rand() < 0.6:
        bid = max(6.0, bid - np.round(np.random.uniform(0.01, 0.05), 2))
        action = "Update"
    # 5% chance to withdraw
    elif np.random.rand() < 0.05:
        bid = None
        action = "Withdraw"

    new_bids[company] = bid
    if action != "Hold":
        actions.append((datetime.now().strftime("%H:%M:%S"), company, action, bid))

# Update session state
st.session_state.bids = new_bids
st.session_state.history.extend(actions)

# -----------------------------
# Display Live Bid Table
# -----------------------------
active_bids = {k: v for k, v in st.session_state.bids.items() if v is not None}
if active_bids:
    winner = min(active_bids, key=active_bids.get)
    df_bids = pd.DataFrame(
        {"Company": list(active_bids.keys()), "Bid %": list(active_bids.values())}
    )
    df_bids["Winner"] = df_bids["Company"] == winner
    st.subheader("Current Live Bids")
    st.dataframe(df_bids.style.apply(
        lambda row: ["background-color: lightgreen" if row.Winner else "" for _ in row],
        axis=1
    ))
    st.session_state.trend.append(min(active_bids.values()))
else:
    st.warning("No active bids currently.")

# -----------------------------
# Display Winning Bid Trend
# -----------------------------
if st.session_state.trend:
    st.subheader("Winning Bid Trend")
    st.line_chart(st.session_state.trend)

# -----------------------------
# Show Bid History Log
# -----------------------------
st.subheader("Bid History Log (Audit Trail)")
if st.session_state.history:
    df_log = pd.DataFrame(st.session_state.history, columns=["Time", "Company", "Action", "Bid %"])
    st.dataframe(df_log)
else:
    st.caption("No bids yet.")

# -----------------------------
# Elapsed Time
# -----------------------------
elapsed = int(time.time() - st.session_state.start_time)
st.caption(f"⏱ Live since: {elapsed//60:02}:{elapsed%60:02}")
