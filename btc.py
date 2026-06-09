import requests
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

response = requests.get(
"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
timeout=10
)

btc = response.json()["bitcoin"]["usd"]

message = f"""
🚀 BTC Hourly Report

💰 BTC Price: ${btc:,.2f}
"""

requests.post(
WEBHOOK,
json={
"content": message
},
timeout=10
)

print("Discord message sent.")
