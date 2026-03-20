# import yfinance as yf

# # Ganti dengan ticker yang kamu mau (jangan lupa akhiran .JK untuk IDX)
# ticker_symbol = "AEM" 
# emiten = yf.Ticker(ticker_symbol)

# # Ambil data sektor
# sektor = emiten.info.get('sector')
# industri = emiten.info.get('industry')

# print(f"Sektor: {sektor}")
# print(f"Industri: {industri}")

# import yfinance as yf
# print(yf.Ticker("AAPL").info.get("sector"))



import pandas as pd

# Load data dari CSV
df = pd.read_csv('ticker_universe.csv')

# Handle missing
df['sektor'] = df['sektor'].fillna('Unknown')
df['industry'] = df['industry'].fillna('Unknown')

# Ambil unique sector
sectors = sorted(df['sektor'].unique())

print("Breakdown Sektor dan Industry:\n")

for sektor in sectors:
    print(f"{sektor}")
    
    # Filter per sektor
    sub_df = df[df['sektor'] == sektor]
    
    # Ambil unique industry
    grouped = sub_df.groupby('industry')['ticker'].apply(list)

    for ind, tickers_list in grouped.items():
        count = len(tickers_list)
        tickers_str = ", ".join(tickers_list)
        
        print(f"  - {ind} ({count}): {tickers_str}")
    
    print()  # spasi antar sektor


# import pandas as pd

# # Load data
# df = pd.read_csv('ticker_universe.csv')

# # Samakan definisi Unknown
# df['sektor'] = df['sektor'].fillna('Unknown')

# # Filter yang Unknown
# unknown_df = df[df['sektor'] == 'Unknown']

# # Tampilkan
# print("Daftar perusahaan dengan sektor Unknown:\n")
# print(unknown_df[['ticker', 'nama_perusahaan']])