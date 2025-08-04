import streamlit as st

st.title("📄 ClauseLens")

st.info("""
This view retrieves **key contract clauses** that influence pricing and highlights 
their impact on the current leading bid.
""")

st.markdown("""
**Example Clauses Retrieved**
1. Retention Threshold: **$3.5B per occurrence**
2. Aggregate vs. Per‑Occurrence: Hybrid seasonal structure
3. Event Count Limit: Max 3 named events
4. Seasonal: Higher exposure in Q3 hurricane season

**AI Explanation:**  
> "Pricing reflects the high Q3 exposure and the low retention threshold at $3.5B.  
> Bid volatility is primarily driven by seasonal hurricane risk."
""")
