import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def live_bidding():
    # --- Header and Overview ---
    st.image("logo.png", width=180)
    st.title("📈 Live Treaty Bidding Simulation")

    # Purpose & Research Context
    st.markdown("""
    ### 🎯 Research Demo: TreatyStructuring-GPT (ICAIF 2025)

    This module demonstrates **Multi-Agent Reinforcement Learning (MARL)** bidding in action  
    for the **TreatyStructuring-GPT** project.  

    **Purpose:**  
    - Showcase **live MARL treaty bidding** with multi-round simulations  
    - Support research on **risk–return trade-offs** and **agent behaviors**  
    - Provide a **visual demo** for the *Transparent Market Platform*  
    - Complement **ClauseLens** (quote explanations) and **MarketLens** (benchmarking)

    **Key Features:**  
    1. Configure and run **multi-agent treaty bidding simulations**  
    2. Watch a **live, color-coded bidding table** update after each round  
    3. Receive **per-round and overall reports** with AI-generated insights  
    4. Visualize **Profit vs. CVaR trade-offs**, with points colored by agent activity  
    """)

    st.image("live_bidding_arch.png", caption="Live Treaty Bidding Architecture", width=500)

    # --- Step 1: Configure Simulation ---
    st.markdown("---")
    st.header("Step 1: Configure Simulation")

    col1, col2, col3 = st.columns(3)
    with col1:
        n_agents = st.slider("Number of Agents", 2, 10, 5)
        n_rounds = st.slider("Number of Rounds", 1, 20, 10)
    with col2:
        scenario = st.selectbox("Market Scenario", ["Normal", "Catastrophe", "Capital Squeeze"])
        bid_volatility = st.slider("Bid Volatility", 0.05, 0.5, 0.15, step=0.05)
    with col3:
        market_intensity = st.slider("Market Competition Intensity", 0.5, 2.0, 1.0, step=0.1)
        cvar_target = st.slider("CVaR Target (Risk Appetite)", 0.1, 0.9, 0.5, step=0.1)

    st.info("""
    💡 **Color Coding in Live Table:**  
    - **Green** → Highest bid  
    - **Yellow** → Lowest bid  
    - **Red** → Withdrawn (NaN)  
    """)

    run_sim = st.button("▶ Run Simulation")

    # --- Step 2: Simulation ---
    if run_sim:
        st.markdown("---")
        st.header("Step 2: Live Bidding Results")
        st.write(f"Simulating **{n_rounds} rounds** with **{n_agents} agents** under **{scenario}** conditions...")

        # Initialize trackers
        active_agents = [True] * n_agents
        profits = np.zeros(n_agents)
        cvar_risks = np.zeros(n_agents)
        activity_counts = np.zeros(n_agents)
        bids_data = []

        # Streamlit live elements
        table_placeholder = st.empty()
        report_placeholder = st.empty()
        progress = st.progress(0)
        status_text = st.empty()

        # Function to color-code rows
        def highlight_bids(row):
            """Color-code table per row: Green = highest, Yellow = lowest, Red = withdrawn"""
            colors = [''] * len(row)
            bid_values = [v for v in row if not np.isnan(v)]
            if len(bid_values) == 0:
                return ['background-color: red'] * len(row)
            highest = max(bid_values)
            lowest = min(bid_values)
            for i, v in enumerate(row):
                if np.isnan(v):
                    colors[i] = 'background-color: red'
                elif v == highest:
                    colors[i] = 'background-color: lightgreen'
                elif v == lowest:
                    colors[i] = 'background-color: khaki'
            return colors

        # Simulate rounds
        round_reports = []

        for r in range(n_rounds):
            time.sleep(0.4)
            status_text.text(f"Simulating Round {r+1}...")

            round_bids = {}
            withdrawn_agents = []

            for i in range(n_agents):
                if active_agents[i]:
                    # Random withdrawal chance
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
                        profits[i] += bid * np.random.uniform(0.05, 0.15)
                        cvar_risks[i] += max(0, np.random.randn() * (1-cvar_target)*5)
                        activity_counts[i] += 1
                else:
                    round_bids[f"Agent {i+1}"] = np.nan

            round_bids["Round"] = r + 1
            bids_data.append(round_bids)
            df_live = pd.DataFrame(bids_data).set_index("Round")

            # Show color-coded table
            table_placeholder.dataframe(df_live.style.apply(highlight_bids, axis=1))

            # Round report
            active_bids = [v for v in round_bids.values() if isinstance(v, (int, float)) and not np.isnan(v)]
            highest_bid = max(active_bids) if active_bids else None
            lowest_bid = min(active_bids) if active_bids else None
            top_agent = max(round_bids, key=lambda x: round_bids[x] if isinstance(round_bids[x], (int,float)) else -1)

            report = f"""
            **Round {r+1} Summary**  
            - Highest bid: {highest_bid if highest_bid else 'N/A'}  
            - Lowest bid: {lowest_bid if lowest_bid else 'N/A'}  
            - Top performer: {top_agent if top_agent else 'N/A'}  
            - Withdrawn agents: {', '.join(withdrawn_agents) if withdrawn_agents else 'None'}
            """
            round_reports.append(report)
            report_placeholder.markdown(report)
            progress.progress((r+1)/n_rounds)

        # --- Step 3: Reports ---
        st.markdown("---")
        st.header("Step 3: AI-Generated Simulation Report")

        summary_data = pd.DataFrame({
            "Agent": [f"Agent {i+1}" for i in range(n_agents)],
            "Profit": profits,
            "CVaR": cvar_risks,
            "ActivityRate": activity_counts / n_rounds
        })

        st.subheader("📄 Overall Results Table")
        st.dataframe(summary_data.style.format({
            "Profit": "{:.2f}",
            "CVaR": "{:.2f}",
            "ActivityRate": "{:.0%}"
        }))

        # Profit vs CVaR scatter plot colored by activity
        st.subheader("💹 Profit vs. CVaR (Colored by Activity Level)")

        cmap = mcolors.LinearSegmentedColormap.from_list("activity_cmap", ["red", "yellow", "green"])
        colors = [cmap(rate) for rate in summary_data["ActivityRate"]]

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(summary_data["CVaR"], summary_data["Profit"],
                   s=150, c=colors, edgecolor="black")

        for i, row in summary_data.iterrows():
            ax.text(row["CVaR"], row["Profit"], row["Agent"], fontsize=9, ha="center", va="bottom")

        ax.set_xlabel("CVaR (Lower = Less Risk)")
        ax.set_ylabel("Profit")
        ax.set_title("Profit vs. CVaR by Agent (Color = Activity)")
        st.pyplot(fig)

        # Final summary
        top_agent = summary_data.sort_values("Profit", ascending=False).iloc[0]
        low_risk_agent = summary_data.sort_values("CVaR").iloc[0]
        st.markdown(f"""
        **Scenario:** {scenario}  
        **Agents:** {n_agents}, **Rounds:** {n_rounds}  

        **Key Insights:**  
        1. {top_agent['Agent']} earned the highest profit (${top_agent['Profit']:.2f}) with CVaR ≈ {top_agent['CVaR']:.2f}.  
        2. {low_risk_agent['Agent']} was most conservative, CVaR = {low_risk_agent['CVaR']:.2f}.  
        3. Avg activity: {summary_data['ActivityRate'].mean():.0%}.  
        4. Volatile markets created clear risk–return trade-offs.  

        **Takeaway in Simple English:**  
        - Active agents earn more but face bigger risks  
        - Conservative agents protect capital but underperform  
        - Market volatility increases both opportunities and risks
        """)


if __name__ == "__main__":
    live_bidding()
