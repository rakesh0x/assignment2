assignment 2 - weather based order updater

hey, this is my assignment submission for the async order processing task.

what i was asked to do
- read orders from a json file
- fetch live weather for each city using an api
- do it concurrently with asyncio, not one by one
- if weather is bad (rain, snow, extreme), mark the order as delayed and add an apology message
- handle api errors properly without crashing

how i did it
- used asyncio + aiohttp so all the weather calls run at the same time with asyncio.gather
- used openweathermap api for live weather data
- read and updated everything in order.json
- used logging to show what is happening for each city
- wrapped the api call in try / except so one bad city doesnt stop the rest

files submitted
- main.py -> my full solution
- order.json -> input orders + updated output with status and apology
- .env -> has my openweather_api_key (not uploaded to github)
- readme.md -> this file

how to run my code
1. clone my repo
2. create a .env file with:
   openweather_api_key=your_key_here
3. install dependencies:
   pip install aiohttp python-dotenv
4. run:
   python3 main.py

sample logic
- if weather is clear or clouds -> status = pending, no apology
- if weather is rain / snow / extreme -> status = delayed, plus a message like:
  hi bob jones, your order to mumbai is delayed due to heavy rain. we appreciate your interest

error handling i added
- if api returns non-200, i log the http error and skip that order
- if city is invalid, i log it and continue with other orders
- if api key is missing, i raise a clear error at startup

thats it. thanks for checking my assignment.
