# Exercise 2 - Currency dashboard
#
# Fetch https://open.er-api.com/v6/latest/USD once, then print a small table
# showing how many XAF you get for 1 USD, 1 EUR, and 1 GBP.
#
# Hint: the response's "rates" dict has one entry per currency, all relative
# to USD (e.g. rates["EUR"] tells you how many EUR equal 1 USD). To convert
# "how many XAF per EUR", divide rates["XAF"] by rates["EUR"].
#
# Expected output shape:
#   1 USD = 610.5 XAF
#   1 EUR = 655.2 XAF
#   1 GBP = 765.9 XAF
#
# Run: python3 exercises/02_currency_dashboard.py

import asyncio
import httpx

async def currency_dashboard():
    # TODO: your code here - follow the same try/except shape as 01_get_rate.py
    pass

asyncio.run(currency_dashboard())
