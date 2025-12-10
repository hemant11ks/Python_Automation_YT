# ---------------------------------------------------------
# Python Weather CLI Tool using OpenWeatherMap API
# Concepts:
# - HTTP GET request using requests
# - API endpoint, query parameters, API key
# - JSON response handling
# - Error handling (city not found, invalid key)
# ---------------------------------------------------------
from dotenv import load_dotenv
import requests  # Third-party library to make HTTP requests
import os

# 1. CONSTANTS / CONFIGURATION
#    (These can be changed easily later)
load_dotenv()
#API_KEY = "492b59152ded581d626e8c62f8e3dc20"  # <-- Put your OpenWeatherMap API key here
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

API_KEY = os.getenv("API_KEY")


def get_weather(city_name: str):
    """
    Fetch weather information for a given city
    using OpenWeatherMap API.

    :param city_name: Name of the city (string)
    :return: dict with weather info OR dict with error
    """

    # 2. Build the request URL with query parameters
    #    q       -> city name
    #    appid   -> API key
    #    units   -> metric means temperature in Celsius
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    # 3. Send GET request
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        # Any network-related error (no internet, timeout, DNS, etc.)
        return {"error": f"Network error: {e}"}

    # 4. Check HTTP status code
    if response.status_code != 200:
        # Convert response to JSON to see error message if available
        try:
            error_data = response.json()
            message = error_data.get("message", "Unknown error")
        except ValueError:
            message = "Invalid response from server"

        # Handle common failure cases
        if response.status_code == 401:
            return {"error": f"Invalid API key: {message}"}
        elif response.status_code == 404:
            return {"error": f"City not found: {city_name}"}
        else:
            return {"error": f"API request failed with status {response.status_code}: {message}"}

    # 5. Parse JSON data on success
    try:
        data = response.json()
    except ValueError:
        return {"error": "Failed to decode JSON response"}

    # 6. Extract useful fields safely
    main = data.get("main", {})
    weather_list = data.get("weather", [])
    wind = data.get("wind", {})

    temperature = main.get("temp")
    pressure = main.get("pressure")
    humidity = main.get("humidity")
    description = weather_list[0].get("description") if weather_list else None
    wind_speed = wind.get("speed")

    # 7. Build a clean result dictionary
    return {
        "city": data.get("name", city_name),
        "temperature": temperature,
        "pressure": pressure,
        "humidity": humidity,
        "description": description,
        "wind_speed": wind_speed
    }


def print_weather_report(result: dict):
    """
    Nicely print the weather details or error message.
    """
    if "error" in result:
        print("\n❌ Error:", result["error"])
        return

    print("\n📍 Weather Report for:", result["city"])
    print("--------------------------------------")
    print(f"🌡 Temperature : {result['temperature']} °C")
    print(f"💧 Humidity    : {result['humidity']} %")
    print(f"🔽 Pressure    : {result['pressure']} hPa")
    print(f"🌬 Wind Speed  : {result['wind_speed']} m/s")
    print(f"🌦 Condition   : {result['description']}")


if __name__ == "__main__":
    # 8. Take input from user (real use case)
    city = input("Enter city name: ").strip()

    if not city:
        print("Please enter a valid city name.")
    else:
        weather_data = get_weather(city)
        print_weather_report(weather_data)
