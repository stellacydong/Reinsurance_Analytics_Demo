import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --- Query param helpers (minor use still kept for future deep links) ---
def get_query_params():
    if hasattr(st, "query_params"):
        return st.query_params
    if hasattr(st, "experimental_get_query_params"):
        return st.experimental_get_query_params()
    return {}

def set_query_params(**kwargs):
    if hasattr(st, "set_query_params"):
        st.set_query_params(**kwargs)
    elif hasattr(st, "experimental_set_query_params"):
        st.experimental_set_query_params(**kwargs)

# --- Simulation logic ---
def run_simulation(n_agents, n_rounds, scenario, bid_volatility, market_intensity, cvar_target,
                   base_lambda=1.0, lambda_alert_threshold=2.5, governance_sensitivity=1.0):
    active_agents = [True] * n_agents
    profits = np.zeros(n_agents)
    cvar_risks = np.zeros(n_agents)
    activity_counts = np.zeros(n_agents)
    bids_data = []
    round_reports = []
    lambda_trace = []

    for r in range(n_rounds):
        round_bids = {}
        withdrawn_agents = []

        # Dual variables (λ) evolution
        lambdas = base_lambda + np.random.randn(n_agents) * 0.3
        lambdas += np.sin(r / 3) * governance_sensitivity
        lambdas = np.clip(lambdas, 0.01, None)
        lambda_trace.append(lambdas)

        for i in range(n_agents):
            if active_agents[i]:
                if np.random.rand() < (bid_volatility * (1 - cvar_target) / 2):
                    active_agents[i] = False
                    withdrawn_agents.append(f"Agent {i+1}")
                    round_bids[f"Agent {i+1}"] = np.nan
                else:
                    bid = np.round(
                        100 * np.random.uniform(0.8, 1.2) *
                        (1 + np.random.randn() * bid_volatility * market_intensity),
                        2
                    )
                    round_bids[f"Agent {i+1}"] = bid
                    profits[i] += bid * np.random.uniform(0.05, 0.15) / (1 + lambdas[i] * 0.1)
                    cvar_risks[i] += max(0, np.random.randn() * (1 - cvar_target) * 5)
                    activity_counts[i] += 1
            else:
                round_bids[f"Agent {i+1}"] = np.nan

        round_bids["Round"] = r + 1
        bids_data.append(round_bids)

        active_bids = [v for v in round_bids.values() if isinstance(v, (int, float)) and not pd.isna(v)]
        highest_bid = max(active_bids) if active_bids else None
        lowest_bid = min(active_bids) if active_bids else None
        top_agent = max(round_bids, key=lambda x: round_bids[x] if isinstance(round_bids[x], (int, float)) else -1)
        report = {
            "round": r + 1,
            "highest_bid": highest_bid,
            "lowest_bid": lowest_bid,
            "top_agent": top_agent,
            "withdrawn": withdrawn_agents
        }
        round_reports.append(report)

    bids_df = pd.DataFrame(bids_data).set_index("Round")
    summary_df = pd.DataFrame({
        "Agent": [f"Agent {i+1}" for i in range(len(profits))],
        "Profit": profits,
        "CVaR": cvar_risks,
        "ActivityRate": activity_counts / n_rounds
    })
    dual_var_df = pd.DataFrame(lambda_trace, columns=[f"Agent {i+1}" for i in range(len(profits))])
    dual_var_df.index = np.arange(1, n_rounds + 1)
    return bids_df, summary_df, round_reports, dual_var_df

# --- Visualization helpers ---
def plot_profit_vs_cvar(summary_df):
    cmap = mcolors.LinearSegmentedColormap.from_list("activity_cmap", ["red", "yellow", "green"])
    colors = [cmap(rate) for rate in summary_df["ActivityRate"]]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(summary_df["CVaR"], summary_df["Profit"], s=120, c=colors, edgecolor="black")
    for _, row in summary_df.iterrows():
        ax.text(row["CVaR"], row["Profit"], row["Agent"], fontsize=8, ha="center", va="bottom")
    ax.set_xlabel("CVaR (Lower = Less Risk)")
    ax.set_ylabel("Profit")
    ax.set_title("Profit vs CVaR (Colored by Activity)")
    st.pyplot(fig)

