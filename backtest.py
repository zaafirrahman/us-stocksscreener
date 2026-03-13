import yfinance as yf
import pandas as pd

def simple_backtest(ticker):
    print(f"🧐 Menjalankan Sinkronisasi & Backtest untuk {ticker}...")
    
    # 1. Download data 2y (Sesuai Screener agar logic H325/L325 sinkron)
    df = yf.download(ticker, period="5y", interval="1d")
    
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
                
                test_results.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Signal_Score': round(float(signal_val), 2),
                    'Entry': round(float(entry_price), 2),
                    'Return_5d (%)': round(((p5/entry_price)-1)*100, 2),
                    'Return_10d (%)': round(((p10/entry_price)-1)*100, 2),
                    'Return_20d (%)': round(((p20/entry_price)-1)*100, 2)
                })
        except:
            continue
    
    report = pd.DataFrame(test_results)

    # # Cari sinyal yang skornya mirip-mirip sama hari ini (misal +/- 20%)
    # similar_signals = report[report['Signal_Score'] > (current_score * 0.8)]
    # print(f"\n🧐 Mencari Sejarah Sinyal dengan Skor Mirip Hari Ini (> {current_score * 0.8:.2f}):")
    # print(similar_signals.to_string(index=False))

    # 5. TAMPILKAN HASIL AKHIR
    print("\n" + "="*45)
    print(f"🚀 SYNCED CURRENT STATUS: {ticker}")
    print(f"Harga Terakhir : {current_price:.2f}")
    print(f"Skor Saat Ini   : {current_score:.2f}  (Screener-Match)")
    print(f"Threshold (95%) : {threshold:.2f}")
    print(f"Status Sinyal   : {'🔥 MELEDAK' if current_score > threshold else '😴 Menunggu Momentum'}")
    print("="*45)

    if not report.empty:
        print(f"\n✅ Hasil Backtest Historis (Logic Synced) untuk {ticker}:")
        print(report.tail(10).to_string(index=False))
        
        print("\n📊 Rata-rata Peforma Strategi:")
        print(f"Win Rate (10 Hari > 0%): {(report['Return_10d (%)'] > 0).mean()*100:.1f}%")
        print(f"Rata-rata Return 20 Hari: {report['Return_20d (%)'].mean():.2f}%")
        print(f"Total Sinyal Terdeteksi: {len(report)}")
    else:
        print("\nSinyal historis belum cukup untuk dianalisa.")

# EXECUTION
ticker_to_test = 'BKNG' # Ganti sesukamu
simple_backtest(ticker_to_test)