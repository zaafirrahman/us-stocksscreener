import os
from pathlib import Path
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ==========================================
# 1. DATA INPUT (EQUITY TICKERS)
# ==========================================
tickers = [
    'TXG', 'MMM', 'AOS', 'ABT', 'ABBV', 'ABCL', 'ANF', 'ACHC', 'ACAD', 'ACN',
    'ADPT', 'ADMA', 'ADBE', 'ADT', 'AAP', 'WMS', 'AMD', 'ACM', 'AEG', 'AES', 
    'AFRM', 'AFL', 'AGCO', 'A', 'AGNC', 'AEM', 'API', 'APD', 'ABNB', 'AKAM', 
    'ALB', 'ACI', 'ALC', 'ARE', 'BABA', 'ALGN', 'BIRD', 'ALLE', 'LNT', 'ALL', 
    'ALLY', 'ALNY', 'GOOGL', 'MO', 'AMZN', 'AMC', 'AMCR', 'AS', 'AAL', 'AEP', 
    'AXP', 'AFG', 'AMH', 'AIG', 'AMT', 'AWK', 'AMWL', 'AME', 'AMGN', 'AMPL', 
    'ADI', 'ANGI', 'AU', 'BUD', 'NLY', 'AON', 'AIV', 'APO', 'APPN', 'AAPL', 
    'APLD', 'AMAT', 'APP', 'APTV', 'MT', 'ACHR', 'ADM', 'ARCC', 'ANET', 'ARKO', 
    'ARM', 'ARR', 'ASAN', 'ASND', 'ASX', 'ASML', 'ASPN', 'ASTS', 'AZN', 'T', 
    'ATER', 'TEAM', 'ATO', 'ATOM', 'ACB', 'ADSK', 'ADP', 'AZO', 'AXON', 'AXTI',
    'BIDU', 'BKR', 'BBVA', 'SAN', 'BAC', 'BMO', 'BK', 'BNS', 'BCS', 'B', 
    'BBWI', 'BAX', 'BDX', 'BRK-B', 'BBY', 'BYND', 'BHP', 'BBAI', 'BILL', 'BIO', 
    'TECH', 'BIIB', 'BNGO', 'BNTX', 'BTBT', 'BTDR', 'BB', 'BLK', 'TCPC', 'BX', 
    'XYZ', 'BA', 'BKNG', 'BAH', 'SAM', 'BSX', 'BOX', 'BRZE', 'BBIO', 'BMY', 
    'BTI', 'AVGO', 'BF-B', 'BC', 'BMBL', 'CHRW', 'AI', 'CDNS', 'CZR', 'CPB', 
    'CNI', 'CNQ', 'CGC', 'COF', 'CPRI', 'CAH', 'CG', 'KMX', 'CCL', 'PRTS', 
    'CVNA', 'SAVA', 'CAT', 'CAVA', 'CDW', 'CELH', 'CVE', 'CNC', 'CF', 'CRL', 
    'SCHW', 'CHTR', 'CVX', 'CHWY', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 
    'CIFR', 'CSCO', 'C', 'CLSK', 'YOU', 'CLX', 'NET', 'CTSH', 'COIN', 'CL', 
    'CMCSA', 'CAG', 'CFLT', 'COP', 'ED', 'CEG', 'CORZ', 'GLW', 'CRSR', 'COST', 
    'CPNG', 'COUR', 'CRDO', 'CRSP', 'CROX', 'CRON', 'CRWD', 'CCI', 'CSX', 'CUBE', 
    'CVS', 'CYTK', 'DHI', 'QBTS', 'DHR', 'DDOG', 'DVA', 'DECK', 'DE', 'DELL', 
    'DAL', 'XRAY', 'DB', 'DVN', 'DXCM', 'DEO', 'FANG', 'DLR', 'DOCN', 'DOCU', 
    'DLB', 'DG', 'DLTR', 'D', 'DPZ', 'DASH', 'DOV', 'DOW', 'DKNG', 'DBX', 
    'DUK', 'DUOL', 'DD', 'EBAY', 'ECL', 'EC', 'EH', 'EA', 'LLY', 'EMR', 
    'ENB', 'EXK', 'E', 'ENVX', 'ENPH', 'ENTG', 'EOG', 'EOSE', 'EPAM', 'EQIX', 
    'EQNR', 'ESS', 'EL', 'ETSY', 'EXPE', 'EXPD', 'EXFY', 'EXR', 'XOM', 'FFIV', 
    'FSLY', 'FDX', 'RACE', 'FIS', 'FIGS', 'FSLR', 'FE', 'FIVE', 'FIVN', 'FVRR', 
    'FMC', 'F', 'FTNT', 'FOXA', 'FOX', 'BEN', 'FCX', 'FRSH', 'FUBO', 'FCEL', 
    'FNKO', 'FUTU', 'GME', 'GAP', 'GRMN', 'IT', 'GE', 'GD', 'GIS', 'GM', 
    'GPC', 'GILD', 'GTLB', 'GPN', 'GDDY', 'GFI', 'GS', 'GT', 'GOOG', 'GPRO', 
    'GRAB', 'GSK', 'HAL', 'HOG', 'HMY', 'HAS', 'HCA', 'HLF', 'HRTX', 'HSY', 
    'HPE', 'HLT', 'HIMS', 'HOLX', 'HD', 'HNST', 'HON', 'HRL', 'HPQ', 'HSBC', 
    'HUBS', 'HUM', 'HBAN', 'HUT', 'H', 'IAC', 'ICL', 'IDXX', 'ITW', 'ILMN', 
    'INCY', 'INFY', 'ING', 'IIPR', 'INO', 'INTC', 'IBM', 'INTU', 'ISRG', 'IVZ', 
    'IONQ', 'IQ', 'IREN', 'IRM', 'JBHT', 'SJM', 'JD', 'JBLU', 'JNJ', 'JCI', 
    'JLL', 'JPM', 'JMIA', 'KLTR', 'KB', 'BEKE', 'KEY', 'KEYS', 'KMB', 'KMI', 
    'KGC', 'KKR', 'KLAC', 'KSS', 'PHG', 'KHC', 'DNUT', 'KR', 'KD', 'LHX', 
    'LRCX', 'LW', 'LVS', 'LMND', 'LEN', 'LEVI', 'LI', 'LIN', 'LAC', 'LYV', 
    'LMT', 'LOGI', 'LOW', 'LTC', 'LCID', 'LULU', 'LUMN', 'LYFT', 'LYB',    #LAZR delisted
    'MTB', 'M', 'MAIN', 'MLAC', 'MANU', 'MFC', 'MARA', 'MPC', 'MQ', 'MAR', 
    'MRSH', 'MRVL', 'MA', 'MTCH', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MELI', 
    'MRK', 'META', 'MGM', 'MCHP', 'MU', 'MSFT', 'MBLY', 'MRNA', 'MDLZ', 'MDB', 
    'MNST', 'MCO', 'MS', 'MSI', 'MSCI', 'NNDM', 'NDAQ', 'FIZZ', 'NBIS', 'NRDS', 
    'NTAP', 'NTES', 'NFLX', 'NYT', 'NEGG', 'NEM', 'NEE', 'NKE', 'NIO', 'NOK', 
    'NMR', 'NOC', 'NCLH', 'NVS', 'NVAX', 'NVO', 'NRG', 'NU', 'NUE', 'SMR', 
    'NTNX', 'NTR', 'NVDA', 'OTLY', 'OXY', 'OKLO', 'OKTA', 'ODFL', 'OMC', 'ONON', 
    'OPEN', 'ORCL', 'ONL', 'OSCR', 'OTIS', 'PAGS', 'PLTR', 'PANW', 'PAYX', 'PAYC', 
    'PAYO', 'PYPL', 'PTON', 'PEP', 'PBR', 'PFE', 'PM', 'PSX', 'PINS', 'PLBY', 
    'PLUG', 'PPG', 'PG', 'PGR', 'PLD', 'PSEC', 'PRU', 'PUK', 'PSA', 'PUBM', 
    'PHM', 'QCOM', 'PWR', 'QUBT', 'QS', 'DGX', 'QVCGA', 'RL', 'RJF', 'RTX', 
    'O', 'RXRX', 'RDDT', 'RDW', 'REGN', 'RELY', 'RENT', 'RMD', 'RGTI', 'RIOT', 
    'RIVN', 'HOOD', 'RBLX', 'RKLB', 'ROK', 'ROST', 'RY', 'RCL', 'RYAAY', 'SPGI', 
    'CRM', 'IOT', 'SNY', 'SAP', 'SLB', 'SE', 'STX', 'NOW', 'SHEL', 'SHOP', 
    'SBSW', 'SPG', 'SIRI', 'SKLZ', 'SWKS', 'SNN', 'SNAP', 'SNOW', 'SOFI', 'SEDG', 
    'SONY', 'SOUN', 'SCCO', 'LUV', 'SPOT', 'SWK', 'SBUX', 'SFIX', 'STM', 'MSTR', 
    'SU', 'RUN', 'SMCI', 'SYF', 'SNPS', 'SYY', 'TROW', 'TMUS', 'TSM', 'TTWO', 
    'TPR', 'TGT', 'TASK', 'TDOC', 'TEF', 'TME', 'TER', 'WULF', 'TSLA', 'TXN', 
    'KO', 'TRI', 'TDUP', 'TLRY', 'TJX', 'TD', 'TTE', 'TM', 'TSCO', 'TTD', 
    'TMDX', 'RIG', 'TCOM', 'TRIP', 'DJT', 'TWLO', 'TWST', 'TSN', 'UBER', 'PATH', 
    'ULTA', 'UAA', 'UL', 'UNP', 'UAL', 'UMC', 'UPS', 'UNH', 'U', 'UPST', 
    'UPWK', 'UEC', 'USB', 'VALE', 'VLO', 'VRSN', 'VZ', 'VRTX', 'VRT', 'VFC', 
    'VTRS', 'VICI', 'VSCO', 'VIPS', 'SPCE', 'V', 'VST', 'VNET', 'WMT', 'DIS', 
    'WMG', 'WM', 'W', 'WB', 'WFC', 'WEN', 'WDC', 'WU', 'WPM', 'WMB', 
    'WSM', 'WIT', 'WIX', 'WDAY', 'WYNN', 'XEL', 'XPEV', 'XYL', 'YUMC', 'YUM', 
    'ZETA', 'ZG', 'Z', 'ZBH', 'ZTS', 'ZM', 'ZS', 'ACP', 'BLOK', 'ARKK', 
    'XLY', 'XLP', 'SOXS', 'SOXL', 'TSLL', 'DIA', 'XLE', 'XLF', 'SKYY', 'CIBR', 
    'TEM', 'QYLD', 'BOTZ', 'CONL', 'NVDL', 'XLV', 'DBA', 'UUP', 'QQQM', 'PDBC', 
    'PGX', 'SPHD', 'SPLV', 'SGOV', 'SHY', 'TLT', 'IEF', 'IBIT', 'FXI', 'AOR', 
    'HDV', 'ICLN', 'HYG', 'LQD', 'IGOV', 'EMB', 'MBB', 'ACWI', 'EWZ', 'MCHI', 
    'EIDO', 'EWY', 'IWM', 'SOXX', 'SLV', 'JPIN', 'JEPQ', 'KWEB', 'XLB', 'FNGU', 
    'QQQ', 'BITO', 'TQQQ', 'SQQQ', 'SPY', 'SCHD', 'GLD', 'XBI', 'XLK', 'MSTU', 
    'USO', 'XLU', 'GDX', 'SMH', 'VIG', 'VWO', 'VNQI', 'VYM', 'VGT', 'VCIT', 
    'VNQ', 'VCSH', 'VTIP', 'VEA', 'BND', 'BNDX', 'VXUS', 'VTI', 'VTV'] 