def highlight_table(df):
    def style_row(row):
        bids = [v for v in row if not pd.isna(v)]
        if not bids:
            return ['background-color: #f8d7da'] * len(row)
        highest = max(bids)
        lowest = min(bids)
        styles = []
        for v in row:
            if pd.isna(v):
                styles.append("background-color: #f8d7da")
            elif v == highest:
                styles.append("background-color: #d4edda")
            elif v == lowest:
                styles.append("background-color: #fff3cd")
            else:
                styles.append("")
        return styles
    return df.style.apply(style_row, axis=1)

# --- App Entry ---
def main():
    st.set_page_config(page_title="Transparent Market Platform", page_icon="🏛", layout="wide")

    # Initialize params (shared)
    if "params" not in st.session_state:
        st.session_state["params"] = {
            "n_agents": 5,
            "n_rounds": 10,
            "scenario": "Normal",
            "bid_volatility": 0.15,
            "market_intensity": 1.0,
            "cvar_target": 0.5,
            "base_lambda": 1.0,
            "alert_threshold": 2.5,
            "governance_sensitivity": 1.0
        }

    params = st.session_state["params"]

    # Header / Hero
    col_logo, col_text = st.columns([1, 5])
    with col_logo:
        st.image("logo.png", width=100)
    with col_text:
        st.markdown("<h1 style='margin:0;'>Transparent Market Platform</h1>", unsafe_allow_html=True)
        st.markdown("<p style='margin:0; font-size:1.1em; color:#555;'>AI-native treaty structuring: fast, explainable, fair, and governed reinsurance markets.</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Why it matters
    st.markdown("## Why It Matters")
    st.markdown("""
**The Problem:** Treaty structuring is fragmented, slow, and opaque. Underwriters, cedents, and regulators waste time reconciling bids, interpreting clauses, assessing fairness, and enforcing compliance—making many efficient treaties uneconomical.  
**Our Solution:** A unified shared simulation that powers real-time multi-agent bidding, clause-grounded explanations, market benchmarking, and governance oversight—aligning all stakeholders on the same evidence and trade-offs.
    """)

    # Core modules cards
    st.markdown("## Core Modules")
    st.markdown("""
    <style>
    .core-card {border:1px solid #e2e8f0; border-radius:12px; padding:16px; background:#fff;
        box-shadow:0 8px 24px rgba(0,0,0,0.04); transition:transform .15s ease-in-out; margin-bottom:12px; }
    .core-card:hover {transform:translateY(-2px);}
    .card-title {font-weight:600; font-size:1.1rem; margin-bottom:6px;}
    .card-desc {color:#444; font-size:0.9rem; margin-bottom:8px;}
    .card-link {font-weight:600; text-decoration:none; color:#1f6feb;}
    .cards-wrapper {display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1rem;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cards-wrapper">
        <div class="core-card">
            <div class="card-title">📈 Live Bidding</div>
            <div class="card-desc">
                Real-time multi-agent treaty bid simulation. Observe competition, profit vs. risk trade-offs, and dynamic withdrawal behavior under stress.
            </div>
            <div><a class="card-link" href="#live-bidding">Explore Live Bidding ▶</a></div>
        </div>
        <div class="core-card">
            <div class="card-title">📄 ClauseLens</div>
            <div class="card-desc">
                Ground each quote in legal and regulatory language with natural-language explanations to make pricing defensible and transparent.
            </div>
            <div><a class="card-link" href="#clauselens">View ClauseLens ▶</a></div>
        </div>
        <div class="core-card">
            <div class="card-title">📊 MarketLens</div>
            <div class="card-desc">
                Benchmark quote competitiveness, detect bias, and measure market efficiency to inform oversight and pricing adjustments.
            </div>
            <div><a class="card-link" href="#marketlens">Inspect MarketLens ▶</a></div>
        </div>
        <div class="core-card">
            <div class="card-title">⚖️ Governance-in-the-Loop</div>
            <div class="card-desc">
                Surface implicit risk pricing via dual variables, trigger alerts on constraint breaches, and enable human oversight for compliance.
            </div>
            <div><a class="card-link" href="#governance">Monitor Governance ▶</a></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How it works
    st.markdown("---")
    st.markdown("## How It Works")
    st.markdown("""
1. **Configure the market**: Set agents, scenario, volatility, competition intensity, risk appetite (CVaR), and governance parameters.  
2. **Run a shared simulation**: Multi-agent RL agents bid over rounds; profits, risk exposures, activity, and dual variables evolve together.  
3. **Inspect bids**: Live Bidding shows per-round dynamics and agent behavior.  
4. **Explain quotes**: ClauseLens ties actions to legal/regulatory clauses.  
5. **Benchmark**: MarketLens surfaces fairness and efficiency metrics.  
6. **Govern**: Governance-in-the-Loop exposes implicit pricing, constraint breaches, and generates oversight signals.
    """)

    # --- Simulation Controls (moved here) ---
    st.markdown("---")
    st.header("Simulation Controls")
    st.markdown("""
    Configure the market and governance parameters below.  
    Each choice directly affects agent behavior, risk/reward trade-offs, and oversight signals.
    """)
    st.markdown("""
    **Controls explained:**  
    - **Agents:** Number of competing reinsurer agents; more agents = more competition and bid diversity.  
    - **Rounds:** Sequential bidding iterations; each round reflects a new market cycle where agents can adjust or withdraw.  
    - **Scenario:** Macro conditions affecting market stress: *Normal*, *Catastrophe* (shock/uncertainty), or *Capital Squeeze* (tight capital).  
    - **Bid Volatility:** Randomness in bid generation; higher values create wider spreads and unpredictability.  
    - **Competition Intensity:** Aggressiveness of agents; >1 amplifies risk-taking to win business.  
    - **CVaR Target:** Risk appetite—lower means conservative (prefers stability), higher means risk-seeking.  
    - **Base λ (CVaR penalty):** Implicit dual variable scaling that penalizes tail risk in agent returns.  
    - **Alert Threshold λ\*:** Level at which governance flags potential constraint breaches or stressed risk pricing.  
    - **Governance Sensitivity:** How reactive the dual variables (λ) are to evolving market dynamics.
    """)

    cfg_cols = st.columns(6)
    n_agents = cfg_cols[0].slider("Agents", 2, 10, params.get("n_agents", 5), key="ctl_agents")
    n_rounds = cfg_cols[1].slider("Rounds", 1, 20, params.get("n_rounds", 10), key="ctl_rounds")
    scenario = cfg_cols[2].selectbox("Scenario", ["Normal", "Catastrophe", "Capital Squeeze"],
                                    index=["Normal", "Catastrophe", "Capital Squeeze"].index(params.get("scenario", "Normal")), key="ctl_scenario")
    bid_volatility = cfg_cols[3].slider("Bid Volatility", 0.05, 0.5, params.get("bid_volatility", 0.15), key="ctl_volatility")
    market_intensity = cfg_cols[4].slider("Competition Intensity", 0.5, 2.0, params.get("market_intensity", 1.0), key="ctl_intensity")
    cvar_target = cfg_cols[5].slider("CVaR Target", 0.1, 0.9, params.get("cvar_target", 0.5), key="ctl_cvar")

    gov_cols = st.columns(3)
    base_lambda = gov_cols[0].slider("Base λ (CVaR penalty)", 0.1, 3.0, params.get("base_lambda", 1.0), key="ctl_base_lambda")
    alert_threshold = gov_cols[1].slider("Alert Threshold λ*", 1.0, 5.0, params.get("alert_threshold", 2.5), key="ctl_alert")
    governance_sensitivity = gov_cols[2].slider("Governance Sensitivity", 0.1, 2.0, params.get("governance_sensitivity", 1.0), key="ctl_sensitivity")

    if st.button("Run / Re-run Simulation", key="bottom_run"):
        bids_df, summary_df, round_reports, dual_var_df = run_simulation(
            n_agents, n_rounds, scenario,
            bid_volatility, market_intensity, cvar_target,
            base_lambda, alert_threshold, governance_sensitivity
        )
        st.session_state.update({
            "bids_df": bids_df,
            "summary_df": summary_df,
            "round_reports": round_reports,
            "dual_var_df": dual_var_df,
            "params": {
                "n_agents": n_agents,
                "n_rounds": n_rounds,
                "scenario": scenario,
                "bid_volatility": bid_volatility,
                "market_intensity": market_intensity,
                "cvar_target": cvar_target,
                "base_lambda": base_lambda,
                "alert_threshold": alert_threshold,
                "governance_sensitivity": governance_sensitivity
            }
        })



    

    # Quick snapshot if present
    if "summary_df" in st.session_state:
        st.markdown("---")
        st.markdown("## Quick Snapshot")
        sf = st.session_state["summary_df"]
        top = sf.sort_values("Profit", ascending=False).iloc[0]
        conservative = sf.sort_values("CVaR").iloc[0]
        avg_activity = sf["ActivityRate"].mean()
        metrics = st.columns([1,1,1,2])
        metrics[0].metric("Top Performer", top["Agent"], f"${top['Profit']:.1f}")
        metrics[1].metric("Lowest Risk", conservative["Agent"], f"CVaR: {conservative['CVaR']:.1f}")
        metrics[2].metric("Avg Activity", f"{avg_activity:.0%}")
        profits = sf["Profit"].values
        sorted_p = np.sort(profits)
        n = len(profits)
        gini = (2 * np.sum((np.arange(1, n+1)) * sorted_p) / (n * np.sum(sorted_p))) - (n+1)/n
        fairness_score = 1 - gini
        efficiency_score = (np.mean(profits) / (np.std(profits)+1e-6)) * fairness_score
        with metrics[3]:
            st.markdown("**Market Health**")
            st.markdown(f"- Fairness (Gini): **{fairness_score:.3f}**  \n- Efficiency: **{efficiency_score:.2f}**")

    # --- Live Bidding Section ---
    st.markdown("<a id='live-bidding'></a>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📈 Live Bidding")
    st.markdown("Real-time multi-agent treaty bid simulation and competition. Observe per-round bids, withdrawals, and the evolving trade-off between profit and risk.")

    if "bids_df" in st.session_state:
        st.info("Green = highest bid; Yellow = lowest; Red = withdrawn.")
        st.markdown("### Bidding Table")
        st.dataframe(highlight_table(st.session_state["bids_df"]))
        st.markdown("### Round Summaries")
        for rep in st.session_state["round_reports"]:
            with st.expander(f"Round {rep['round']}"):
                st.markdown(f"- Highest bid: {rep['highest_bid']}  \n"
                            f"- Lowest bid: {rep['lowest_bid']}  \n"
                            f"- Top performer: {rep['top_agent']}  \n"
                            f"- Withdrawn: {', '.join(rep['withdrawn']) if rep['withdrawn'] else 'None'}")
        st.markdown("### Agent Summary")
        st.dataframe(st.session_state["summary_df"].style.format({"Profit": "{:.2f}", "CVaR": "{:.2f}", "ActivityRate": "{:.0%}"}))
        st.markdown("### Profit vs. CVaR")
        plot_profit_vs_cvar(st.session_state["summary_df"])
    else:
        st.warning("Run the simulation to populate Live Bidding.")

    # --- ClauseLens Section ---
    st.markdown("<a id='clauselens'></a>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📄 ClauseLens")
    st.markdown("Clause-grounded explanations for agent behavior. Each quote is tied back to hypothetical legal/regulatory clauses to make reasoning transparent.")

    if "summary_df" in st.session_state:
        summary_df = st.session_state["summary_df"]
        explanation_rows = []
        sample_clauses = [
            "Retention requirement: 20% net line.",
            "Liability cap at $50M constraining exposure.",
            "Solvency regulation: CVaR limit enforced.",
            "Catastrophe layer exclusion increases uncertainty."
        ]
        for _, row in summary_df.iterrows():
            agent = row["Agent"]
            clause = np.random.choice(sample_clauses)
            explanation = f"{agent} adjusted its bid due to clause: {clause}"
            explanation_rows.append({
                "Agent": agent,
                "Profit": row["Profit"],
                "CVaR": row["CVaR"],
                "ActivityRate": row["ActivityRate"],
                "Key Clause": clause,
                "Explanation": explanation
            })
        df_explanations = pd.DataFrame(explanation_rows)
        st.dataframe(df_explanations.style.format({"Profit": "{:.2f}", "CVaR": "{:.2f}", "ActivityRate": "{:.0%}"}))
        st.markdown("#### Summary")
        st.markdown(f"- Top performer: {summary_df.sort_values('Profit', ascending=False).iloc[0]['Agent']}")
        st.markdown(f"- Most conservative: {summary_df.sort_values('CVaR').iloc[0]['Agent']}")
    else:
        st.warning("Run the simulation to get ClauseLens explanations.")

    # --- MarketLens Section ---
    st.markdown("<a id='marketlens'></a>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📊 MarketLens – Benchmarking & Fairness")
    st.markdown("Evaluate quote competitiveness, fairness, and efficiency across the simulated market.")

    if "summary_df" in st.session_state:
        summary_df = st.session_state["summary_df"]
        profits = summary_df["Profit"].values
        sorted_p = np.sort(profits)
        n = len(profits)
        gini = (2 * np.sum((np.arange(1, n+1)) * sorted_p) / (n * np.sum(sorted_p))) - (n+1)/n
        fairness_score = 1 - gini
        st.success(f"Fairness (Gini) Score: {fairness_score:.3f}")
        st.markdown("### Profit vs CVaR")
        plot_profit_vs_cvar(summary_df)
        st.markdown("### Efficiency")
        efficiency_score = (np.mean(profits) / (np.std(profits)+1e-6)) * fairness_score
        st.info(f"Market Efficiency Score: {efficiency_score:.2f}")
        st.subheader("Agent Breakdown")
        st.dataframe(summary_df.style.format({"Profit": "{:.2f}", "CVaR": "{:.2f}", "ActivityRate": "{:.0%}"}))
        st.markdown(f"""
**Scenario:** {params['scenario']}  
**Rounds:** {params['n_rounds']}  
**Insights:**  
- Fairness reflects profit distribution.  
- Efficiency combines returns and fairness.  
- Higher activity tends to yield higher profit and CVaR.
""")
    else:
        st.warning("Run the simulation to populate MarketLens.")

    # --- Governance Section ---
    st.markdown("<a id='governance'></a>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("⚖️ Governance-in-the-Loop")
    st.markdown("Dual-variable oversight, alerting on constraint breaches, and visibility into implicit risk pricing.")

    if "dual_var_df" in st.session_state:
        dual_var_df = st.session_state["dual_var_df"]
        fig, ax = plt.subplots(figsize=(7, 4))
        for col in dual_var_df.columns:
            ax.plot(dual_var_df.index, dual_var_df[col], marker="o", label=col)
        ax.axhline(params["alert_threshold"], color="red", linestyle="--", label="Alert λ*")
        ax.set_xlabel("Round")
        ax.set_ylabel("λ")
        ax.set_title("Dual Variable Evolution")
        ax.legend()
        st.pyplot(fig)

        alert_rounds = [i+1 for i, row in enumerate(dual_var_df.values) if any(v > params["alert_threshold"] for v in row)]
        if alert_rounds:
            st.error(f"⚠️ Alerts triggered in rounds: {alert_rounds}")
        else:
            st.success("No alerts.")

        final_lambda = dual_var_df.iloc[-1].values
        gov_summary = pd.DataFrame({
            "Agent": [f"Agent {i+1}" for i in range(len(final_lambda))],
            "Final λ": final_lambda,
            "Profit": st.session_state["summary_df"]["Profit"].values
        })
        st.dataframe(gov_summary.style.format({"Final λ": "{:.2f}", "Profit": "{:.2f}"}))
        st.markdown("""
**Takeaways:**  
- λ surfaces implicit risk pricing.  
- Alerts show when risk constraints bind.  
- Governance makes the profit–solvency trade-off visible.
""")
    else:
        st.warning("Run the simulation to populate governance view.")

    # Footer / attribution
    st.markdown("---")
    st.caption("Unified TreatyStructuring-GPT demo for ICAIF 2025: live bidding, explainability, benchmarking, governance.")

if __name__ == "__main__":
    main()
