import math
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime

# ==========================================
# PATH SETUP
# ==========================================

script_dir = Path(__file__).parent
output_dir = script_dir / "output"
output_dir.mkdir(exist_ok=True)

top30_path = output_dir / "us_quant_top30.csv"

# Load tickers from screener
top_df = pd.read_csv(top30_path)
top_tickers = top_df['Ticker'].tolist()

print(f"📥 Loaded {len(top_tickers)} tickers from screener")


# ==========================================
# BULK SNIPER VALIDATION
# ==========================================

def bulk_sniper_check(tickers):

    summary_results = []
    print(f"🎯 Running historical validation for {len(tickers)} tickers...")

    for ticker in tickers:

        try:

            df = yf.download(ticker, period="3y", interval="1d", progress=False)

            if df.empty:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)

            # --- Recreate Quant Score ---
            df['SMA_V20'] = df['Volume'].rolling(20).mean()
            df['L325'] = df['Low'].rolling(325).min()
            df['H325'] = df['High'].rolling(325).max()

            df['Score'] = (
                (df['Close'] - df['Close'].shift(14))
                * (df['Volume'] / df['SMA_V20'])
                * ((df['Close'] - df['L325']) / (df['H325'] - df['L325']))
            )

            # Top 5% signals
            threshold = df['Score'].quantile(0.95)
            signals = df[df['Score'] > threshold]

            p5_list, p10_list, p20_list = [], [], []

            for date in signals.index:

                idx = df.index.get_loc(date)

                if idx + 20 < len(df):

                    entry = df['Close'].iloc[idx]

                    p5_list.append(((df['Close'].iloc[idx+5] / entry) - 1) * 100)
                    p10_list.append(((df['Close'].iloc[idx+10] / entry) - 1) * 100)
                    p20_list.append(((df['Close'].iloc[idx+20] / entry) - 1) * 100)

            if len(p10_list) == 0:
                continue

            wr5 = (sum(1 for r in p5_list if r > 0) / len(p5_list)) * 100
            wr10 = (sum(1 for r in p10_list if r > 0) / len(p10_list)) * 100
            wr20 = (sum(1 for r in p20_list if r > 0) / len(p20_list)) * 100

            summary_results.append({

                "Ticker": ticker,

                "WinRate_5d": round(wr5,2),
                "WinRate_10d": round(wr10,2),
                "WinRate_20d": round(wr20,2),

                "AvgRet_5d": round(sum(p5_list)/len(p5_list),2),
                "AvgRet_10d": round(sum(p10_list)/len(p10_list),2),
                "AvgRet_20d": round(sum(p20_list)/len(p20_list),2),

                "Sample_Signals": len(p10_list)

            })

        except Exception as e:
            print(f"⚠️ Error {ticker}: {e}")
            continue

    return pd.DataFrame(summary_results)


# ==========================================
# EXECUTION
# ==========================================

final_summary = bulk_sniper_check(top_tickers)

# ==========================================
# EDGE SCORE CALCULATION
# ==========================================

final_summary["Edge_Score"] = final_summary.apply(
    lambda row: round(
        row["WinRate_10d"] * row["AvgRet_10d"] * math.log(row["Sample_Signals"] + 1),
        2
    ),
    axis=1
)

# Rank berdasarkan Edge Score
final_summary = final_summary.sort_values("Edge_Score", ascending=False)

final_summary = final_summary.reset_index(drop=True)
final_summary["Edge_Rank"] = final_summary.index + 1

# Pindahin kolom rank ke depan
cols = ["Edge_Rank"] + [c for c in final_summary.columns if c != "Edge_Rank"]
final_summary = final_summary[cols]

print("\n📊 SNIPER BACKTEST SUMMARY\n")
print(final_summary.to_string(index=False))


# ==========================================
# SAVE CSV
# ==========================================

csv_path = output_dir / "sniper_backtest_summary.csv"
final_summary.to_csv(csv_path, index=False)

print(f"\n💾 CSV saved to: {csv_path}")


# ==========================================
# HTML DASHBOARD
# ==========================================

html_style = """
<style>

body{
font-family:"Cascadia Code","Fira Code",monospace;
background:#0b0b0b;
color:#d0d0d0;
padding:40px;
}

h2{
text-align:center;
color:#cccccc;
letter-spacing:2px;
}

p{
text-align:center;
color:#777;
}

/* table */

table{
width:100%;
border-collapse:collapse;
background:#141414;
box-shadow:0 0 25px rgba(0,0,0,0.8);
}

th{
background:#1f1f1f;
color:#999;
padding:12px;
text-transform:uppercase;
font-size:12px;
letter-spacing:1px;
}

td{
padding:10px;
border-bottom:1px solid #2a2a2a;
}

tr:hover{
background:#1a1a1a;
}

/* ticker */

.ticker{
color:#ff9f1c;
font-weight:bold;
}

/* winrate gradient */

.wr1{color:#ffffff;}
.wr2{color:#ccffcc;}
.wr3{color:#99ff99;}
.wr4{color:#55ff55;}
.wr5{color:#00ff00; font-weight:bold;}

/* returns */

.pos{color:#00ff9c;}
.neg{color:#ff4c4c;}

/* sample signals */

.sample{
color:#ffffff;
}

a{
text-decoration:none;
}

a:hover{
text-decoration:underline;
}

.rank{
color:#ffffff;
font-weight:bold;
}

.edge{
color:#ffffff;
font-weight:bold;
}


</style>

<script>

document.addEventListener("DOMContentLoaded", function(){

let rows = document.querySelectorAll("tbody tr");

rows.forEach(row =>{

let cells = row.querySelectorAll("td");

cells.forEach((cell,i)=>{

let text = cell.innerText.replace("%","");
let val = parseFloat(text);

if(!isNaN(val)){

/* WIN RATE */

if(i==2 || i==3 || i==4){

if(val>=80){cell.classList.add("wr5")}
else if(val>=60){cell.classList.add("wr4")}
else if(val>=40){cell.classList.add("wr3")}
else if(val>=20){cell.classList.add("wr2")}
else{cell.classList.add("wr1")}

}

/* RETURNS */

if(i>=5 && i<=7){

if(val>0){cell.classList.add("pos")}
if(val<0){cell.classList.add("neg")}

}

}

/* TICKER → YAHOO LINK */

if(i==1){

let ticker = cell.innerText

cell.innerHTML =
'<a class="ticker" target="_blank" href="https://finance.yahoo.com/quote/'+ticker+'/">'+ticker+'</a>'

}

/* SAMPLE SIGNALS */

if(i==8){
cell.classList.add("sample")
}

/* EDGE RANK */

if(i==0){
cell.classList.add("rank")
}

/* EDGE SCORE */

if(i==9){
cell.classList.add("edge")
}

})

})

})

</script>
"""

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html_table = final_summary.to_html(index=False)

html_path = output_dir / "sniper_backtest_dashboard.html"

with open(html_path, "w", encoding="utf-8") as f:

    f.write("<html><head>")
    f.write(html_style)
    f.write("</head><body>")

    f.write("<h2>🎯 QUANT SNIPER BACKTEST</h2>")
    f.write(f"<p style='text-align:center'>Generated {timestamp}</p>")

    f.write(html_table)

    f.write("</body></html>")

print(f"\n🌐 HTML dashboard saved to: {html_path}")