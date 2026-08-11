# Exercise 3 - Weather checker
#
# Use the free, no-signup-required Open-Meteo API to print the current
# temperature for a city. Open-Meteo needs latitude/longitude rather than a
# city name, so this file gives you Buea, Cameroon's coordinates to start.
#
# API docs: https://open-meteo.com/en/docs
# Example URL:
#   https://api.open-meteo.com/v1/forecast?latitude=4.15&longitude=9.24&current_weather=true
#
# Expected output shape:
#   Current temperature: 24.3 C
#
# Run: python3 exercises/03_weather_checker.py

import asyncio
import httpx

LATITUDE = 4.15
LONGITUDE = 9.24

async def weather_checker():
    # TODO: your code here - follow the same try/except shape as 01_get_rate.py
    # The temperature is nested at data["current_weather"]["temperature"]
    pass

asyncio.run(weather_checker())
