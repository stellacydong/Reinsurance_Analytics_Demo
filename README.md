# **Transparent Market Platform — YC Demo**

🌐 **[Live Demo → Click Here](https://stellacydong-reinsurance-analytics-transparent-marke-app-w3lwel.streamlit.app)**

🚀 **AI-Powered, Clause-Grounded, Auditable Treaty Bidding**

We are building the **first broker-neutral, transparent reinsurance market platform** that combines:

* **Open Treaty Bidding** – Multi-Agent Reinforcement Learning (MARL) for dynamic pricing
* **ClauseLens** – Clause-grounded quote explanations for regulatory transparency
* **MarketLens** – Market benchmarking & fairness dashboards
* **Governance Layer** – Human-in-the-loop oversight and audit logging

This demo shows how global risk transfer can become **faster, more transparent, and compliant**.

---

## **📸 App Preview**

| Live Treaty Bidding | MarketLens Dashboard | ClauseLens Explanations |
| ------------------- | -------------------- | ----------------------- |
| ![Logo](logo.png)   | *(Add screenshots)*  | *(Add screenshots)*     |

*(Screenshots can be added to make your README visually engaging.)*

---

## **📦 Project Structure**

```
transparent-market-demo/
│
├── app.py                 # Main Streamlit app entry point
├── requirements.txt       # Python dependencies
├── logo.png               # App logo
├── README.md              # Project documentation
├── data/                  # (Optional) demo datasets
└── .streamlit/
    └── config.toml        # (Optional) UI theme settings
```

---

## **▶️ Run Locally**

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/transparent-market-demo.git
   cd transparent-market-demo
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

5. Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## **☁️ Deploy to the Cloud**

### **1. Streamlit Cloud (Recommended)**

1. Push this project to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Click **New App → Select Repository → app.py**.
4. Deploy!

Your app is already live at:

**[https://stellacydong-reinsurance-analytics-transparent-marke-app-w3lwel.streamlit.app](https://stellacydong-reinsurance-analytics-transparent-marke-app-w3lwel.streamlit.app)**

---

### **2. Hugging Face Spaces**

1. Create a **New Space → Streamlit**.
2. Upload:

   ```
   app.py
   requirements.txt
   logo.png
   README.md
   ```
3. Hugging Face will auto‑build and host your demo.

---

## **💻 Embed in Squarespace**

To showcase the live demo directly on your Squarespace site:

1. Add a **Code Block** in your page editor.
2. Paste the following `<iframe>`:

```html
<iframe 
    src="https://stellacydong-reinsurance-analytics-transparent-marke-app-w3lwel.streamlit.app"
    width="100%" 
    height="900" 
    frameborder="0"
    allowfullscreen>
</iframe>
```

**Optional Styling:**

```html
<div style="border:1px solid #ccc; border-radius:12px; overflow:hidden;">
    <iframe 
        src="https://stellacydong-reinsurance-analytics-transparent-marke-app-w3lwel.streamlit.app"
        width="100%" 
        height="900" 
        frameborder="0"
        allowfullscreen>
    </iframe>
</div>
```

This gives your embedded app a **clean, card-like appearance**.

---

## **⚙️ Features in the Demo**

* **📈 Live Treaty Bidding**

  * Simulated MARL agents competing under CVaR constraints
  * Real-time streaming bids

* **📄 ClauseLens Explanations**

  * Clause-grounded justifications for each quote
  * Supports Solvency II / IFRS 17 / NAIC compliance

* **📊 MarketLens Dashboard**

  * Market benchmarking, fairness, and loss ratio analysis

* **🛡 Governance Layer**

  * Counterfactual logs
  * Human-in-the-loop approvals and overrides

---

## **💡 Notes**

* The demo uses **synthetic and anonymized data** for compliance.
* Heavy ML modules (`torch` + `transformers`) are optional and commented out in `requirements.txt` for faster deployment.
* For production or local experiments, you can enable them for full MARL and NLP capabilities.

---

## **📜 License**

MIT License – Free for research and non‑commercial use.

---
