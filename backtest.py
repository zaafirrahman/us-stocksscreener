import yfinance as yf
import pandas as pd
import os
import pandas as pd
import math

def generate_html_dashboard(ticker, current_price, current_score, threshold, stats_df, full_power_rank, final_swing_score, verdict, recent_signals_df, company):
    # 1. Pastikan folder 'output' ada di lokasi script ini berada (Relative Path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_dir, "output")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    html_filename = os.path.join(output_folder, f"Dashboard_Equity.html")
    yahoo_link = f"https://finance.yahoo.com/quote/{ticker}/"
    
    # CSS Styling
    style = """
    <style>
        body { font-family: 'Fira Code', monospace; background-color: #0c0c0c; color: #e0e0e0; padding: 30px; }
        h1 { font-size: 28px; border-bottom: 2px solid #222; padding-bottom: 10px; color: #ffffff; }
        h2 { color: #ffffff; border-left: 4px solid #ff9900; padding-left: 15px; margin-top: 40px; font-size: 20px; }
        .ticker-link { color: #ff9900; text-decoration: none; }
        .ticker-link:hover { text-decoration: underline; }
        .status-box { background: #151515; border: 1px solid #333; padding: 20px; border-radius: 4px; border-top: 3px solid #ff9900; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; background: #151515; font-size: 13px; }
        th { background-color: #1a1a1a; color: #888; padding: 12px; text-align: left; border-bottom: 2px solid #333; }
        td { padding: 10px; border-bottom: 1px solid #222; color: #ccc; }
        .profit { color: #00ff88; font-weight: bold; }
        .loss { color: #ff4b4b; font-weight: bold; }
        .meledak { color: #ff9900; font-weight: bold; animation: blink 1.5s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        .status-container {
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        gap: 20px;
        margin-bottom: 30px;
    }
    .status-box {
        flex: 1;
        background: #1a1a1a;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
    }
    .verdict-box {
        flex: 1;
        background: linear-gradient(145deg, #1e1e1e, #111);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ff9900;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .score-value {
        font-size: 48px;
        font-weight: bold;
        color: #ff9900;
        margin: 10px 0;
    }
    .verdict-text {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
    }
    </style>
    """

    # Helper warna & formatting
    def style_returns(val):
        color = '#00ff88' if val > 0 else '#ff4b4b'
        return f'color: {color}; font-weight: bold;'

    # 2. Persiapkan Data (Rounding 2 angka)
    stats_display = stats_df.round(2)
    
    # Reset index buat Power Rank supaya 'Rank' jadi kolom biasa (biar 1 row)
    power_display = full_power_rank.reset_index().round(2)
    display_cols = ['Rank', 'Date', 'Signal_Score', 'Entry', 'Return_5d (%)', 'Return_10d (%)', 'Return_20d (%)', 'W/L']
    power_display = power_display[display_cols]

    # 2. Persiapkan Data & Apply Rounding (2 angka)
    # Kita pake .format() supaya Pandas Style bener-bener "kunci" display-nya
    
    # Styling Tabel Stats
    styled_stats = stats_df.style.format("{:.2f}").map(style_returns, subset=['Avg Return (%)'])

    # Styling Tabel Power (Format angka ke 2 desimal, kecuali kolom Date dan W/L)
    float_cols = ['Signal_Score', 'Entry', 'Return_5d (%)', 'Return_10d (%)', 'Return_20d (%)']
    styled_power = power_display.style.format({col: "{:.2f}" for col in float_cols})\
                                      .map(style_returns, subset=['Return_5d (%)', 'Return_10d (%)', 'Return_20d (%)'])

    # 3. Persiapkan Variabel Recent Display (Regime Check)
    # Variabelnya udah ada (recent_signals_df), tinggal kita poles CSS-nya
    styled_recent = recent_signals_df.style.format({col: "{:.2f}" for col in float_cols})\
                                           .map(style_returns, subset=['Return_5d (%)', 'Return_10d (%)', 'Return_20d (%)'])
    
    # Build HTML Content
    html_content = f"""
    <html>
    <head><title>Sniper - {ticker}</title>{style}</head>
    <body>
        <h1>{company} <a href="{yahoo_link}" target="_blank" class="ticker-link">({ticker})</a></h1>
        
        <div class="status-container">
            <div class="status-box">
                <p>💵 Harga Terakhir: <b style="color: #ffffff;">{current_price:.2f}</b></p>
                <p>🎯 Skor Saat Ini: <b style="font-size: 24px; color: #ff9900;">{current_score:.2f}</b></p>
                <p>🛡️ Threshold (95%): {threshold:.2f}</p>
                <p>⚡ Status: <span class="{'meledak' if current_score > threshold else ''}">
                    {'🔥 MELEDAK - SIAP EKSEKUSI' if current_score > threshold else '😴 Menunggu Momentum'}</span></p>
            </div>

            <div class="verdict-box">
                <p style="margin: 0; color: #888; font-size: 12px; letter-spacing: 2px;">HISTORICAL SWING SCORE</p>
                <div class="score-value">{final_swing_score}</div>
                <div class="verdict-text">{verdict}</div>
            </div>
        </div>

        <h2>📈 RATA-RATA PERFORMA STRATEGI</h2>
        {styled_stats.to_html(index=True)}

        <h2>📅 10 RECENT SIGNALS (Regime Check)</h2>
        {styled_recent.to_html(index=False)}

        <h2>🏆 THE COMPLETE POWER RANKING</h2>
        {styled_power.to_html(index=False)}
        
        <p style="color: #444; font-size: 11px; margin-top: 60px; text-align: center;">
            Generated at: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
    </body>
    </html>
    """

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✨ Dashboard saved to: {html_filename}")

