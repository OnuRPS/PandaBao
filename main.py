import os
import aiohttp
import asyncio
from telegram import Bot

# Configurări din environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
GIF_URL = os.getenv("GIF_URL")  # Optional

CONTRACT_ADDRESS = "0x36721B2A5829768de3D79B5a9A1780652BC25cb2"
API_URL = "https://api.etherscan.io/api"

# Verificare config
if not TELEGRAM_TOKEN:
    raise ValueError("⚠️ TELEGRAM_TOKEN is missing!")
if not CHAT_ID:
    raise ValueError("⚠️ CHAT_ID is missing!")
if not ETHERSCAN_API_KEY:
    raise ValueError("⚠️ ETHERSCAN_API_KEY is missing!")

# Inițializare bot
bot = Bot(token=TELEGRAM_TOKEN)

async def check_transactions():
    print("✅ Bot is running and watching the address...")
    last_tx = ""
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={ETHERSCAN_API_KEY}"
                async with session.get(url) as response:
                    data = await response.json()

            if data.get("status") == "1" and data.get("result"):
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]
                    amount = int(latest_tx["value"]) / 10**18
                    from_address = latest_tx["from"]
                    to_address = latest_tx["to"]

                    message = (
                        "🪙 *New $GOV movement detected!*\n\n"
                        f"🔁 From: `{from_address}`\n"
                        f"📥 To: `{to_address}`\n"
                        f"💰 Amount: {amount:.4f} ETH\n"
                        f"🔗 [View on Etherscan](https://etherscan.io/tx/{last_tx})\n\n"
                        "⚱️ Powered by *Chrysus* \n"
                        "🌐 https://chrysus.org"
                        "🌐 https://www.pinksale.finance/launchpad/ethereum/0x36721B2A5829768de3D79B5a9A1780652BC25cb2?refId=0x68b2bfb227be9c3540f9e9084c768821e336c64d"
                        "\n\n🤖 *BuyDetector* by [ReactLAB](https://pandabao.org/) — crafted for precision and performance."
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
