import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
import sys


class PrivatBankAPI:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/exchange_rates?"

    async def get_exchange_rate(self, date: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}json&date={date}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None


async def fetch_exhange_rates(days: int):
    api = PrivatBankAPI()
    today = datetime.now()
    results = []

    for i in range(1, days + 1):
        date = (today - timedelta(days=i)).strftime("%d.%m.%Y")
        exchange_rate = await api.get_exchange_rate(date)
        eur_data = exchange_rate[0][date]["exchangeRate"][8]
        usd_data = exchange_rate[0][date]["exchangeRate"][23]

        results.append(
            {
                date: {
                    "EUR": {
                        "sale": eur_data.get("saleRateNB", ""),
                        "purchase": eur_data.get("purchaseRateNB", ""),
                    },
                    "USD": {
                        "sale": usd_data.get("saleRateNB", ""),
                        "purchase": usd_data.get("purchaseRateNB", ""),
                    },
                }
            }
        )

    return results


async def main(days: int):
    exchange_rates = await fetch_exhange_rates(days)
    print(json.dumps(exchange_rates, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <number_of_days")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        if days <= 0 or days > 10:
            raise ValueError
    except ValueError:
        print("Number of days msut be an integer between 1 and 10")
        sys.exit(1)

    asyncio.run(main(days))
