import requests
import json

API_KEY = "bbd120002d548472350865cd278bb369"
CITY_NAME = input("Enter city name: ")   # <-- take input from user
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
url = f"{BASE_URL}?q={CITY_NAME}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    temp = data["main"]["temp"]
    weather_description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    print(f"\nWeather in {CITY_NAME.capitalize()}:")
    print(f"  Temperature: {temp}°C")
    print(f"  Description: {weather_description}")
    print(f"  Humidity: {humidity}%")
    print(f"  Wind Speed: {wind_speed} m/s")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except (KeyError, IndexError) as e:
    print(f"Error parsing weather data: {e}")
