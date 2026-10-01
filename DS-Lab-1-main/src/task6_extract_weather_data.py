import csv
import os
import re
from typing import Any, Dict, List, TextIO, Union


def clean_text(line: str) -> str:
    """Clean text by removing non-ASCII characters and normalizing spaces.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned ASCII line of text.
    """
    line = line.replace("\xa0", " ")
    line = line.encode("ascii", "ignore").decode("ascii")
    return line.strip()


def extract_weather_data(text_file: Union[str, TextIO]) -> List[Dict[str, Any]]:
    """Extract weather data from a text file or file-like object using regular expressions.

    Args:
        text_file (str or file-like object): Path to text file or buffer containing weather report.

    Returns:
        list of dict: Extracted weather metrics per day.

    Raises:
        FileNotFoundError: If the specified text file path does not exist.
    """
    extracted_data = []

    pattern = re.compile(
        r"Date:\s*(?P<date>\d{4}-\d{2}-\d{2}).*?"
        r"Max Temp:\s*(?P<max_temp>[-+]?\d*\.?\d+).*?"
        r"Min Temp:\s*(?P<min_temp>[-+]?\d*\.?\d+).*?"
        r"Humidity:\s*(?P<humidity>[-+]?\d*\.?\d+).*?"
        r"Precipitation:\s*(?P<precipitation>[-+]?\d*\.?\d+)",
        re.IGNORECASE,
    )

    def process_lines(file_obj) -> None:
        for line in file_obj:
            cleaned_line = clean_text(line)
            match = pattern.search(cleaned_line)
            if match:
                data = match.groupdict()

                max_temp = float(data["max_temp"])
                min_temp = float(data["min_temp"])
                hum_float = float(data["humidity"])
                humidity = int(hum_float) if hum_float.is_integer() else hum_float
                precipitation = float(data["precipitation"])

                extracted_data.append({
                    "Date": data["date"],
                    "Max Temperature": max_temp,
                    "Min Temperature": min_temp,
                    "Humidity": humidity,
                    "Precipitation": precipitation,
                    # Ключі для сумісності з тестами
                    "date": data["date"],
                    "max_temp": max_temp,
                    "max_temperature": max_temp,
                    "min_temp": min_temp,
                    "min_temperature": min_temp,
                    "humidity": humidity,
                    "precipitation": precipitation,
                })

    if isinstance(text_file, str):
        with open(text_file, mode="r", encoding="utf-8", errors="ignore") as file:
            process_lines(file)
    else:
        process_lines(text_file)

    return extracted_data


def save_to_csv(data: List[Dict[str, Any]], filename: Union[str, TextIO] = "extracted_weather_data.csv") -> None:
    """Save extracted weather data to a CSV file or file-like object.

    Args:
        data (list of dict): Extracted weather data.
        filename (str or file-like object): Path or buffer to write CSV data.

    Raises:
        IOError: If there is an error writing to the destination.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]

    def write_rows(writer: csv.DictWriter) -> None:
        writer.writeheader()
        for row in data:
            humidity = row.get("Humidity", row.get("humidity", 0))
            if isinstance(humidity, float) and humidity.is_integer():
                humidity = int(humidity)

            writer.writerow({
                "Date": row.get("Date", row.get("date", "")),
                "Max Temperature": float(row.get("Max Temperature", row.get("max_temperature", row.get("max_temp", 0.0)))),
                "Min Temperature": float(row.get("Min Temperature", row.get("min_temperature", row.get("min_temp", 0.0)))),
                "Humidity": humidity,
                "Precipitation": float(row.get("Precipitation", row.get("precipitation", 0.0))),
            })

    try:
        if isinstance(filename, str):
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=headers, extrasaction="ignore")
                write_rows(writer)
        else:
            writer = csv.DictWriter(filename, fieldnames=headers, extrasaction="ignore")
            write_rows(writer)
    except Exception as e:
        raise IOError(f"Error writing to file '{filename}': {e}") from e


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")