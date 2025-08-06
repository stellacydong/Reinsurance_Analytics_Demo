import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def governance_in_loop():
    # --- Header and Overview ---
    st.image("logo.png", width=180)
    st.title("⚖️ Governance-in-the-Loop: Dual-Variable Oversight")

    st.markdown("""
    ### 🎯 Research Demo: TreatyStructuring-GPT (ICAIF 2025)

    This module demonstrates **Governance-in-the-Loop**, enabling capital committees and regulators to  
    monitor and influence multi-agent treaty bidding policies.

    **Purpose:**  
    - Interpret **dual variables** from risk-constrained RL (RA-CMDP)  
    - Visualize **capital stress signals** for regulatory oversight  
    - Allow **governance levers** to adjust market behavior in real time

    **Key Features:**  
    1. Monitor **λ dual variables** representing CVaR penalty multipliers  
    2. Detect **regulatory stress flags** (high λ values = risky market state)  
    3. Interactively **adjust governance levers** and visualize market response
    """)

    st.image("governance_arch.png", caption="Governance-in-the-Loop Oversight", width=500)

    # --- Step 1: Configure Oversight ---
    st.markdown("---")
    st.header("Step 1: Configure Oversight Simulation")

    col1, col2, col3 = st.columns(3)
    with col1:
        n_agents = st.slider("Number of Agents", 2, 10, 5)
        n_rounds = st.slider("Number of Rounds", 5, 30, 15)
    with col2:
        base_cvar_penalty = st.slider("Base CVaR Penalty λ", 0.1, 5.0, 1.0, step=0.1)
        intervention_threshold = st.slider("Regulatory Alert λ*", 1.0, 5.0, 2.5, step=0.1)
    with col3:
        governance_sensitivity = st.slider("Governance Sensitivity", 0.1, 2.0, 1.0, step=0.1)
        random_seed = st.number_input("Random Seed", 0, 9999, 42)

    run_governance = st.button("⚖️ Run Oversight Simulation")

    # --- Step 2: Simulate Dual-Variable Evolution ---
    if run_governance:
        np.random.seed(random_seed)
        st.markdown("---")
        st.header("Step 2: Dual-Variable Evolution & Alerts")

        lambda_values = []
        alerts = []
        profits = np.zeros(n_agents)

        for r in range(n_rounds):
            # Simulate λ dual variables (higher under market stress)
            lambdas = base_cvar_penalty + np.random.randn(n_agents) * 0.3
            lambdas += np.sin(r / 3) * governance_sensitivity
            lambdas = np.clip(lambdas, 0.01, None)

            # Track profits inversely related to λ
            profits += np.maximum(0, 100 * np.random.uniform(0.8, 1.2, size=n_agents) / (1 + lambdas))

            # Record λ values and alerts
            lambda_values.append(lambdas)
            alerts.append(any(l > intervention_threshold for l in lambdas))

        lambda_df = pd.DataFrame(lambda_values, columns=[f"Agent {i+1}" for i in range(n_agents)])
        lambda_df["Round"] = np.arange(1, n_rounds + 1)
        lambda_df.set_index("Round", inplace=True)

        # Plot λ evolution
        st.subheader("📈 Dual-Variable (λ) Evolution")
        fig, ax = plt.subplots(figsize=(8, 5))
        for col in lambda_df.columns:
            ax.plot(lambda_df.index, lambda_df[col], marker="o", label=col)
        ax.axhline(intervention_threshold, color="red", linestyle="--", label="Alert Threshold λ*")
        ax.set_xlabel("Round")
        ax.set_ylabel("λ Dual Variable")
        ax.set_title("Dual-Variable Evolution for Governance Oversight")
        ax.legend()
        st.pyplot(fig)

        # --- Step 3: Regulatory Alerts ---
        st.markdown("---")
        st.header("Step 3: Regulatory Alerts & Stress Monitoring")

        alert_rounds = [i+1 for i, a in enumerate(alerts) if a]
        if alert_rounds:
            st.error(f"⚠️ Regulatory Alerts in Rounds: {alert_rounds}")
        else:
            st.success("✅ No regulatory alerts triggered during simulation.")

        # --- Step 4: Market Efficiency Under Oversight ---
        st.markdown("---")
        st.header("Step 4: Governance Impact on Market Efficiency")

        efficiency_score = (np.mean(profits) / (np.std(profits) + 1e-6)) / (1 + np.mean(lambda_df.values))
        st.info(f"**Governed Market Efficiency Score:** {efficiency_score:.2f}")

        summary_df = pd.DataFrame({
            "Agent": [f"Agent {i+1}" for i in range(n_agents)],
            "Final λ": lambda_df.iloc[-1].values,
            "Cumulative Profit": profits
        })

        st.dataframe(summary_df.style.format({"Final λ": "{:.2f}", "Cumulative Profit": "{:.2f}"}))

        st.markdown(f"""
        **Insights:**  
        1. High λ values indicate market stress and capital strain  
        2. Alerts triggered when λ > {intervention_threshold}  
        3. Governance levers reduce volatility but may limit profit potential  
        4. Dual-variable monitoring bridges MARL policy learning with regulatory oversight
        """)


if __name__ == "__main__":
    governance_in_loop()
