import os
import aiohttp
import asyncio
from telegram import Bot

# CONFIG
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

CONTRACT_ADDRESS = "0x68b2BfB227BE9C3540f9e9084c768821e336C64d"
API_URL = "https://api.etherscan.io/api"
GIF_URL = "https://pandabao.org/wp-content/uploads/2025/04/Untitled-design-3.gif"

# VALIDĂRI
if not TELEGRAM_TOKEN:
    raise ValueError("⚠️ TELEGRAM_TOKEN is missing!")
if not CHAT_ID:
    raise ValueError("⚠️ CHAT_ID is missing!")
if not ETHERSCAN_API_KEY:
    raise ValueError("⚠️ ETHERSCAN_API_KEY is missing!")

bot = Bot(token=TELEGRAM_TOKEN)

async def check_transactions():
    last_tx = None

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={ETHERSCAN_API_KEY}"
                ) as response:
                    data = await response.json()

            if data.get("status") == "1" and "result" in data:
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]
                    amount_eth = int(latest_tx["value"]) / 10**18

                    message = (
                        "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥\n"
                        "🥇The Future of DeFi is GOLD! Get in NOW!\n"
                        "⚡🔥 New Buy On PinkSale 🔥⚡\n\n"
                        f"💰 Amount: {amount_eth:.4f} ETH \n"
                        f"🔗 [Check the transaction on Etherscan 🧐](https://etherscan.io/tx/{last_tx})\n"
                    )

                    await bot.send_animation(chat_id=CHAT_ID, animation=GIF_URL, caption=message, parse_mode="Markdown")
                    print(f"✅ Sent GIF with transaction {last_tx}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(check_transactions())
