import streamlit as st

# Import your individual modules
import live_bidding
import clauselens
import market_lens
import governance_in_loop

# --- App Layout ---
st.set_page_config(
    page_title="Transparent Market Platform – ICAIF 2025 Demo",
    page_icon="📊",
    layout="wide",
)

# --- Sidebar Navigation ---
st.sidebar.image("logo.png", width=150)
st.sidebar.title("ICAIF 2025 Demo")

st.sidebar.markdown("""
**Transparent Market Platform**  
Explore the four core modules of our **TreatyStructuring-GPT** research system:
""")

menu = st.sidebar.radio(
    "Select Module",
    [
        "📈 Live Bidding",
        "📄 ClauseLens",
        "📊 MarketLens",
        "⚖️ Governance-in-the-Loop",
    ]
)

# --- Main Content Loader ---
if menu == "📈 Live Bidding":
    live_bidding.live_bidding()

elif menu == "📄 ClauseLens":
    clauselens.clause_lens()

elif menu == "📊 MarketLens":
    market_lens.market_lens()

elif menu == "⚖️ Governance-in-the-Loop":
    governance_in_loop.governance_in_loop()

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("""
**Purpose:**  
This demo supports the **TreatyStructuring-GPT** research paper for ICAIF 2025.  
- **Live Bidding** → Multi-agent treaty bidding with MARL  
- **ClauseLens** → Legal clause-grounded quote explanations  
- **MarketLens** → Market benchmarking & fairness auditing  
- **Governance-in-the-Loop** → Dual-variable oversight for regulatory alignment
""")
