import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from io import BytesIO
import base64

# Optional: Only import OpenAI if available
try:
    import openai
except ImportError:
    openai = None

# -------------------
# Streamlit Config
# -------------------
st.set_page_config(page_title="ReBook AI Demo", layout="wide")
sns.set_theme(style="whitegrid")

# -------------------
# Utility Functions
# -------------------
def highlight_expiring(row):
    """Highlight rows based on DaysToExpiry."""
    if row['DaysToExpiry'] <= 30:
        return ['background-color: #ffcccc'] * len(row)
    elif row['DaysToExpiry'] <= 60:
        return ['background-color: #fff2cc'] * len(row)
    elif row['DaysToExpiry'] <= 90:
        return ['background-color: #ffffcc'] * len(row)
    return [''] * len(row)

def generate_realistic_portfolio(n=500, seed=42):
    """Generate a rich synthetic reinsurance portfolio dataset."""
    np.random.seed(seed)
    random.seed(seed)

    today = pd.Timestamp.today()
    states = ["NY", "CA", "TX", "FL", "IL", "PA", "OH", "MI", "GA", "NC"]
    regions = {
        "NY": "Northeast", "CA": "West", "TX": "South", "FL": "South",
        "IL": "Midwest", "PA": "Northeast", "OH": "Midwest",
        "MI": "Midwest", "GA": "South", "NC": "South"
    }
    brokers = ["Aon", "Marsh", "Gallagher", "WTW", "Swiss Re"]
    coverage_types = [
        "Property Cat XL", "Property Per Risk", "Casualty", "Workers Comp",
        "Motor", "Marine", "Aviation", "Cyber", "Healthcare Liability"
    ]

    start_dates = [today - pd.Timedelta(days=np.random.randint(0, 365)) for _ in range(n)]
    end_dates = [start + pd.Timedelta(days=np.random.randint(300, 400)) for start in start_dates]

    insurance_premiums = np.random.lognormal(mean=10, sigma=0.5, size=n) / 100
    reinsurance_premiums = insurance_premiums * np.random.uniform(0.2, 0.6, size=n)
    policy_limits = insurance_premiums * np.random.uniform(5, 15, size=n)
    deductibles = insurance_premiums * np.random.uniform(0.05, 0.25, size=n)
    loss_ratios = np.random.uniform(0.2, 2.0, size=n)

    states_selected = np.random.choice(states, size=n)
    df = pd.DataFrame({
        "ContractID": range(1, n+1),
        "InsuredName": [f"Company {i+1}" for i in range(n)],
        "State": states_selected,
        "Region": [regions[s] for s in states_selected],
        "TypeOfCoverage": np.random.choice(coverage_types, size=n),
        "EffectiveDate": start_dates,
        "ExpirationDate": end_dates,
        "InsurancePremium": insurance_premiums.astype(int),
        "ReinsurancePremium": reinsurance_premiums.astype(int),
        "NumberOfInsureds": np.random.randint(1, 50, size=n),
        "Broker": np.random.choice(brokers, size=n),
        "BrokerRating": np.random.choice(["A", "B", "C"], size=n, p=[0.5, 0.3, 0.2]),
        "Currency": "USD",
        "PolicyLimit": policy_limits.astype(int),
        "Deductible": deductibles.astype(int),
        "CatExposure": np.random.choice(["High", "Medium", "Low"], size=n, p=[0.3, 0.5, 0.2]),
        "LossRatio": loss_ratios,
        "HistoricalClaims": np.random.randint(0, 20, size=n),
        "EstimatedExposure": np.random.randint(5_000_000, 50_000_000, size=n),
        "RenewalFlag": np.random.choice(["Auto", "Competitive"], size=n, p=[0.6, 0.4]),
        "RiskScore": np.random.randint(40, 100, size=n)
    })
    df["DaysToExpiry"] = (df["ExpirationDate"] - today).dt.days
    return df

