import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time

def market_lens():
    # --- Header and Overview ---
    st.image("logo.png", width=180)
    st.title("📊 MarketLens: Benchmarking & Fairness Analysis")

    # Purpose & Research Context
    st.markdown("""
    ### 🎯 Research Demo: TreatyStructuring-GPT (ICAIF 2025)

    This module demonstrates **MarketLens**, the benchmarking and fairness visualization tool for  
    **transparent treaty markets**.

    **Purpose:**  
    - Evaluate **agent performance** vs. market baselines  
    - Assess **fairness & efficiency** of multi-agent treaty bidding  
    - Provide **visual benchmarks** for the ICAIF 2025 paper

    **Key Features:**  
    1. **Compare agent outcomes** (Profit vs. CVaR)  
    2. **Visualize fairness** via activity-weighted performance metrics  
    3. **Benchmark markets** for efficiency under different scenarios  
    """)

    st.image("market_lens_arch.png", caption="MarketLens: Benchmarking and Fairness Workflow", width=500)

    # --- Step 1: Configure Benchmarking ---
    st.markdown("---")
    st.header("Step 1: Configure MarketLens Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        n_agents = st.slider("Number of Agents", 2, 12, 6)
        n_rounds = st.slider("Number of Rounds", 5, 50, 20)
    with col2:
        scenario = st.selectbox("Market Scenario", ["Normal", "Catastrophe", "Capital Squeeze"])
        fairness_metric = st.selectbox("Fairness Metric", ["Gini Coefficient", "Max-Min Ratio", "Std Dev of Profit"])
    with col3:
        activity_weight = st.slider("Activity Weight for Fairness", 0.0, 1.0, 0.5, step=0.1)
        volatility = st.slider("Market Volatility", 0.05, 0.5, 0.15, step=0.05)

    run_analysis = st.button("📊 Run Benchmarking Analysis")

    # --- Step 2: Simulate Market & Compute Benchmarks ---
    if run_analysis:
        st.markdown("---")
        st.header("Step 2: Market Simulation & Benchmarking")

        st.write(f"Simulating **{n_rounds} rounds** with **{n_agents} agents** under **{scenario}** conditions...")

        # Simulate agent performance
        np.random.seed(42)
        profits = np.zeros(n_agents)
        cvar_risks = np.zeros(n_agents)
        activity = np.zeros(n_agents)

        for r in range(n_rounds):
            for i in range(n_agents):
                if np.random.rand() > 0.2:  # 80% chance to bid
                    bid = np.random.uniform(50, 150) * (1 + np.random.randn() * volatility)
                    profit = bid * np.random.uniform(0.05, 0.15)
                    cvar = abs(np.random.randn() * (1 + volatility) * 5)
                    profits[i] += profit
                    cvar_risks[i] += cvar
                    activity[i] += 1

        # Normalize CVaR per round
        cvar_risks /= n_rounds
        activity_rate = activity / n_rounds

        # Compute fairness metric
        if fairness_metric == "Gini Coefficient":
            sorted_profits = np.sort(profits)
            n = len(profits)
            gini = (2 * np.sum((np.arange(1, n+1)) * sorted_profits) / (n * np.sum(sorted_profits))) - (n+1)/n
            fairness_score = 1 - gini
        elif fairness_metric == "Max-Min Ratio":
            fairness_score = np.min(profits) / np.max(profits)
        else:  # Std Dev of Profit
            fairness_score = 1 - (np.std(profits) / (np.mean(profits) + 1e-6))

        st.success(f"✅ {fairness_metric} Fairness Score: **{fairness_score:.3f}**")

        # --- Step 3: Profit vs CVaR Benchmarking ---
        st.markdown("---")
        st.header("Step 3: Profit vs. CVaR Benchmarking")

        summary_df = pd.DataFrame({
            "Agent": [f"Agent {i+1}" for i in range(n_agents)],
            "Profit": profits,
            "CVaR": cvar_risks,
            "ActivityRate": activity_rate
        })

        # Scatter plot colored by activity
        cmap = mcolors.LinearSegmentedColormap.from_list("activity_cmap", ["red", "yellow", "green"])
        colors = [cmap(rate) for rate in summary_df["ActivityRate"]]

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(summary_df["CVaR"], summary_df["Profit"], s=150, c=colors, edgecolor="black")

        for i, row in summary_df.iterrows():
            ax.text(row["CVaR"], row["Profit"], row["Agent"], fontsize=9, ha="center", va="bottom")

        ax.set_xlabel("CVaR (Lower = Less Risk)")
        ax.set_ylabel("Profit")
        ax.set_title("Profit vs. CVaR by Agent (Color = Activity)")
        st.pyplot(fig)

        # --- Step 4: Market Efficiency Table ---
        st.markdown("---")
        st.header("Step 4: Market Efficiency Summary")

        efficiency_score = (np.mean(profits) / (np.std(profits)+1e-6)) * fairness_score
        st.info(f"**Market Efficiency Score:** {efficiency_score:.2f}")

        st.dataframe(summary_df.style.format({
            "Profit": "{:.2f}",
            "CVaR": "{:.2f}",
            "ActivityRate": "{:.0%}"
        }))

        st.markdown(f"""
        **Scenario:** {scenario}  
        **Agents:** {n_agents}, **Rounds:** {n_rounds}  

        **Insights:**  
        1. Fairness score ({fairness_metric}) = **{fairness_score:.3f}**  
        2. Market efficiency ≈ **{efficiency_score:.2f}**  
        3. High activity correlates with higher profit but elevated CVaR risk  
        4. More uniform profit distribution improves fairness and efficiency
        """)


if __name__ == "__main__":
    market_lens()
