import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. Konfigurasi
# GANTI 'YourName' dengan username Windows/Mac kamu agar Selenium bisa pakai Profile Chrome asli
CHROME_PROFILE_PATH = r'C:\Users\ASUS\Downloads\piton\us_stocksscreener\User Data' 
US_TICKERS = [
    'BLOK', 'ARKK', 
    'XLY', 'XLP', 'SOXS', 'SOXL', 'TSLL', 'DIA', 'XLE', 'XLF', 'SKYY', 'CIBR', 
    'TEM', 'QYLD', 'BOTZ', 'CONL', 'NVDL', 'XLV', 'DBA', 'UUP', 'QQQM', 'PDBC', 
    'PGX', 'SPHD', 'SPLV', 'SGOV', 'SHY', 'TLT', 'IEF', 'IBIT', 'FXI', 'AOR', 
    'HDV', 'ICLN', 'HYG', 'LQD', 'IGOV', 'EMB', 'MBB', 'ACWI', 'EWZ', 'MCHI', 
    'EIDO', 'EWY', 'IWM', 'SOXX', 'SLV', 'JPIN', 'JEPQ', 'KWEB', 'XLB', 'FNGU', 
    'QQQ', 'BITO', 'TQQQ', 'SQQQ', 'SPY', 'SCHD', 'GLD', 'XBI', 'XLK', 'MSTU', 
    'USO', 'XLU', 'GDX', 'SMH', 'VIG', 'VWO', 'VNQI', 'VYM', 'VGT', 'VCIT', 
    'VNQ', 'VCSH', 'VTIP', 'VEA', 'BND', 'BNDX', 'VXUS', 'VTI', 'VTV'] # Tambahkan list lainnya

SAVE_FOLDER = "logos3"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# 2. Setup Selenium dengan argumen bypass
options = Options()
options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
options.add_argument("--profile-directory=Default")

# Argumen wajib biar nggak "bengong" dan kena blokir
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-allow-origins=*")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Tambahkan ini biar popup "Restore" atau "VPN" nggak menghalangi driver
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--restore-last-session") # Kadang membantu melewati dialog restore

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Set timeout agar tidak bengong selamanya jika page berat
    driver.set_page_load_timeout(30) 
except Exception as e:
    print(f"Gagal buka browser: {e}")
    exit()

# Script tambahan anti-bot
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

def download_logo(ticker):
    url = f"https://musaffa.com/etf/{ticker}"
    try:
        driver.get(url)
        # Tunggu sebentar sampai Angular selesai render datanya
        time.sleep(4) 

        # SELECTOR PRESISI: Cari img di dalam div class 'icon_name'
        # Ini akan menghindari bendera negara (us.svg) dan ikon mahkota
        try:
            logo_element = driver.find_element(By.CSS_SELECTOR, ".icon_name img")
            svg_url = logo_element.get_attribute("src")
        except:
            svg_url = None

        if svg_url and ".svg" in svg_url:
            # Download menggunakan requests
            headers = {"User-Agent": driver.execute_script("return navigator.userAgent;")}
            cookies = {c['name']: c['value'] for c in driver.get_cookies()}
            
            response = requests.get(svg_url, headers=headers, cookies=cookies, timeout=10)
            
            if response.status_code == 200:
                file_path = os.path.join(SAVE_FOLDER, f"{ticker}.svg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"[SUCCESS] {ticker} downloaded dari {svg_url}")
            else:
                print(f"[FAILED] {ticker} - Status Code {response.status_code}")
        else:
            print(f"[NOT FOUND] {ticker} - Logo tidak ditemukan di class icon_name")

    except Exception as e:
        print(f"[ERROR] {ticker} - {str(e)}")

# 3. Looping Santai (No Threading)
print(f"Starting download for {len(US_TICKERS)} tickers...")
for ticker in US_TICKERS:
    download_logo(ticker)
    time.sleep(2) # Jeda antar ticker supaya tidak dianggap bot agresif

driver.quit()
print("Selesai, bro!")