import os

# Konfigurasi
SAVE_FOLDER = "logos_etf"
OUTPUT_FILE = "audit_gallery_etf.html"

# Ambil semua file .svg di folder logos
if not os.path.exists(SAVE_FOLDER):
    print(f"Error: Folder '{SAVE_FOLDER}' gak ketemu, bro!")
    exit()

logos = [f for f in os.listdir(SAVE_FOLDER) if f.endswith('.svg')]
logos.sort() # Biar rapi sesuai abjad ticker

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quant Radar - Logo Audit</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .header {{ position: sticky; top: 0; background: #1e293b; padding: 20px; border-radius: 12px; z-index: 100; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
        h1 {{ margin: 0; font-size: 24px; color: #38bdf8; }}
        .stats {{ font-weight: bold; color: #94a3b8; }}
        
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 15px; }}
        .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; text-align: center; transition: transform 0.2s, border-color 0.2s; cursor: pointer; }}
        .card:hover {{ transform: translateY(-3px); border-color: #38bdf8; background: #232f45; }}
        
        /* Container logo: Background putih biar SVG transparan kelihatan jelas */
        .img-wrapper {{ background: #ffffff; border-radius: 6px; padding: 8px; margin-bottom: 8px; display: flex; align-items: center; justify-content: center; height: 60px; }}
        .card img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
        
        .ticker {{ font-size: 13px; font-weight: 700; letter-spacing: 0.5px; color: #cbd5e1; }}
        .error-hint {{ color: #ef4444; font-size: 10px; margin-top: 4px; display: none; }}
        
        /* Jika gambar gagal load (Broken Link) */
        img:error {{ content: url('https://via.placeholder.com/60?text=ERR'); }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Quant Radar: Logo Audit</h1>
            <div class="stats">Total Terkumpul: {len(logos)} Logos</div>
        </div>
        <div style="font-size: 12px; color: #64748b;">Tips: Klik kartu untuk copy ticker</div>
    </div>

    <div class="grid">
"""

for logo in logos:
    ticker = logo.replace('.svg', '')
    img_path = f"{SAVE_FOLDER}/{logo}"
    
    html_content += f"""
        <div class="card" onclick="copyToClipboard('{ticker}')">
            <div class="img-wrapper">
                <img src="{img_path}" loading="lazy" onerror="this.parentElement.style.border='2px solid #ef4444';">
            </div>
            <span class="ticker">{ticker}</span>
        </div>
    """

html_content += """
    </div>

    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text);
            console.log('Copied:', text);
            // Alert kecil simpel
            const notification = document.createElement('div');
            notification.innerText = 'Copied: ' + text;
            notification.style.position = 'fixed';
            notification.style.bottom = '20px';
            notification.style.right = '20px';
            notification.style.background = '#38bdf8';
            notification.style.padding = '10px 20px';
            notification.style.borderRadius = '5px';
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 2000);
        }
    </script>
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"🔥 Selesai, bro! File '{OUTPUT_FILE}' sudah siap diintip.")