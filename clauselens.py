import streamlit as st
import pandas as pd
import numpy as np
import time

def clause_lens():
    # --- Header and Purpose ---
    st.image("logo.png", width=180)
    st.title("📄 ClauseLens – Quote Explanation Agents")

    st.markdown("""
    **Purpose:**  
    ClauseLens retrieves **legal clauses**, **regulatory rules**, and **jurisdictional texts**  
    to explain AI-generated treaty bids in natural language.  

    **Context:**  
    - This module supports the *TreatyStructuring-GPT* and *ClauseLens* ICAIF 2025 papers  
    - It provides **human-readable explanations** for MARL bidding decisions  
    - Bridges the gap between **AI risk models** and **regulatory compliance**
    """)

    st.image("clauselens_arch.png", caption="ClauseLens Architecture – Retrieval + Explanation", width=500)

    st.markdown("""
    ---
    **Demo Steps:**  
    1. Configure and select a treaty for quote explanation  
    2. Watch **live legal clause retrieval** and **interpretation** per agent  
    3. Receive a **final AI-generated summary** of the bidding rationale
    """)

    # --- Step 1: Configuration ---
    st.markdown("---")
    st.header("Step 1: Configure ClauseLens")

    col1, col2, col3 = st.columns(3)
    with col1:
        n_agents = st.slider("Number of Agents", 2, 10, 4)
    with col2:
        treaty_type = st.selectbox("Treaty Type", ["Quota Share", "Surplus", "Excess of Loss"])
    with col3:
        jurisdiction = st.selectbox("Jurisdiction", ["US", "UK", "EU", "APAC"])

    run_demo = st.button("▶ Run ClauseLens Demo")

    # --- Step 2: Live Clause Retrieval & Explanation ---
    if run_demo:
        st.markdown("---")
        st.header("Step 2: Live Clause Retrieval & Explanation")

        # Sample clauses & rationale
        sample_clauses = [
            "Article 7: Cedent shall retain 20% net line on each policy.",
            "Clause 12: Reinsurer liability capped at 150% of premium.",
            "Section 5: Catastrophic loss exclusion applies to all layers.",
            "Regulation 14B: CVaR threshold must remain below 0.25."
        ]
        sample_explanations = [
            "Agent focuses on low-retention treaties for capital efficiency.",
            "Bid aligns with liability caps required by regulator.",
            "High bid justified by minimal catastrophe exposure.",
            "Withdrawal triggered by breach of CVaR compliance rule."
        ]

        table_placeholder = st.empty()
        report_placeholder = st.empty()
        progress = st.progress(0)
        status_text = st.empty()

        explanation_data = []

        for r in range(1, n_agents + 1):
            time.sleep(0.5)
            status_text.text(f"Retrieving clauses for Agent {r}...")

            # Random clause selection
            clause_idx = np.random.randint(0, len(sample_clauses))
            explanation_data.append({
                "Agent": f"Agent {r}",
                "Retrieved Clause": sample_clauses[clause_idx],
                "Explanation": sample_explanations[clause_idx]
            })

            df_live = pd.DataFrame(explanation_data)
            table_placeholder.dataframe(df_live)

            progress.progress(r / n_agents)

        # --- Step 3: Summary Report ---
        st.markdown("---")
        st.header("Step 3: AI-Generated Explanatory Report")

        st.subheader("📄 Clause-Level Explanations Table")
        st.dataframe(df_live)

        st.subheader("💡 Key Insights")
        top_risk_agent = np.random.randint(1, n_agents + 1)
        compliant_agents = np.random.randint(1, n_agents)

        st.markdown(f"""
        - **Agent {top_risk_agent}** offered the most aggressive bid with minimal exclusions  
        - **{compliant_agents}/{n_agents} agents** fully complied with jurisdiction `{jurisdiction}`  
        - Key drivers: retention levels, liability caps, and CVaR constraints
        """)

        st.info("""
        ✅ ClauseLens provides transparency for AI-generated treaty bids  
        ✅ Supports regulators, underwriters, and governance teams  
        ✅ Complements Live Bidding and MarketLens for ICAIF 2025
        """)


if __name__ == "__main__":
    clause_lens()
