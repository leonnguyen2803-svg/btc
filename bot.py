import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
headers = {"User-Agent": "Mozilla/5.0"}

# ================= BTC =================
btc_usd = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
    timeout=10
).json()["bitcoin"]["usd"]

# 🔥 FIX CHUẨN: lấy tỷ giá USD/VND thật từ API
usd_vnd = requests.get(
    "https://open.er-api.com/v6/latest/USD",
    timeout=10
).json()["rates"]["VND"]

btc_vnd = btc_usd * usd_vnd

# ================= INPUT =================
btc_buy_usd = 63200
btc_invest_vnd = 100_000_000

gold_qty = 20
gold_buy_per_chi = 17_300_000

# ================= BTC P/L =================
btc_amount = btc_invest_vnd / (btc_buy_usd * usd_vnd)

btc_value_now = btc_amount * btc_usd * usd_vnd

btc_profit_vnd = btc_value_now - btc_invest_vnd
btc_profit_pct = (btc_profit_vnd / btc_invest_vnd) * 100

# ================= GOLD =================
url = "https://ngoctham.com/bang-gia-vang/"
res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

gold_price = None

for row in soup.select("table tr"):
    cols = row.find_all("td")
    if len(cols) >= 3:
        if "Nhẫn 999.9" in cols[0].get_text(strip=True):
            gold_price = int(cols[2].get_text(strip=True).replace(".", "").replace(",", ""))
            break

gold_invest = gold_qty * gold_buy_per_chi

if gold_price:
    gold_value_now = gold_qty * gold_price
    gold_profit_vnd = gold_value_now - gold_invest
    gold_profit_pct = (gold_profit_vnd / gold_invest) * 100
else:
    gold_profit_vnd = 0
    gold_profit_pct = 0

# ================= OUTPUT =================
message = f"""BTC: {btc_usd:,.0f} USD
BTC: {btc_vnd:,.0f} VND
BTC P/L: {btc_profit_pct:+.2f}% ({btc_profit_vnd:+,.0f} VND)

Nhẫn vàng trơn 1 chỉ: {gold_price if gold_price else 'N/A'} VND
GOLD P/L: {gold_profit_pct:+.2f}% ({gold_profit_vnd:+,.0f} VND)
"""

requests.post(
    WEBHOOK,
    json={"content": message}
)

print("DONE")
