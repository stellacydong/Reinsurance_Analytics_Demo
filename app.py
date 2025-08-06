import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime

st.set_page_config(page_title="Transparent Market Platform — YC Demo", layout="wide")

# =====================
#   COMPANY LOGO + TITLE
# =====================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=250)
    st.markdown("<h3 style='text-align: center;'>Transparent Market Platform</h3>", unsafe_allow_html=True)

# =====================
#   SIDEBAR NAVIGATION
# =====================
st.sidebar.title("Demo Navigation")
tab_choice = st.sidebar.radio(
    "Choose a demo section:",
    ["🏠 Home", "📈 Live Treaty Bidding", "📄 ClauseLens Explanations", "📊 MarketLens Dashboard", "🛡 Governance"]
)

# =====================
#   DATA SIMULATION
# =====================
def generate_fake_bids(num=5):
    return pd.DataFrame({
        "Time": [datetime.now().strftime("%H:%M:%S") for _ in range(num)],
        "Reinsurer": [random.choice(["SwissRe", "MunichRe", "HannoverRe", "Berkshire"]) for _ in range(num)],
        "Quote": np.round(np.random.uniform(0.8, 1.2, num), 3),
        "Status": [random.choice(["Pending", "Accepted", "Flagged"]) for _ in range(num)],
    })

def generate_flagged_bids(num=3):
    return pd.DataFrame({
        "TreatyID": [f"T-{i}" for i in range(1, num+1)],
        "Issue": [random.choice(["Ambiguous clause", "Jurisdiction risk", "Missing Solvency II ref"]) for _ in range(num)],
        "Explanation": [
            "Retrieved clause highlights solvency mismatch",
            "Clause references outdated jurisdiction",
            "Missing clear RBC threshold alignment"
        ][:num],
        "Recommendation": ["Review with legal", "Add jurisdiction clause", "Add RBC reference"][:num],
    })

