# Exercise 1 - Get the USD -> XAF exchange rate (SOLVED - worked together in the
# session, see LESSON.md)
#
# Install first (with your venv activated): pip install httpx
# Run: python3 exercises/01_get_rate.py

import asyncio
import httpx

async def get_usd_to_xaf_rate():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            rate = data["rates"]["XAF"]
            print(f"1 USD = {rate} XAF")
    except httpx.RequestError:
        print("Network problem - could not reach the exchange rate service.")
    except httpx.HTTPStatusError as error:
        print(f"Exchange rate service returned an error: {error.response.status_code}")

asyncio.run(get_usd_to_xaf_rate())
