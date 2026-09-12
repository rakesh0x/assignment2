hey, so this is my little weather + orders thing

basically i had this problem where orders kept getting delayed because of bad weather, and nobody told the customers anything. so i built this small script that checks the weather for each order city and updates stuff on its own.

what it does
- reads all the orders from order.json
- hits the openweather api for every city, all at once (asyncio + aiohttp so its fast)
- if its raining, snowing, or something extreme, it marks that order as delayed
- it also writes a small apology message for the customer, like hey your order is late because of heavy rain, that kind of thing
- if the weather is fine, it just keeps the order as pending and removes any old apology
- logs everything so you can see what happened

files in here
- main.py -> all the logic lives here
- order.json -> your orders list, this is what gets updated
- .env -> this is where your api key goes (not pushed to github)

how to run it
1. clone this repo
2. make a .env file and add your key like this:
   openweather_api_key=your_key_here
   you can get one for free from openweathermap.org
3. install what you need:
   pip install aiohttp python-dotenv
4. add your orders to order.json, something like:
   [
     {
       "order_id": "1001",
       "customer": "alice smith",
       "city": "new york",
       "status": "pending"
     }
   ]
5. just run it:
   python3 main.py

what an order looks like after
- good weather:
  status stays pending, no apology
- bad weather:
  status becomes delayed, and you get something like:
  hi bob jones, your order to mumbai is delayed due to heavy rain. we appreciate your interest

a quick note
- if a city name is wrong or the api fails, it just logs the error and moves on, it wont crash the whole thing
- be nice with the free api tier, dont spam it too much

thats pretty much it. small script, does one job, saves a lot of manual checking.
