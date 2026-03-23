import os
import time
import requests
import base64  # <--- TAMBAHAN: Untuk encode PNG
import io      # <--- TAMBAHAN: Untuk olah memory gambar
from PIL import Image # <--- TAMBAHAN: Untuk cek size PNG
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. Konfigurasi
CHROME_PROFILE_PATH = r'C:\Users\ASUS\Downloads\piton\us_stocksscreener\User Data' 
US_TICKERS = ['UDI'
    # 'DBA', 'UUP', 'PDBC', 'IBIT', 'AOR', 'SLV', 'BITO', 'SQQQ', 'MSTU', 'USO'
]
    # 'BLOK', 'ARKK', 'XLY', 'XLP', 'SOXS', 'SOXL', 'TSLL', 'DIA', 'XLE', 'XLF', 
    # 'SKYY', 'CIBR', 'TEM', 'QYLD', 'BOTZ', 'CONL', 'NVDL', 'XLV', 'DBA', 'UUP', 
    # 'QQQM', 'PDBC', 'PGX', 'SPHD', 'SPLV', 'SGOV', 'SHY', 'TLT', 'IEF', 'IBIT', 
    # 'FXI', 'AOR', 'HDV', 'ICLN', 'HYG', 'LQD', 'IGOV', 'EMB', 'MBB', 'ACWI', 
    # 'EWZ', 'MCHI', 'EIDO', 'EWY', 'IWM', 'SOXX', 'SLV', 'JPIN', 'JEPQ', 'KWEB', 
    # 'XLB', 'FNGU', 'QQQ', 'BITO', 'TQQQ', 'SQQQ', 'SPY', 'SCHD', 'GLD', 'XBI', 
    # 'XLK', 'MSTU', 'USO', 'XLU', 'GDX', 'SMH', 'VIG', 'VWO', 'VNQI', 'VYM', 
    # 'VGT', 'VCIT', 'VNQ', 'VCSH', 'VTIP', 'VEA', 'BND', 'BNDX', 'VXUS', 'VTI', 'VTV'


SAVE_FOLDER = "logos_etf3" # Pakai folder baru biar aman buat test
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# 2. Setup Selenium (Tetap sama seperti punyamu)
options = Options()
options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
options.add_argument("--profile-directory=Default")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features=AutomationControlled")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30) 
except Exception as e:
    print(f"Gagal buka browser: {e}")
    exit()

# --- FUNGSI BARU: MAGIC WRAPPER ---
def save_as_svg_wrapper(img_content, ticker):
    """Membungkus PNG ke dalam file SVG agar dashboard tidak perlu ganti kode."""
    try:
        img = Image.open(io.BytesIO(img_content))
        width, height = img.size
        # Encode ke base64
        base64_data = base64.b64encode(img_content).decode('utf-8')
        
        # Template SVG (Bingkai transparan)
        svg_template = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image width="{width}" height="{height}" xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
        
        file_path = os.path.join(SAVE_FOLDER, f"{ticker}.svg")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(svg_template)
        return True
    except Exception as e:
        print(f"Gagal wrapping {ticker}: {e}")
        return False

def download_logo(ticker):
    url = f"https://musaffa.com/etf/{ticker}"
    try:
        driver.get(url)
        time.sleep(5) # ETF butuh waktu agak lama buat narik logo dari Finnhub

        # --- UPDATE SELECTOR ---
        # Untuk ETF, selectornya 'img.stock-image' sesuai hasil inspect tadi
        try:
            logo_element = driver.find_element(By.CSS_SELECTOR, "img.stock-image")
            img_url = logo_element.get_attribute("src")
        except:
            img_url = None

        # --- LOGIKA DOWNLOAD & CONVERT ---
        if img_url and ("finnhub" in img_url or ".png" in img_url or ".svg" in img_url):
            headers = {"User-Agent": driver.execute_script("return navigator.userAgent;")}
            response = requests.get(img_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Cek jika ternyata dapetnya SVG asli (langsung simpan)
                if ".svg" in img_url:
                    file_path = os.path.join(SAVE_FOLDER, f"{ticker}.svg")
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"[SUCCESS] {ticker} downloaded as Native SVG")
                
                # Jika dapetnya PNG (lakukan Magic Wrapper)
                else:
                    if save_as_svg_wrapper(response.content, ticker):
                        print(f"[MAGIC] {ticker} wrapped into SVG successfully")
            else:
                print(f"[FAILED] {ticker} - Status {response.status_code}")
        else:
            print(f"[NOT FOUND] {ticker} - Logo Finnhub tidak muncul")

    except Exception as e:
        print(f"[ERROR] {ticker} - {str(e)}")

# 3. Looping
print(f"Starting ETF download for {len(US_TICKERS)} tickers...")
for ticker in US_TICKERS:
    download_logo(ticker)
    time.sleep(2)

driver.quit()
print("Selesai, bro! Cek folder logos_etf ya.")