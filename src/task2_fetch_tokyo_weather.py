from typing import Any, Dict
import requests

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_weather_data() -> Dict[str, Any]:
    """Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature.

    Raises:
        requests.RequestException: If the HTTP request fails or times out.
        KeyError: If the expected weather data is missing in the API response.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
        "&daily=temperature_2m_max&timezone=Asia/Tokyo"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {e}") from e

    try:
        date = data["daily"]["time"][0]
        max_temp = float(data["daily"]["temperature_2m_max"][0])
    except (KeyError, IndexError, TypeError) as e:
        raise KeyError("Expected weather data missing in API response") from e

    return {
        "date": date,
        "max_temperature": max_temp
    }


if __name__ == "__main__":
    try:
        weather_data = fetch_weather_data()
        save_to_json(weather_data, "tokyo_weather.json")
        print("Data successfully saved to tokyo_weather.json")
    except Exception as e:
        print(f"An error occurred: {e}")