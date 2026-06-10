import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# ================= BTC USD =================
btc_api = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
btc_usd = requests.get(btc_api).json()["bitcoin"]["usd"]

# ================= VND RATE (stable fallback) =================
# dùng rate cố định ổn định (tránh scrape lỗi Remitano)
vnd_rate = 25000
btc_vnd = btc_usd * vnd_rate

# ================= GOLD =================
gold_url = "https://ngoctham.com/bang-gia-vang/"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(gold_url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table tr")

gold_price = None

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 3:
        name = cols[0].get_text(strip=True)
        price = cols[2].get_text(strip=True)

        if "Nhẫn 999.9" in name:
            gold_price = price
            break

# ================= DISCORD EMBED =================
embed = {
    "title": "📊 MARKET DASHBOARD",
    "color": 0x3498db,
    "fields": [
        {
            "name": "₿ BTC (USD)",
            "value": f"${btc_usd:,.2f}",
            "inline": True
        },
        {
            "name": "₿ BTC (VND)",
            "value": f"{btc_vnd:,.0f} VND",
            "inline": True
        },
        {
            "name": "🥇 Gold (Nhẫn 999.9)",
            "value": gold_price or "N/A",
            "inline": False
        }
    ]
}

requests.post(
    WEBHOOK,
    json={"embeds": [embed]}
)

print("DONE")
