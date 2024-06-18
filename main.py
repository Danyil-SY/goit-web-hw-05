import aiohttp
import argparse
import asyncio
import sys
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


async def main(days: int, currencies: list[str]):
    rates = await fetch_rates(days, currencies)
    print(rates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch currency rates from PrivatBank")
    parser.add_argument(
        "days", type=int, help="Number of days to fetch rates for (up to 10)"
    )
    parser.add_argument(
        "--currencies",
        type=str,
        nargs="+",
        default=["EUR", "USD"],
        help="List of currencies to fetch rates for",
    )

    args = parser.parse_args()

    if args.days > 10:
        print("You can only fetch rates for the last 10 days.")
        sys.exit(1)

    asyncio.run(main(args.days, args.currencies))
