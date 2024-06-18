import aiohttp
import asyncio
import json
import websockets
from aiofile import AIOFile, Writer
from aiopath import AsyncPath
from datetime import datetime, timedelta


API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"


async def fetch_rate_for_date(
    session: aiohttp.ClientSession, date: str, currencies: list[str]
) -> dict[str, dict[str, dict[str, float]]]:
    try:
        async with session.get(API_URL.format(date=date)) as response:
            data = await response.json()
            rates = {currency: {} for currency in currencies}
            for rate in data.get("exchangeRate", []):
                if rate["currency"] in rates:
                    rates[rate["currency"]] = {
                        "sale": rate.get("saleRate"),
                        "purchase": rate.get("purchaseRate"),
                    }
            return {date: rates}
    except Exception as e:
        print(f"Error fetching data for {date}: {e}")
        return {}


async def fetch_rates(
    days: int, currencies: list[str]
) -> list[dict[str, dict[str, dict[str, float]]]]:
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_rate_for_date(
                session,
                (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y"),
                currencies,
            )
            for i in range(days)
        ]
        return await asyncio.gather(*tasks)


async def log_command(command: str) -> None:
    log_path = AsyncPath("command.log")
    async with AIOFile(log_path, "a") as afp:
        writer = Writer(afp)
        await writer(f"{datetime.now()}: {command}\n")


async def handle_exchange(
    days: int, currencies: list[str]
) -> list[dict[str, dict[str, dict[str, float]]]]:
    rates = await fetch_rates(days, currencies)
    await log_command(f"exchange {days} {' '.join(currencies)}")
    return rates


async def handler(websocket, path) -> None:
    async for message in websocket:
        if message.startswith("exchange"):
            args = message.split()
            days = int(args[1]) if len(args) > 1 else 1
            currencies = args[2:] if len(args) > 2 else ["EUR", "USD"]
            rates = await handle_exchange(days, currencies)
            await websocket.send(json.dumps(rates, indent=2))
        else:
            await websocket.send(f"Received: {message}")


start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