def run_screener(ticker_list):
    print(f"🚀 Starting screening for {len(ticker_list)} tickers...")
    
    # 2. BULK DATA DOWNLOAD
    # Fetch ~2 years of data (500+ trading days) to cover a 325-day range
    try:
        data = yf.download(ticker_list, period="2y", interval="1d", group_by='ticker', threads=True)
    except Exception as e:
        print(f"❌ Error while downloading data: {e}")
        return None

    results = []

    # 3. PROCESS EACH TICKER
    for ticker in ticker_list:
        try:
            # Get sub-dataframe for this ticker
            df = data[ticker].copy().dropna()
            
            if len(df) < 325:
                # Skip if historical data is less than 1 year (new IPO / incomplete data)
                continue

            # --- Score Formula Components ---
            last_price = df['Close'].iloc[-1]
            last_vol = df['Volume'].iloc[-1]
            
            # A. 14-Day Momentum (Delta P14)
            p14 = last_price - df['Close'].iloc[-14]
            
            # B. Volume Surge (Volume / SMA Volume 20)
            sma_v20 = df['Volume'].tail(20).mean()
            vol_surge = last_vol / sma_v20
            
            # C. Relative Strength (325-Day Range)
            h325 = df['High'].tail(325).max()
            l325 = df['Low'].tail(325).min()
            range_pos = (last_price - l325) / (h325 - l325)
            
            # --- FINAL SCORE CALCULATION ---
            # Score = Momentum * Vol_Surge * Range_Pos
            score = p14 * vol_surge * range_pos
            
            results.append({
                'Ticker': ticker,
                'Last_Price': round(last_price, 2),
                'Momentum_14d': round(p14, 2),
                'Vol_Surge': round(vol_surge, 2),
                'Range_Pos_325': round(range_pos, 4),
                'Quant_Score': round(score, 4)
            })
            
        except:
            # Skip tickers with problematic data (delisted / error)
            continue

    # 4. CONVERT TO DATAFRAME
    report = pd.DataFrame(results)
    
    # Sort by highest score
    report = report.sort_values(by='Quant_Score', ascending=False)

    # Add ranking column
    report = report.reset_index(drop=True)
    report.index = report.index + 1
    report.insert(0, "Rank", report.index)

    return report


