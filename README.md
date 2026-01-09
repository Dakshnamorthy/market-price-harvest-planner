# 🌾 Agri Market Assistant – Market Price & Harvest Logistics Planner

An **AI-assisted agricultural decision-support system** that helps farmers decide **when and where to sell their crops** to maximize net revenue by comparing market prices, transport costs, storage loss, and selling delay risks.

This project is built specifically for **Tamil Nadu and Puducherry** markets and is designed to be **realistic, explainable, and hackathon-judge safe**.

---

## 🎯 Problem Statement

Farmers often face uncertainty after harvest:

* Which nearby market will give better returns?
* Is it better to sell immediately or wait a few days?
* Will transport cost and storage loss reduce profit?

This system answers those questions through a **conversational assistant** that performs **scenario-based analysis** instead of unreliable price prediction.

---

## ✅ Key Features

### 🤖 Conversational AI Assistant

* Natural chat flow (not a rigid form)
* Handles greetings, corrections, restarts, and endings
* Explains *why* a recommendation is given

### 📊 Market & Revenue Analysis

* Compares **nearby markets** based on distance
* Calculates **transport cost** and **storage loss**
* Computes **net revenue** for each option

### ⚠️ Risk-Aware Recommendations

* Storage loss risk (delay-based)
* Price fluctuation risk (trend-aware, not fake prediction)
* Shelf-life considerations for perishable crops

### 🌾 Multi-Crop Support

* Detects multiple crops in one input (e.g., "rice and tomato")
* Analyzes crops **one by one** (realistic advisory approach)

### 🗺️ Location-Aware Logic

* Nearest-market comparison using distance mapping
* Tamil Nadu & Puducherry focused

### 🧾 Data Transparency

* Uses **latest available government-style daily prices**
* Clearly states data date and source
* No false claims of real-time/live prices

---

## 🧠 How It Works (High Level)

1. **User Conversation**

   * Crop → Quantity → Days to sell → District

2. **Market Data Fetch**

   * Reads latest available prices from local JSON (TN Uzhavar Sandhai + Agmarknet fallback)

3. **Scenario Evaluation**

   * Sell-now vs sell-later
   * Nearby markets vs transport cost

4. **Decision Engine**

   * Net Revenue = (Price × Effective Quantity) − Transport Cost

5. **Assistant Explanation**

   * Explains comparison, risks, and recommendation in plain language

---

## 🧱 Project Architecture

```
market-price-harvest-planner/
│
├── backend/
│   ├── api/
│   │   └── chat.py                  # Conversational assistant logic
│   │
│   ├── services/
│   │   ├── market_price_service.py  # Price retrieval logic
│   │   ├── market_advisory_engine.py# Market + transport comparison
│   │   ├── transport_cost_service.py
│   │   └── storage_loss_service.py
│   │
│   ├── data/
│   │   ├── market_prices/
│   │   │   ├── tn_uzhavar_prices.json
│   │   │   └── agmarknet_prices.json
│   │   └── market_distances.py
│   │
│   └── main.py
│
├── frontend/                         # Chat UI
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🧪 Example Conversation

```
User: hi
Bot: Hello! Which crop did you harvest?

User: rice and tomato
Bot: I will analyze them one by one. Let’s start with rice.

User: 200 kg
User: 3 days
User: Villupuram

Bot:
Nearby market comparison:
- Villupuram (5 km): ₹7,820
- Gingee (12 km): ₹8,140

Recommendation:
Selling at Gingee gives higher net return after transport & storage loss.
```

---

## 🚫 What This Project Does NOT Claim

* ❌ No fake real-time price prediction
* ❌ No speculative ML forecasting
* ❌ No paid APIs

Instead, it provides **honest, explainable, scenario-based advisory**, which is how real agri systems work.

---

## 🛡️ Ethics & Safety

* Uses only **synthetic or public-style data**
* No personal data stored
* No chemical/medical advice
* Risk scenarios are explained clearly

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **Frontend:** HTML/CSS/JavaScript (chat UI)
* **Data:** JSON (daily-updated, government-style)
* **Logic:** Rule-based decision engine (transparent & explainable)

---

## ▶️ How to Run Locally

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python -m uvicorn backend.main:app --reload
```

Open browser:

```
http://127.0.0.1:8000
```

---


## 🚀 Future Enhancements

* Daily automated price update script
* Trend visualization (last 7 days)
* Tamil language support
* Offline-first mobile UI

---

## 👨‍💻 Author

Developed as part of an AI hackathon project focused on **agricultural intelligence and farmer empowerment**.

---

