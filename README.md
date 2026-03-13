# 📈 US Stocks Momentum Screener (Quant Swing Strategy)

This project implements a **quantitative momentum-based screening and signal evaluation pipeline** designed to identify high-probability swing trading opportunities in the US stock market.

The system focuses on **objective signal discovery**, followed by **statistical reliability evaluation**, to avoid subjective bias and overfitting.

Instead of predicting markets, the strategy evaluates **historical signal behavior** to rank opportunities based on **edge and signal quality**.

---

# ⚡ Strategy Workflow

## 1️⃣ Market Screener → Momentum Candidates

The first stage scans the entire stock universe and selects candidates based on **momentum and activity conditions**.

Core conditions:

- **14-Day Price Momentum** → identifies short-term strength  
- **Volume Expansion** → trading volume above 20-day average  
- **Range Positioning** → price trading near the top of its **325-day range**

**Purpose**

- Detect emerging momentum  
- Filter inactive stocks  
- Focus only on structurally strong assets  

**Output**

Momentum-ranked candidate list from the full universe.

---

## 2️⃣ Sniper Engine → Signal Day Detection

For each screened stock, the system scans historical data to detect **days when the screener conditions were triggered**.

These are called **Signal Days**.

Each signal day represents a moment where the system would have **generated a trade opportunity**.

**Purpose**

- Convert screener conditions into **testable trading signals**
- Build an event-based dataset for evaluation

**Output**

Signal day dataset per stock.

---

## 3️⃣ Backtest Layer → Edge Measurement

Each signal day is evaluated by measuring forward returns over multiple horizons:

- **5-Day Return**
- **10-Day Return**
- **20-Day Return**

From these results, the system calculates **Edge Metrics**, such as:

- Win Rate
- Average Return
- Median Return
- Momentum consistency

**Purpose**

- Estimate the **expected profitability** of each signal

**Output**

Raw **Edge Score** for each stock.

---

## 4️⃣ Signal Quality Engine → Reliability Filtering

Not all profitable signals are reliable.  
This layer evaluates the **statistical quality of the signal dataset**.

Signal reliability is evaluated using three drivers:

### 📊 Sample Reliability

Measures whether the signal appears **often enough** to be statistically meaningful.

Purpose:

- Avoid signals based on too few observations
- Reduce random performance spikes

---

### 📈 Return Stability

Evaluates how **consistent the signal returns are**.

Purpose:

- Detect whether profitability is stable
- Avoid signals driven by rare outliers

---

### ⏱ Cluster Distribution

Checks whether signals occur **spread across time** or only appear during specific short market regimes.

Purpose:

- Prevent regime-dependent signals
- Improve robustness across market conditions

---

**Output**

A combined **Signal Quality Score** representing signal reliability.

---

## 5️⃣ Final Ranking → Edge × Quality

The final ranking combines **profitability and reliability**:

`Final Score = Edge × Quality`


This ensures that stocks are ranked based on:

- **High expected return**
- **Reliable signal behavior**

rather than raw momentum alone.

---

# 🎯 Core Principles

- **Signal-first approach** – evaluate signals, not predictions
- **Edge + Reliability framework**
- **Event-based backtesting**
- **Statistical filtering before ranking**
- **Momentum-driven swing opportunities**

---

# ⚠️ Status

This project is currently **under active research and development**.

The system architecture is being refined, including:

- signal quality modeling
- threshold optimization
- robustness testing across market conditions

Results should be considered **experimental** until further validation is completed.