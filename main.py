import os
import aiohttp
import asyncio
from telegram import Bot

# === Config ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
CONTRACT_ADDRESS = "0x68b2BfB227BE9C3540f9e9084c768821e336C64d"
API_URL = "https://api.etherscan.io/api"
GIF_URL = "https://pandabao.org/wp-content/uploads/2024/12/TelegramCumparari.gif"

# === Validări ===
if not TELEGRAM_TOKEN:
    raise ValueError("⚠️ TELEGRAM_TOKEN lipsește! Verifică variabilele de mediu.")
if not CHAT_ID:
    raise ValueError("⚠️ CHAT_ID lipsește! Verifică variabilele de mediu.")
if not ETHERSCAN_API_KEY:
    raise ValueError("⚠️ ETHERSCAN_API_KEY lipsește! Verifică variabilele de mediu.")

# === Bot ===
bot = Bot(token=TELEGRAM_TOKEN)

# === Check Transactions ===
async def check_transactions():
    last_tx = ""
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={ETHERSCAN_API_KEY}") as response:
                    data = await response.json()

            if data.get("status") == "1" and "result" in data:
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]
                    amount = int(latest_tx["value"]) / 10**18

                    message = (
                        "🐼 *New CHRYSUS Supporter on ETH!*\n\n"
                        f"💰 Amount: `{amount:.4f}` ETH\n"
                        "🔗 [View on Etherscan](https://etherscan.io/tx/" + last_tx + ")\n"
                        "\n🌟 Thank you for supporting Chrysus – The Gold-Pegged Stablecoin!"
                    )

                    await bot.send_animation(chat_id=CHAT_ID, animation=GIF_URL, caption=message, parse_mode="Markdown")

        except Exception as e:
            print(f"⚠️ Eroare: {e}")

        await asyncio.sleep(30)

# === Main ===
if __name__ == "__main__":
    asyncio.run(check_transactions())
