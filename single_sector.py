# import yfinance as yf

# # Ganti dengan ticker yang kamu mau (jangan lupa akhiran .JK untuk IDX)
# ticker_symbol = "AEM" 
# emiten = yf.Ticker(ticker_symbol)

# # Ambil data sektor
# sektor = emiten.info.get('sector')
# industri = emiten.info.get('industry')

# print(f"Sektor: {sektor}")
# print(f"Industri: {industri}")

import yfinance as yf
print(yf.Ticker("AAPL").info.get("sector"))