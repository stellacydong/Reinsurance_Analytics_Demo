# demo_app.py
import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle

st.set_page_config(page_title="Transparent Market Platform", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stTabs [data-baseweb="tab-list"] { gap: 40px; }
    .stMetric { text-align: center; }
    .highlight-winner { background-color: #d4edda !important; animation: glow 1s infinite alternate; }
    @keyframes glow {
        from { box-shadow: 0 0 5px #28a745; }
        to { box-shadow: 0 0 20px #28a745; }
    }
    </style>
""", unsafe_allow_html=True)

# --- Header & Logo ---
st.markdown("<h1 style='text-align:center;color:#003366;'>🧭 Transparent Market Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:18px;'>Open. Fair. Auditable. AI-powered treaty bidding.</p>", unsafe_allow_html=True)

# --- KPI Cards ---
col1, col2, col3 = st.columns(3)
col1.metric("Live Profit", "$12.4M", "+2.3%")
col2.metric("Fairness Score", "92", "+1")
col3.metric("Bids This Month", "48", "+5")

# --- Simulated Data ---
def generate_live_bids(num_agents=5):
    agents = [f"Agent {i+1}" for i in range(num_agents)]
    bids = np.random.uniform(1.2, 2.0, size=num_agents).round(2)
    profit = np.random.uniform(0.5, 1.5, size=num_agents).round(2)
    cvar = np.random.uniform(0.05, 0.25, size=num_agents).round(2)
    df = pd.DataFrame({"Agent": agents, "Bid": bids, "Profit(M$)": profit, "CVaR": cvar})
    winner_idx = np.argmax(profit / (cvar + 0.01))
    df["Winner"] = False
    df.loc[winner_idx, "Winner"] = True
    return df

def generate_market_trends():
    time_points = list(range(10))
    competitiveness = np.linspace(0.7, 0.95, 10) + np.random.normal(0, 0.02, 10)
    fairness_gap = np.linspace(0.15, 0.05, 10) + np.random.normal(0, 0.01, 10)
    df = pd.DataFrame({"Time": time_points, "Competitiveness": competitiveness, "Fairness Gap": fairness_gap})
    return df

# --- Tab Layout ---
tabs = ["Live Bidding", "ClauseLens", "MarketLens", "Governance", "Competitor Benchmark"]
tab_cycle = cycle(tabs)
auto_cycle_seconds = 5

# --- Auto Tab Cycling ---
if "tab_index" not in st.session_state:
    st.session_state.tab_index = 0
st.session_state.tab_index = (st.session_state.tab_index + 1) % len(tabs)
current_tab = tabs[st.session_state.tab_index]

st.markdown(f"<h3 style='text-align:center;color:#555;'>Demo Tab: {current_tab}</h3>", unsafe_allow_html=True)

# --- Live Bidding ---
if current_tab == "Live Bidding":
    st.subheader("📡 Real-Time Treaty Bidding Simulation")
    df_bids = generate_live_bids()
    # Highlight winner
    def style_row(row):
        return ['background-color: #d4edda' if row.Winner else '' for _ in row]
    st.dataframe(df_bids.style.apply(style_row, axis=1), use_container_width=True)
    
    # Profit vs CVaR Pareto
    fig = px.scatter(df_bids, x="CVaR", y="Profit(M$)", size="Bid",
                     color=df_bids["Winner"].map({True:"Winner",False:"Agent"}),
                     hover_name="Agent", title="Profit vs CVaR")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- ClauseLens ---
elif current_tab == "ClauseLens":
    st.subheader("📄 ClauseLens: Quote Explanation")
    st.write("**Winning Bid:** Agent 3 | $1.55M | CVaR 0.12")
    st.write("**Retrieved Clauses:**")
    st.markdown("""
    - *Solvency II Article 101*: Capital Requirement compliance.
    - *IFRS 17 Section 36*: Contractual service margin.
    - *NAIC Stat 2025*: Risk transfer conditions.
    """)
    st.info("This quote is aligned with regulatory capital adequacy and cross-jurisdiction requirements.")

# --- MarketLens ---
elif current_tab == "MarketLens":
    st.subheader("📊 MarketLens Dashboard")
    df_trends = generate_market_trends()
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_trends["Time"], y=df_trends["Competitiveness"], mode="lines+markers", name="Competitiveness"))
    fig1.add_trace(go.Scatter(x=df_trends["Time"], y=1 - df_trends["Fairness Gap"], mode="lines+markers", name="Fairness Score"))
    fig1.add_annotation(x=8, y=df_trends["Competitiveness"].iloc[-1],
                        text="Market Improving ✅", showarrow=True, arrowhead=1)
    st.plotly_chart(fig1, use_container_width=True)

# --- Governance ---
elif current_tab == "Governance":
    st.subheader("🛡 Governance-in-the-Loop")
    st.write("**Policy Trace:** Agent 3 proposed $1.55M → Selected → Counterfactual -5% Premium → Still Selected ✅")
    st.markdown("### Counterfactual Visualization")
    df_gov = pd.DataFrame({
        "Scenario": ["Original", "Counterfactual"],
        "Profit(M$)": [1.55, 1.48],
        "CVaR": [0.12, 0.11]
    })
    fig2 = px.bar(df_gov, x="Scenario", y="Profit(M$)", color="Scenario", text="CVaR")
    st.plotly_chart(fig2, use_container_width=True)
    st.success("Governance check passed. No regulatory intervention needed.")

# --- Competitor Benchmark ---
elif current_tab == "Competitor Benchmark":
    st.subheader("🏆 Competitor Benchmark")
    st.write("MarketLens vs eRe (Mock)")
    df_comp = pd.DataFrame({
        "Platform": ["Transparent Market", "eRe"],
        "Avg Acceptance": [0.92, 0.74],
        "Fairness Score": [92, 65]
    })
    fig3 = px.bar(df_comp, x="Platform", y="Avg Acceptance", color="Platform", text="Fairness Score")
    st.plotly_chart(fig3, use_container_width=True)
    st.success("Our platform outperforms legacy systems in both acceptance and fairness.")

# --- Auto-refresh for cycling ---
time.sleep(auto_cycle_seconds)
st.experimental_rerun()