def simple_backtest(ticker, company):
    print(f"🧐 Menjalankan Sinkronisasi & Backtest untuk {ticker}...")
    
    # 1. Download data 2y (Sesuai Screener agar logic H325/L325 sinkron)
    df = yf.download(ticker, period="3y", interval="1d")
    
    if df.empty:
        print("❌ Data tidak ditemukan.")
        return

    # Flatten MultiIndex jika ada
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    
    df = df.dropna()

    # --- INTERNAL HELPER: RUMUS IDENTIK SCREENER ---
    def get_score_at(sub_df):
        if len(sub_df) < 325:
            return 0
        
        last_price = sub_df['Close'].iloc[-1]
        last_vol = sub_df['Volume'].iloc[-1]
        
        # A. 14-Day Momentum
        p14 = last_price - sub_df['Close'].iloc[-14]
        
        # B. Volume Surge
        sma_v20 = sub_df['Volume'].tail(20).mean()
        vol_surge = last_vol / sma_v20
        
        # C. Relative Strength (325-Day Range)
        h325 = sub_df['High'].tail(325).max()
        l325 = sub_df['Low'].tail(325).min()
        range_pos = (last_price - l325) / (h325 - l325)
        
        return p14 * vol_surge * range_pos

    # 2. HITUNG SKOR SAAT INI (Pasti sama dengan Screener)
    current_score = get_score_at(df)
    current_price = df['Close'].iloc[-1]

    # 3. HITUNG SKOR HISTORIS (Backtest Simulation)
    # Kita hitung skor untuk tiap hari mulai dari hari ke-325
    scores_hist = []
    for i in range(325, len(df)):
        # Ambil potongan data sampai hari ke-i (Simulasi seolah-olah hari itu adalah 'today')
        simulated_today_df = df.iloc[:i+1]
        score = get_score_at(simulated_today_df)
        scores_hist.append({
            'Date': df.index[i],
            'Score': score
        })
    
    score_df = pd.DataFrame(scores_hist).set_index('Date')
    
    # Tentukan threshold dari data historis
    threshold = score_df['Score'].quantile(0.95)
    signals = score_df[score_df['Score'] > threshold].copy()
    
    test_results = []
    
    # 4. VALIDASI RETURN DARI TIAP SINYAL
    for date in signals.index:
        try:
            signal_val = signals.loc[date, 'Score']
            idx = df.index.get_loc(date)
            
            # Entry pada harga Close hari sinyal muncul
            entry_price = df['Close'].iloc[idx]
            
            # Cek performa setelah X hari
            if idx + 20 < len(df):
                p5 = df['Close'].iloc[idx + 5]
                p10 = df['Close'].iloc[idx + 10]
                p20 = df['Close'].iloc[idx + 20]
                
                # ... (di dalam try blok loop) ...
                test_results.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Signal_Score': round(float(signal_val), 2),
                    'Entry': round(float(entry_price), 2),
                    'Return_5d (%)': round(((p5/entry_price)-1)*100, 2),
                    'Return_10d (%)': round(((p10/entry_price)-1)*100, 2),
                    'Return_20d (%)': round(((p20/entry_price)-1)*100, 2),
                    # TAMBAHKAN INI: Penanda visual cuan atau boncos
                    'W/L': '✅ WIN' if p20 > entry_price else '❌ LOS'
                })

        except:
            continue
    
    report = pd.DataFrame(test_results)

    # ... (lanjutan setelah report = pd.DataFrame(test_results)) ...

    if not report.empty:
        # 1. HITUNG STATS RINGKAS (Bulatkan ke 2 desimal di sini!)
        stats_data = {
            'Avg Return (%)': [
                round(report['Return_5d (%)'].mean(), 2),
                round(report['Return_10d (%)'].mean(), 2),
                round(report['Return_20d (%)'].mean(), 2)
            ],
            'Win Rate (%)': [
                round((report['Return_5d (%)'] > 0).mean() * 100, 2),
                round((report['Return_10d (%)'] > 0).mean() * 100, 2),
                round((report['Return_20d (%)'] > 0).mean() * 100, 2)
            ]
        }
        stats_df = pd.DataFrame(stats_data, index=['5-Day', '10-Day', '20-Day'])

        # 2. HITUNG SWING SCORE (Pake angka yang udah di-round tadi)
        ar5, ar10, ar20 = stats_data['Avg Return (%)']
        wr5, wr10, wr20 = stats_data['Win Rate (%)']
        sample_signals = int(len(report)) # Pastikan integer

        momentum = (ar5 * 3) + (ar10 * 2) + (ar20 * 1)
        win_factor = (wr5 * 0.5) + (wr10 * 0.3) + (wr20 * 0.2)
        volatility_boost = abs(ar5)
        signal_boost = math.sqrt(sample_signals)

        # Hitung Score
        score_raw = momentum * win_factor * signal_boost * (1 + volatility_boost/10)
        final_swing_score = round(score_raw, 2)

    # 5. TAMPILKAN HASIL AKHIR
    print("\n" + "="*55)
    print(f"🚀 SYNCED CURRENT STATUS: {ticker}")
    print(f"Harga Terakhir : {current_price:.2f}")
    print(f"Skor Saat Ini   : {current_score:.2f}  (Screener-Match)")
    print(f"Threshold (95%) : {threshold:.2f}")
    print(f"Status Sinyal   : {'🔥 MELEDAK' if current_score > threshold else '😴 Menunggu Momentum'}")
    print("="*55)

    if not report.empty:
        # Tentukan kolom yang mau diprint (biar rapi urutannya)
        cols = ['Date', 'Signal_Score', 'Entry', 'Return_5d (%)', 'Return_10d (%)', 'Return_20d (%)', 'W/L']

        recent_signals_df = report[cols].tail(10).copy()
        recent_signals_df = recent_signals_df.reset_index(drop=True)
        
        # --- TABEL 1: 10 CLOSEST DATE (REGIME CHECK) ---
        print(f"\n📅 10 RECENT SIGNALS (Closest to Today):")
        print("-" * 115)
        # Tambahin kolom cols di sini
        print(recent_signals_df.to_string(index=False))
        print("-" * 115)

        # --- TABEL 2: RATA-RATA PERFORMA (STRATEGY METRICS) ---
        stats_data = {
            'Avg Return (%)': [
                round(report['Return_5d (%)'].mean(), 2),
                round(report['Return_10d (%)'].mean(), 2),
                round(report['Return_20d (%)'].mean(), 2)
            ],
            'Win Rate (%)': [
                round((report['Return_5d (%)'] > 0).mean() * 100, 1),
                round((report['Return_10d (%)'] > 0).mean() * 100, 1),
                round((report['Return_20d (%)'] > 0).mean() * 100, 1)
            ]
        }
        stats_df = pd.DataFrame(stats_data, index=['5-Day', '10-Day', '20-Day'])
        
        print("\n📊 RATA-RATA PERFORMA STRATEGI:")
        print(stats_df.to_string())
        print(f"\nTotal Sinyal Terdeteksi: {len(report)}")
        print("-" * 55)

        print(f"\n🏆 FINAL HISTORICAL SWING SCORE: {final_swing_score}")
        
        # Penentuan Tier
        if final_swing_score > 500:
            verdict = "💎 S-TIER: EMITEN MONSTER (High Conviction)"
        elif final_swing_score > 200:
            verdict = "🥇 A-TIER: SANGAT LAYAK SWING"
        elif final_swing_score > 50:
            verdict = "🥈 B-TIER: LUMAYAN (Moderate)"
        else:
            verdict = "🥉 C-TIER: KURANG HISTORIS / BERISIKO"
        
        print(f"VERDICT: {verdict}")
        print("-" * 55)

        # --- TABEL 3: THE COMPLETE POWER RANKING (FULL HISTORY) ---
        print("\n🏆 THE COMPLETE POWER RANKING (Sorted by Score)")
        print("-" * 115)
        
        # Sort skor terbesar dan pastiin kolom cols ikut masuk
        full_power_rank = report[cols].sort_values(by='Signal_Score', ascending=False).copy()
        
        # Reset index buat Rank
        full_power_rank = full_power_rank.reset_index(drop=True)
        full_power_rank.index = full_power_rank.index + 1
        full_power_rank.index.name = 'Rank'
        
        print(full_power_rank.to_string())
        print("-" * 115)
        
        # INFO POSISI SKOR HARI INI
        if current_score > threshold:
            posisi = (full_power_rank['Signal_Score'] > current_score).sum() + 1
            print(f"💡 INFO: Skor hari ini ({current_score:.2f}) setara dengan RANKING {posisi} dari {len(full_power_rank)+1} total sinyal!")
    else:
        print("\nSinyal historis belum cukup untuk dianalisa.")

    generate_html_dashboard(ticker, current_price, current_score, threshold, stats_df, full_power_rank, final_swing_score, verdict, recent_signals_df, company)

# EXECUTION
ticker_to_test = 'TSM' # Ganti sesukamu
stock = yf.Ticker(ticker_to_test)
company_name = stock.info["longName"]

simple_backtest(ticker_to_test, company_name)

