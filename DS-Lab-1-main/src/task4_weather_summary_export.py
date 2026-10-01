import csv
from typing import Any, Dict, List, TextIO, Union

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def summarize_weather_data(data: List[Dict[str, Any]]) -> Dict[str, Union[float, int]]:
    """Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary containing average temperatures, total precipitation,
              average wind speed, average humidity, and counts of hot, windy, and rainy days.
    """
    if not data:
        return {
            "average_max_temp": 0.0,
            "average_min_temp": 0.0,
            "total_precipitation": 0.0,
            "average_wind_speed": 0.0,
            "average_humidity": 0.0,
            "hot_days": 0,
            "windy_days": 0,
            "rainy_days": 0,
        }

    total_max_temp = 0.0
    total_min_temp = 0.0
    total_precipitation = 0.0
    total_wind_speed = 0.0
    total_humidity = 0.0

    hot_days = 0
    windy_days = 0
    rainy_days = 0

    count = len(data)

    for day in data:
        max_temp = float(day.get("max_temperature", day.get("max_temp", 0)))
        min_temp = float(day.get("min_temperature", day.get("min_temp", 0)))
        precip = float(day.get("precipitation", 0))
        wind = float(day.get("wind_speed", 0))
        humidity = float(day.get("humidity", 0))

        total_max_temp += max_temp
        total_min_temp += min_temp
        total_precipitation += precip
        total_wind_speed += wind
        total_humidity += humidity

        if max_temp > 30:
            hot_days += 1
        if wind > 15:
            windy_days += 1
        if precip > 0:
            rainy_days += 1

    return {
        "average_max_temp": round(total_max_temp / count, 2),
        "average_min_temp": round(total_min_temp / count, 2),
        "total_precipitation": round(total_precipitation, 2),
        "average_wind_speed": round(total_wind_speed / count, 2),
        "average_humidity": round(total_humidity / count, 2),
        "hot_days": hot_days,
        "windy_days": windy_days,
        "rainy_days": rainy_days,
    }


def export_to_csv(data: List[Dict[str, Any]], file: Union[str, TextIO]) -> None:
    """Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): File path or buffer to write CSV data into.

    Raises:
        IOError: If writing to the file or stream fails.
    """
    headers = [
        "Date",
        "Max Temperature",
        "Min Temperature",
        "Precipitation",
        "Wind Speed",
        "Humidity",
        "Weather Description",
        "Is Hot Day",
        "Is Windy Day",
        "Is Rainy Day",
    ]

    def write_data(writer: csv.DictWriter) -> None:
        writer.writeheader()
        for day in data:
            max_temp = float(day.get("max_temperature", day.get("max_temp", 0)))
            min_temp = float(day.get("min_temperature", day.get("min_temp", 0)))
            wind_speed = float(day.get("wind_speed", 0))
            precipitation = float(day.get("precipitation", 0))

            is_hot = day.get("is_hot_day", day.get("is_hot", max_temp > 30))
            is_windy = day.get("is_windy_day", day.get("is_windy", wind_speed > 15))
            is_rainy = day.get("is_rainy_day", day.get("is_rainy", precipitation > 0))

            writer.writerow({
                "Date": day.get("date", ""),
                "Max Temperature": max_temp,
                "Min Temperature": min_temp,
                "Precipitation": precipitation,
                "Wind Speed": wind_speed,
                "Humidity": day.get("humidity", 0),
                "Weather Description": day.get("weather_description", day.get("weather", "")),
                "Is Hot Day": is_hot,
                "Is Windy Day": is_windy,
                "Is Rainy Day": is_rainy,
            })

    try:
        if isinstance(file, str):
            with open(file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                write_data(writer)
        else:
            writer = csv.DictWriter(file, fieldnames=headers)
            write_data(writer)
    except Exception as e:
        raise IOError(f"Failed to export weather data to CSV: {e}") from e


if __name__ == "__main__":
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        summary = summarize_weather_data(weather_data["daily"])

        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        export_to_csv(weather_data["daily"], "tokyo_weather_summary.csv")
        print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        print(f"An error occurred: {e}")