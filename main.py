import asyncio
import logging
import os
#for concurrent requests
#for concurrent requests
import aiohttp
#for updating order.json file
import json
#for loading environment variables
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

#Load environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not set")

#loads the json file containing the orders
def load_orders():
    with open("order.json", "r") as f:
        orders = json.load(f)

    return [order["city"] for order in orders]

#writing apology message
def apology(customer, city, weather_main):
    weather_reason = {
        "Snow": "snow",
        "Rain": "Heavy rain",
        "Extreme": "extreme weather",
    }.get(weather_main, "severe_weather")

    return (
        f"Hi {customer}, your order to {city} is delayed due to "
        f"{weather_reason}. We appreciate your interest"
    )

async def fetch_weather(session, order):
    city = order["city"]
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY
    }

    try:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                error_text = await response.json()

                logging.error(
                    "Weather API failed for %s: HTTP %s - %s",
                    city,
                    response.status,
                    error_text
                )

                return {
                    "order": order,
                    "weather": None,
                    "error": f"HTTP {response.status}"
                }

            data = await response.json()

            return {
                "order": order,
                "weather": data,
                "error": None
            }
    except Exception as error:
        logging.error(
            "Unexpected error while fetching weather for %s: %s",
            city,
            error,
        )

        return {
            "order": order,
            "weather": None,
            "error": str(error)
        }

#process orders
async def process_orders():
    with open("order.json", "r", encoding="utf-8") as file:
        orders = json.load(file)

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *(fetch_weather(session, order) for order in orders)
        )

    for result in results:
        order = result["order"]
        weather = result["weather"]

        if weather is None:
            continue

        weather_main = weather["weather"][0]["main"]

        logging.info(
            "%s - %s",
            order["city"],
            weather_main
        )

        if weather_main in {"Rain", "Snow", "Extreme"}:

            order["status"] = "Delayed"

            order["apology"] = apology(
                order["customer"],
                order["city"],
                weather_main
            )

        else:
            order["status"] = "Pending"

            order.pop("apology", None)

    with open("order.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)

if __name__ == "__main__":
    asyncio.run(process_orders())
