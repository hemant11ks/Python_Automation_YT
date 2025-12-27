# ---------------------------------------------------------
# Python Weather CLI Tool using OpenWeatherMap API
# ---------------------------------------------------------
# WHAT THIS SCRIPT DOES:
# 1. Takes a city name from the user
# 2. Sends an HTTP GET request to OpenWeatherMap API
# 3. Receives weather data in JSON format
# 4. Safely extracts required fields
# 5. Handles all possible errors
# 6. Displays a clean weather report in terminal
# ---------------------------------------------------------

#“In this video, we are going to build a real-world Python automation project using an external API.
#You will understand how APIs work, how Python communicates with servers, how JSON data is handled, and how to write production-ready error handling code.
#This video is beginner-friendly and also useful for interviews and backend concepts.”

# load_dotenv is used to load environment variables
# from a .env file into the system environment
from dotenv import load_dotenv

# requests is a third-party library used to send HTTP requests
import requests

# os is used to access environment variables securely
import os
# ---------------------------------------------------------
# CONFIGURATION / CONSTANTS
# ---------------------------------------------------------

# Load environment variables from .env file
# This allows us to keep API keys outside the code
load_dotenv()

# Base URL (API Endpoint)
# This is the server address where the request is sent
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Fetch API key securely from environment variables
# This avoids hard-coding sensitive information
API_KEY = os.getenv("API_KEY")


# ---------------------------------------------------------
# FUNCTION: FETCH WEATHER DATA
# ---------------------------------------------------------
def get_weather(city_name: str):
    """
    Fetch weather information for a given city.

    Parameters:
        city_name (str): Name of the city entered by user

    Returns:
        dict: Weather details OR error information
    """

    # ---------------------------------------------------------
    # STEP 1: BUILD QUERY PARAMETERS
    # ---------------------------------------------------------
    # These parameters are attached to the URL
    # ?q=Pune&appid=XXXX&units=metric
    params = {
        "q": city_name,      # City name
        "appid": API_KEY,    # API authentication key
        "units": "metric"    # Metric units → Celsius
    }


    # ---------------------------------------------------------
    # STEP 2: SEND HTTP GET REQUEST
    # ---------------------------------------------------------
    # try block is used because network calls can fail
    try:
        response = requests.get(
            BASE_URL,        # API endpoint
            params=params,   # Query parameters
            timeout=10       # Max wait time (seconds)
        )

    # This catches ALL request-related errors:
    # - No internet
    # - Timeout
    # - DNS failure
    # - Connection error
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Network error occurred: {e}"
        }


    # ---------------------------------------------------------
    # STEP 3: CHECK HTTP STATUS CODE
    # ---------------------------------------------------------
    # HTTP 200 means success
    if response.status_code != 200:

        # Try reading error message sent by server
        try:
            error_data = response.json()
            message = error_data.get("message", "Unknown error")
        except ValueError:
            # Happens if server response is not valid JSON
            message = "Invalid response from server"

        # Handle common HTTP errors
        if response.status_code == 401:
            return {"error": "Invalid API key"}
        elif response.status_code == 404:
            return {"error": f"City not found: {city_name}"}
        else:
            return {
                "error": f"HTTP {response.status_code}: {message}"
            }


    # ---------------------------------------------------------
    # STEP 4: PARSE JSON RESPONSE
    # ---------------------------------------------------------
    # Convert JSON → Python dictionary
    try:
        data = response.json()
    except ValueError:
        return {"error": "Failed to parse JSON response"}


    # ---------------------------------------------------------
    # STEP 5: SAFE DATA EXTRACTION (IMPORTANT CONCEPT)
    # ---------------------------------------------------------
    # WHY WE DO THIS:
    # - API responses can change
    # - Keys may be missing
    # - Accessing missing keys directly causes crashes

    # Extract "main" section safely
    # Example: data["main"] → {"temp": 30, "humidity": 60}
    main = data.get("main", {})

    # Extract "weather" list safely
    # Example: [{"description": "clear sky"}]
    weather = data.get("weather", [])

    # Extract "wind" section safely
    # Example: {"speed": 5.6}
    wind = data.get("wind", {})


    # ---------------------------------------------------------
    # STEP 6: BUILD CLEAN RESULT DICTIONARY
    # ---------------------------------------------------------
    return {
        # City name returned by API
        "city": data.get("name", city_name),

        # Temperature in Celsius
        "temperature": main.get("temp"),

        # Humidity percentage
        "humidity": main.get("humidity"),

        # Atmospheric pressure
        "pressure": main.get("pressure"),

        # Weather condition (first item from list)
        "condition": weather[0].get("description") if weather else None,

        # Wind speed
        "wind_speed": wind.get("speed")
    }


# ---------------------------------------------------------
# FUNCTION: DISPLAY WEATHER REPORT
# ---------------------------------------------------------
def print_weather_report(result: dict):
    """
    Prints formatted weather report or error message
    """

    # If API returned an error
    if "error" in result:
        print("\n❌ Error:", result["error"])
        return

    # Display clean formatted output
    print("\n📍 Weather Report for:", result["city"])
    print("--------------------------------------")
    print(f"🌡 Temperature : {result['temperature']} °C")
    print(f"💧 Humidity    : {result['humidity']} %")
    print(f"🔽 Pressure    : {result['pressure']} hPa")
    print(f"🌬 Wind Speed  : {result['wind_speed']} m/s")
    print(f"🌦 Condition   : {result['condition']}")


# ---------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":

    # Take city name from user
    city = input("Enter city name: ").strip()

    # Validate input
    if not city:
        print("Please enter a valid city name.")
    else:
        # Fetch weather data
        weather_data = get_weather(city)

        # Print result
        print_weather_report(weather_data)
