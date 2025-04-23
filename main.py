import os
import aiohttp
import asyncio
from telegram import Bot

# Config din .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
GIF_URL = os.getenv("GIF_URL")

CONTRACT_ADDRESS = "0x36721B2A5829768de3D79B5a9A1780652BC25cb2"
API_URL = "https://api.etherscan.io/api"
ETH_PRICE_API = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
ETH_BALANCE_API = f"{API_URL}?module=account&action=balance&address={CONTRACT_ADDRESS}&tag=latest"

# Verificare .env
if not TELEGRAM_TOKEN or not CHAT_ID or not ETHERSCAN_API_KEY:
    raise ValueError("⚠️ Configurare lipsă în variabilele de mediu!")

# Inițializare bot
bot = Bot(token=TELEGRAM_TOKEN)

def generate_bullets(amount_eth):
    bullets_count = int((amount_eth / 0.01))
    bullets_count = min(bullets_count, 100)
    return '🥇' * bullets_count

async def get_eth_price():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ETH_PRICE_API) as response:
                data = await response.json()
                return float(data["ethereum"]["usd"])
    except:
        return 0.0

async def get_eth_balance():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ETH_BALANCE_API}&apikey={ETHERSCAN_API_KEY}") as response:
                data = await response.json()
                if data["status"] == "1":
                    balance = int(data["result"]) / 1e18
                    return balance
    except:
        pass
    return 0.0

async def check_transactions():
    print("✅ BuyDetector™ is live.")
    last_tx = ""
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                tx_url = f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={ETHERSCAN_API_KEY}"
                async with session.get(tx_url) as response:
                    data = await response.json()

            if data.get("status") == "1" and data.get("result"):
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]
                    amount_eth = int(latest_tx["value"]) / 1e18
                    from_address = latest_tx["from"]
                    to_address = latest_tx["to"]

                    bullets = generate_bullets(amount_eth)
                    eth_price = await get_eth_price()
                    usd_value = amount_eth * eth_price
                    eth_balance = await get_eth_balance()
                    eth_balance_usd = eth_balance * eth_price

                    message = (
                        f"🪙 *New $GOV movement detected!*\n\n"
                        f"🔁 From: `{from_address}`\n"
                        f"📥 To: `{to_address}`\n"
                        f"🟨 *Amount Purchased:*\n"
f"┌────────────────────────────┐\n"
f"│  {amount_eth:.4f} ETH (~${usd_value:,.2f})  │\n"
f"└────────────────────────────┘\n"
                        f"{bullets}\n\n"
                        f"🟦 *Total Raised:*\n"
f"╭────────────────────────────╮\n"
f"│  {eth_balance:.4f} ETH (~${eth_balance_usd:,.2f})  │\n"
f"╰────────────────────────────╯\n"

                        f"🔗 [View on Etherscan](https://etherscan.io/tx/{last_tx})\n\n"
                        f"⚱️ Powered by *Chrysus*\n"
                        f"🌐 https://chrysus.org\n"
                        f"🌐 https://www.pinksale.finance/launchpad/ethereum/0x36721B2A5829768de3D79B5a9A1780652BC25cb2?refId=0x68b2bfb227be9c3540f9e9084c768821e336c64d\n\n"
                        f"───────────────\n"
                        f"🤖 𝓑𝓾𝔂𝓓𝓮𝓽𝓮𝓬𝓽𝓸𝓻™\n"
                        f"🔧 𝒃𝒚 [𝑹𝒆𝒂𝒄𝒕𝑳𝑨𝑩](https://pandabao.org/)\n"
                        f"───────────────"
                    )

                    if GIF_URL:
                        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_URL, caption=message, parse_mode="Markdown")
                    else:
                        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

                    print(f"✅ New TX posted: {last_tx}")

        except Exception as e:
            print(f"⚠️ Error: {e}")
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(check_transactions())