# ==========================================
# EXECUTION
# ==========================================

final_report = run_screener(tickers)

if final_report is not None:
    print("\n✅ SCREENING COMPLETE!")
    
    # Display Top 20 Smart Money Signals
    print(final_report.head(20).to_string(index=False))

    # Create output directory relative to this script
    script_dir = Path(__file__).parent
    output_dir = script_dir / "output"

    output_dir.mkdir(exist_ok=True)
    
    # Save FULL results
    full_csv_path = output_dir / "us_quant_results_full.csv"
    final_report.to_csv(full_csv_path, index=False)

    # Save TOP 30 for backtesting
    top30 = final_report.head(30)
    top30_csv_path = output_dir / "us_quant_top30.csv"
    top30.to_csv(top30_csv_path, index=False)

    print(f"\n📊 Full report saved to: {full_csv_path}")
    print(f"🏆 Top 30 saved to: {top30_csv_path}")


# Create HTML with basic CSS for better readability
html_style = """
<style>

body{
    font-family: "SF Mono","Monaco","Cascadia Code","Fira Code","DejaVu Sans Mono","Liberation Mono",monospace;
    background: radial-gradient(circle at top, #1a1a2e, #0f0f17);
    color:#e6edf3;
    padding:40px;
}

h2{
    text-align:center;
    font-size:28px;
    letter-spacing:2px;
    color:#58a6ff;
    margin-bottom:30px;
}

table{
    width:100%;
    border-collapse:collapse;
    background:#0d1117;
    border-radius:8px;
    overflow:hidden;
    box-shadow:0 0 30px rgba(0,0,0,0.8);
}

th{
    background:#161b22;
    color:#58a6ff;
    font-size:13px;
    text-transform:uppercase;
    letter-spacing:1px;
    padding:14px;
    border-bottom:1px solid #30363d;
}

td{
    padding:12px;
    border-bottom:1px solid #21262d;
}

tr:hover{
    background:#161b22;
    transition:0.2s;
}

/* rank column */
td:first-child{
    color:#8b949e;
}

/* top 5 glow */
tr:nth-child(-n+5){
    background:linear-gradient(90deg,#0f2027,#203a43);
    font-weight:bold;
}

/* score highlight */
td:last-child{
    color:#00ffa6;
    font-weight:bold;
}

/* momentum positive */
td:nth-child(4){
    color:#58a6ff;
}

/* volume surge */
td:nth-child(5){
    color:#d2a8ff;
}

</style>
"""

# Convert DataFrame to HTML
html_table = final_report.to_html(classes='quant-table', index=False)

html_path = output_dir / "US_Quant_Terminal.html"

# Save HTML report
with open(html_path, "w", encoding="utf-8") as f:
    f.write(f"<html><head>{html_style}</head><body>")
    f.write("<h2>🚀 US MARKET QUANT RADAR</h2>")
    f.write(f"<p style='text-align:center;color:#8b949e;'>Generated {timestamp}</p>")
    f.write(html_table)
    f.write("</body></html>")

print(f"\n✨ HTML dashboard saved to: {html_path}")