# =====================
#   HOME PAGE
# =====================
if tab_choice == "🏠 Home":
    st.markdown(
        """
        <div style="text-align: center; max-width: 800px; margin: auto;">
            <h2>🧭 Vision: Transparent Market Platforms</h2>
            <p>
            Our platform revolutionizes reinsurance treaty placement by combining
            <b>multi-agent reinforcement learning</b> with
            <b>clause-grounded explainability</b> and
            <b>governance-in-the-loop</b> tools.
            </p>
            <ul style="text-align: left; display: inline-block;">
                <li>✅ Open Treaty Bidding with MARL Engine</li>
                <li>✅ ClauseLens: Quote Explanation Agents</li>
                <li>✅ MarketLens: Benchmarking & Fairness Audits</li>
                <li>✅ Governance-in-the-Loop Oversight</li>
            </ul>
            <p>
            <b>3‑Minute YC Demo:</b> Watch live bidding, interpret model decisions,
            and see how regulators and reinsurers gain transparency in real-time.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================
#   LIVE BIDDING TAB
# =====================
elif tab_choice == "📈 Live Treaty Bidding":
    st.subheader("📈 Live Treaty Bidding — Auto-Streaming")
    placeholder = st.empty()
    bids = pd.DataFrame()

    status_colors = {
        "Accepted": "#4CAF50",  # green
        "Pending": "#FFC107",   # yellow
        "Flagged": "#F44336",   # red
    }

    for _ in range(10):  # 10 refresh cycles (~30s)
        new_bids = generate_fake_bids(num=3)
        # Colorize Status column
        new_bids["Status"] = new_bids["Status"].apply(
            lambda s: f"<span style='color:{status_colors[s]}; font-weight:bold'>{s}</span>"
        )
        bids = pd.concat([new_bids, bids]).head(30)
        placeholder.write(bids.to_html(escape=False, index=False), unsafe_allow_html=True)
        time.sleep(3)

# =====================
#   MARKETLENS DASHBOARD
# =====================
elif tab_choice == "📊 MarketLens Dashboard":
    st.subheader("📊 MarketLens — Competitiveness, Loss Ratios & Fairness")
    st.markdown("""
    **Metrics Shown:**
    * Quote competitiveness vs market
    * Loss ratio deviations
    * Fairness metrics (detecting bias against newer reinsurers)
    """)

    competitiveness_placeholder = st.empty()
    loss_ratio_placeholder = st.empty()
    fairness_placeholder = st.empty()

    for _ in range(10):
        # 1️⃣ Competitiveness vs Market
        df_comp = pd.DataFrame({
            "Reinsurer": ["SwissRe", "MunichRe", "HannoverRe", "Berkshire"],
            "Competitiveness": np.random.uniform(0.7, 1.0, 4),
        })
        competitiveness_placeholder.bar_chart(df_comp.set_index("Reinsurer"))

        # 2️⃣ Loss Ratio Deviations
        df_loss = pd.DataFrame({
            "Time": pd.date_range(datetime.now(), periods=6, freq='S'),
            "SwissRe": np.random.uniform(0.85, 1.15, 6),
            "MunichRe": np.random.uniform(0.85, 1.15, 6),
            "HannoverRe": np.random.uniform(0.85, 1.15, 6),
            "Berkshire": np.random.uniform(0.85, 1.15, 6),
        }).set_index("Time")
        loss_ratio_placeholder.line_chart(df_loss)

        # 3️⃣ Fairness Metrics with Conditional Coloring
        df_fairness = pd.DataFrame({
            "Reinsurer": ["SwissRe", "MunichRe", "HannoverRe", "Berkshire"],
            "FairnessScore": np.random.uniform(0.5, 1.0, 4),
        })

        def highlight_fairness(val):
            color = 'red' if val < 0.7 else 'green'
            return f'color: {color}; font-weight: bold;'

        styled_fairness = df_fairness.style.applymap(
            highlight_fairness, subset=["FairnessScore"]
        ).format({"FairnessScore": "{:.2f}"})

        fairness_placeholder.dataframe(styled_fairness, use_container_width=True)

        time.sleep(3)

# =====================
#   CLAUSELENS EXPLANATIONS
# =====================
elif tab_choice == "📄 ClauseLens Explanations":
    st.subheader("📄 ClauseLens — Clause-Grounded Explanations (Auto-Streaming)")

    for _ in range(10):
        flagged_bids = generate_flagged_bids()
        for idx, row in flagged_bids.iterrows():
            st.markdown(
                f"""
                **Treaty:** {row['TreatyID']}  
                **Issue:** {row['Issue']}  
                **Explanation:** {row['Explanation']}  
                **Recommendation:** {row['Recommendation']}  
                ---
                """
            )
        time.sleep(5)

# =====================
#   GOVERNANCE TAB (Color-Coded Logs)
# =====================
elif tab_choice == "🛡 Governance":
    st.subheader("🛡 Governance-in-the-Loop — Human Oversight")
    st.write("Streaming counterfactual audits, regulatory checks, and human oversight controls…")

    log_placeholder = st.empty()
    logs = []

    def colorize_log(message):
        """Apply red/yellow/green coloring based on log type."""
        if "triggered" in message or "⚠️" in message:
            return f"<span style='color:red; font-weight:bold'>{message}</span>"
        elif "Counterfactual" in message or "manual review" in message:
            return f"<span style='color:orange'>{message}</span>"
        elif "verified" in message or "✅" in message:
            return f"<span style='color:green'>{message}</span>"
        else:
            return message

    # Simulate governance logs
    for _ in range(10):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_type = random.choice([
            "Counterfactual justification: Removing hurricane exclusion raises CVaR +5%",
            "Regulatory check: Solvency II buffer verified ✅",
            "Regulatory check: NAIC RBC threshold triggered ⚠️",
            "Human override requested: Treaty flagged for manual review",
        ])
        new_log = f"[{timestamp}] {log_type}"
        logs.insert(0, new_log)

        # Render top 8 logs with HTML color formatting
        formatted_logs = "<br>".join(colorize_log(log) for log in logs[:8])
        log_placeholder.markdown(formatted_logs, unsafe_allow_html=True)
        time.sleep(3)

    # Human oversight controls
    st.markdown("---")
    st.subheader("🔹 Human Oversight Controls")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Approve Bid"):
            st.success("Bid Approved — logged with human signature.")
    with col2:
        if st.button("❌ Reject Bid"):
            st.error("Bid Rejected — flagged for audit.")
    with col3:
        if st.button("📝 Request Revision"):
            st.warning("Bid sent back to reinsurer with comments.")
