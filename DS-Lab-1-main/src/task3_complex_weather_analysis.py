from typing import Any, Dict, List

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(
    day: Dict[str, Any],
    temp_threshold: float = 30.0,
    wind_threshold: float = 15.0,
    humidity_threshold: float = 70.0,
) -> Dict[str, Any]:
    """Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    date = day.get("date", "")
    weather_desc = day.get("weather_description", day.get("weather", ""))

    max_temp = float(day.get("max_temperature", day.get("max_temp", 0.0)))
    min_temp = float(day.get("min_temperature", day.get("min_temp", 0.0)))
    wind_speed = float(day.get("wind_speed", 0.0))
    humidity = float(day.get("humidity", 0.0))
    precipitation = float(day.get("precipitation", 0.0))

    temp_swing = round(max_temp - min_temp, 1)
    is_hot_day = max_temp > temp_threshold
    is_windy_day = wind_speed > wind_threshold
    is_uncomfortable_day = humidity > humidity_threshold
    is_rainy_day = precipitation > 0.0
    significant_swing = temp_swing > 10.0

    return {
        "date": date,
        "weather_description": weather_desc,
        "max_temperature": max_temp,
        "min_temperature": min_temp,
        "temperature_swing": temp_swing,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "precipitation": precipitation,
        "is_hot_day": is_hot_day,
        "is_windy_day": is_windy_day,
        "is_uncomfortable_day": is_uncomfortable_day,
        "is_rainy_day": is_rainy_day,
        "significant_swing": significant_swing,
        # Додаткові ключі для зворотної сумісності
        "max_temp": max_temp,
        "min_temp": min_temp,
        "temp_swing": temp_swing,
        "is_hot": is_hot_day,
        "is_windy": is_windy_day,
        "is_uncomfortable": is_uncomfortable_day,
        "is_rainy": is_rainy_day,
    }


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A formatted multi-line string representing the daily report.
    """
    date = analysis.get("date", "")
    weather = analysis.get("weather_description", analysis.get("weather", ""))
    max_temp = float(analysis.get("max_temperature", analysis.get("max_temp", 0.0)))
    min_temp = float(analysis.get("min_temperature", analysis.get("min_temp", 0.0)))
    temp_swing = float(analysis.get("temperature_swing", analysis.get("temp_swing", 0.0)))

    lines = [
        f"Date: {date}",
        f"Weather: {weather}",
        f"Temperature: Max {max_temp:.1f}°C, Min {min_temp:.1f}°C (Swing: {temp_swing:.1f}°C)",
    ]

    is_hot = analysis.get("is_hot_day", analysis.get("is_hot", False))
    is_windy = analysis.get("is_windy_day", analysis.get("is_windy", False))
    is_uncomfortable = analysis.get("is_uncomfortable_day", analysis.get("is_uncomfortable", False))
    is_rainy = analysis.get("is_rainy_day", analysis.get("is_rainy", False))
    significant_swing = analysis.get("significant_swing", analysis.get("is_significant_swing", False))

    if is_hot:
        lines.append("It was a hot day.")
    if significant_swing:
        lines.append("There was a significant temperature swing.")
    if is_uncomfortable:
        lines.append("The humidity made the day uncomfortable.")
    if is_windy:
        lines.append("It was a windy day.")
    if is_rainy:
        lines.append("It was a rainy day.")
    else:
        lines.append("There was no precipitation.")

    return "\n".join(lines)


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report string containing peak values for temperature, wind, humidity, and rainfall.
    """
    if not analyses:
        return ""

    hottest = max(analyses, key=lambda x: float(x.get("max_temperature", x.get("max_temp", 0.0))))
    windiest = max(analyses, key=lambda x: float(x.get("wind_speed", 0.0)))
    most_humid = max(analyses, key=lambda x: float(x.get("humidity", 0.0)))
    rainiest = max(analyses, key=lambda x: float(x.get("precipitation", 0.0)))

    hottest_temp = float(hottest.get("max_temperature", hottest.get("max_temp", 0.0)))
    windiest_speed = float(windiest.get("wind_speed", 0.0))
    rainiest_precip = float(rainiest.get("precipitation", 0.0))

    humidity_val = float(most_humid.get("humidity", 0.0))
    humidity_str = f"{int(humidity_val)}%" if humidity_val.is_integer() else f"{humidity_val}%"

    summary_lines = [
        "Weather Summary:",
        f"Hottest day: {hottest.get('date')} with a maximum temperature of {hottest_temp:.1f}°C",
        f"Windiest day: {windiest.get('date')} with wind speeds of {windiest_speed:.1f} km/h",
        f"Most humid day: {most_humid.get('date')} with a humidity level of {humidity_str}",
        f"Rainiest day: {rainiest.get('date')} with {rainiest_precip:.1f} mm of precipitation",
    ]

    return "\n".join(summary_lines)


if __name__ == "__main__":
    try:
        import os

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        daily_list = weather_data.get("daily", []) if isinstance(weather_data, dict) else weather_data
        analyses = [analyze_daily_weather(day) for day in daily_list]

        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)
            print()

        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")