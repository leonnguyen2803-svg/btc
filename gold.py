import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://ngoctham.com/bang-gia-vang/"

headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(URL, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table tr")

gold_price = None

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 3:
        loai = cols[0].get_text(strip=True)
        gia_ban = cols[2].get_text(strip=True)

        if "Nhẫn 999.9" in loai:
            gold_price = gia_ban
            break

embed = {
    "title": "💰 GOLD DASHBOARD",
    "color": 0xF1C40F,
    "fields": [
        {"name": "Loại vàng", "value": "Nhẫn 999.9", "inline": True},
        {"name": "Giá bán", "value": gold_price or "Không lấy được", "inline": True}
    ]
}

requests.post(WEBHOOK, json={"embeds": [embed]})

print("DONE")