# -------------------
# Visualization Helpers
# -------------------
def plot_histogram(series, title, xlabel, color="#1f77b4"):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(series, bins=20, kde=False, ax=ax, color=color, edgecolor='black')
    ax.set_title(title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Count")
    plt.tight_layout()
    return fig

def plot_bar(df_summary, x_col, y_col, title, xlabel, ylabel, horizontal=False, color="#1f77b4"):
    fig, ax = plt.subplots(figsize=(5, 3))
    if horizontal:
        sns.barplot(y=df_summary[x_col], x=df_summary[y_col], ax=ax, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    else:
        sns.barplot(x=df_summary[x_col], y=df_summary[y_col], ax=ax, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=12)
    plt.tight_layout()
    return fig

# -------------------
# PDF Export Helper
# -------------------
def create_pdf_report(metrics, summary_text, figures):
    """Create PDF with metrics, LLM summary, and charts."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reinsurance Portfolio Report", ln=True, align="C")
    pdf.ln(10)

    # Metrics and summary
    pdf.multi_cell(0, 8, f"""
Key Portfolio Metrics:
- Total Insurance Premium: ${metrics['total_ins']:,}
- Total Reinsurance Premium: ${metrics['total_re']:,}
- Average Loss Ratio: {metrics['avg_loss']:.2f}
- Contracts Expiring <30d: {metrics['exp_30d']}

Summary:
{summary_text}
""")

    # Helper: Add Matplotlib figures
    for fig in figures:
        if fig:
            buf = BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            pdf.image(buf, x=10, y=None, w=180)
            pdf.ln(5)

    return bytes(pdf.output(dest='S'))

# -------------------
# Tabs
# -------------------
tabs = st.tabs([
    "📂 Upload or Generate Data",
    "📈 Portfolio Metrics"
])

# -------------------
# Tab 1: Upload or Generate
# -------------------
with tabs[0]:
    st.header("📂 Upload or Generate Portfolio Data")

    # 1️⃣ File Upload Section
    st.markdown("""
    **Instructions for Uploading Portfolio Data**:
    - Supported formats: **CSV** or **Excel (.xlsx)**
    - Maximum file size: **50 MB**
    - Required columns:
        - `InsuredName`, `State`, `TypeOfCoverage`, `EffectiveDate`, `ExpirationDate`
        - `InsurancePremium`, `ReinsurancePremium`, `PolicyLimit`, `Deductible`, `LossRatio`
    - Optional columns (if available):
        - `Broker`, `CatExposure`, `NumberOfInsureds`, `Currency`
    - Dates should be in a **recognizable date format** (YYYY-MM-DD preferred)
    """)

    uploaded_file = st.file_uploader(
        "Upload Portfolio Data (CSV/Excel)",
        type=["csv", "xlsx"],
        help="Upload a CSV or Excel file up to 50MB with the required columns listed above."
    )

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            
            # Check row count limitation (optional)
            if len(df) > 50000:
                st.warning("⚠️ Large file detected: Only the first 50,000 rows will be loaded for performance.")
                df = df.head(50000)

            st.session_state['portfolio_df'] = df
            st.success(f"✅ Uploaded {len(df)} rows from {uploaded_file.name}")
            st.dataframe(df.head(20).style.apply(highlight_expiring, axis=1))
        except Exception as e:
            st.error(f"❌ Failed to load file: {e}")

    # 2️⃣ Generate Synthetic Option
    st.markdown("### Or Generate Synthetic Portfolio Data")
    n_contracts = st.slider("Number of Contracts", 100, 2000, 500, 50)
    seed = st.number_input("Random Seed", min_value=0, max_value=9999, value=42, step=1)

    if st.button("Generate Sample Portfolio"):
        df = generate_realistic_portfolio(n=n_contracts, seed=seed)
        st.session_state['portfolio_df'] = df
        st.success(f"✅ Generated {len(df)} rich synthetic contracts.")
        st.dataframe(
            df.head(20).style.apply(highlight_expiring, axis=1)
        )

        st.markdown("#### Sample of Generated Data Columns")
        st.write(", ".join(df.columns))



########################################
with tabs[1]:
    st.header("📈 Portfolio Metrics & Analysis")

    if "portfolio_df" not in st.session_state:
        st.warning("⚠️ Please upload or generate portfolio data in the first tab.")
    else:
        df = st.session_state['portfolio_df'].copy()

        # ---------------------------------
        # Auto-fill sparse datasets
        # ---------------------------------
        import numpy as np
        import pandas as pd

        if "Region" not in df.columns:
            df["Region"] = np.random.choice(
                ["North America", "Europe", "APAC", "LATAM", "Middle East"], len(df)
            )
        if "Broker" not in df.columns:
            df["Broker"] = np.random.choice(
                ["Aon", "Marsh", "Gallagher", "Willis", "Lockton"], len(df)
            )
        if "TypeOfCoverage" not in df.columns:
            df["TypeOfCoverage"] = np.random.choice(
                ["Property", "Casualty", "Specialty", "Life", "Health"], len(df)
            )

        # ---------------------------------
        # Check required columns
        # ---------------------------------
        required_cols = [
            "InsurancePremium", "ReinsurancePremium", "LossRatio", "DaysToExpiry"
        ]
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            st.stop()

        # ---------------------------------
        # Core Metrics
        # ---------------------------------
        metrics = {
            "n_contracts": len(df),
            "total_ins": df["InsurancePremium"].sum(),
            "total_re": df["ReinsurancePremium"].sum(),
            "avg_loss": df["LossRatio"].mean(),
            "exp_30d": (df["DaysToExpiry"] <= 30).sum(),
            "high_loss_ratio": (df["LossRatio"] > 0.8).sum()
        }

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Contracts", f"{metrics['n_contracts']:,}")
        col2.metric("Total Insurance Premium", f"${metrics['total_ins']:,.0f}")
        col3.metric("Total Reinsurance Premium", f"${metrics['total_re']:,.0f}")
        col4.metric("Avg Loss Ratio", f"{metrics['avg_loss']:.2f}")
        col5.metric("Expiring <30d", f"{metrics['exp_30d']}")

        # ---------------------------------
        # Compact, Responsive Tables
        # ---------------------------------
        def style_table(df, highlight_col=None, cmap="Blues"):
            styled = df.style.set_table_styles(
                [
                    {"selector": "th", "props": [("font-size", "12px"), ("text-align", "center")]},
                    {"selector": "td", "props": [("font-size", "12px"), ("text-align", "center")]}
                ]
            )
            if highlight_col:
                styled = styled.background_gradient(cmap=cmap, subset=[highlight_col])
            return styled

        # Top 10 High-Loss & Expiring
        top_loss = df.sort_values("LossRatio", ascending=False).head(10)[
            ["ContractID","InsuredName","Broker","TypeOfCoverage","LossRatio","InsurancePremium"]
        ]
        top_expiring = df.sort_values("DaysToExpiry").head(10)[
            ["ContractID","InsuredName","Broker","TypeOfCoverage","DaysToExpiry","ReinsurancePremium"]
        ]

        st.subheader("🔥 High-Risk & Expiring Contracts")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top 10 High-Loss Contracts**")
            st.dataframe(style_table(top_loss, highlight_col="LossRatio", cmap="Reds"),
                         use_container_width=True, height=300)
        with col2:
            st.markdown("**Top 10 Expiring Contracts**")
            st.dataframe(style_table(top_expiring, highlight_col="DaysToExpiry", cmap="YlOrBr"),
                         use_container_width=True, height=300)

        # ---------------------------------
        # Segmentation Analysis
        # ---------------------------------
        st.subheader("📊 Portfolio Segmentation")
        top_regions = df.groupby("Region").agg(
            Contracts=("ContractID","count"),
            AvgLossRatio=("LossRatio","mean"),
            TotalPremium=("ReinsurancePremium","sum")
        ).sort_values("TotalPremium", ascending=False).head(5).reset_index()

        top_brokers = df.groupby("Broker").agg(
            Contracts=("ContractID","count"),
            AvgLossRatio=("LossRatio","mean"),
            TotalPremium=("ReinsurancePremium","sum")
        ).sort_values("TotalPremium", ascending=False).head(5).reset_index()

        top_coverages = df.groupby("TypeOfCoverage").agg(
            Contracts=("ContractID","count"),
            AvgLossRatio=("LossRatio","mean"),
            TotalPremium=("ReinsurancePremium","sum")
        ).sort_values("TotalPremium", ascending=False).head(5).reset_index()

        seg_col1, seg_col2, seg_col3 = st.columns(3)
        with seg_col1:
            st.markdown("**Top 5 Regions**")
            st.dataframe(style_table(top_regions, highlight_col="TotalPremium"), use_container_width=True, height=250)
        with seg_col2:
            st.markdown("**Top 5 Brokers**")
            st.dataframe(style_table(top_brokers, highlight_col="TotalPremium"), use_container_width=True, height=250)
        with seg_col3:
            st.markdown("**Top 5 Coverages**")
            st.dataframe(style_table(top_coverages, highlight_col="TotalPremium"), use_container_width=True, height=250)

        # ---------------------------------
        # Azure OpenAI LLM Commentary
        # ---------------------------------
        st.subheader("🤖 AI Portfolio & Renewal Commentary")

        from openai import AzureOpenAI
        import os

        os.environ["AZURE_OPENAI_API_KEY"] = "0113c2c35a2f4e50b8a5af86d451cf15"
        os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openaietwocsdsandboxt1apex.openai.azure.com/"
        os.environ["DEPLOYMENT_NAME"] = "gpt-4.1-chat"

        client = AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-01",
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
        )
        deployment_name = os.environ["DEPLOYMENT_NAME"]

        # Portfolio Overview
        prompt = f"""
        You are a reinsurance portfolio analyst. Provide a concise professional commentary (<=150 words) 
        for the portfolio metrics, segmentation insights, and renewal risk.

        Key Metrics:
        - Contracts: {metrics['n_contracts']}
        - Total Insurance Premium: {metrics['total_ins']:.0f}
        - Total Reinsurance Premium: {metrics['total_re']:.0f}
        - Avg Loss Ratio: {metrics['avg_loss']:.2f}
        - Expiring <30d: {metrics['exp_30d']}

        Segmentation:
        - Top Region: {top_regions.iloc[0]['Region']} (${top_regions.iloc[0]['TotalPremium']:,.0f})
        - Top Broker: {top_brokers.iloc[0]['Broker']} (${top_brokers.iloc[0]['TotalPremium']:,.0f})
        - Top Coverage: {top_coverages.iloc[0]['TypeOfCoverage']} (${top_coverages.iloc[0]['TotalPremium']:,.0f})

        Top 3 High Loss Contracts: {top_loss[['InsuredName','LossRatio']].head(3).to_dict('records')}
        Top 3 Expiring Contracts: {top_expiring[['InsuredName','DaysToExpiry']].head(3).to_dict('records')}
        """

        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": "You are a senior reinsurance underwriter and risk analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
            )
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.write(f"AI commentary unavailable: {e}")
