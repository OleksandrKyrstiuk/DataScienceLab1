import csv
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, TextIO, Union


def parse_weather_xml(xml_file: Union[str, TextIO]) -> List[Dict[str, Any]]:
    """Parse weather data from an XML file or file-like object.

    Args:
        xml_file (str or file-like object): Path to the XML file or a file-like buffer.

    Returns:
        list of dict: A list of dictionaries containing parsed daily weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML content is malformed.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    parsed_data = []

    for day in root.iter("day"):
        date_elem = day.find("date")
        temp_elem = day.find("temperature")
        hum_elem = day.find("humidity")
        precip_elem = day.find("precipitation")

        date = date_elem.text.strip() if date_elem is not None and date_elem.text else ""
        temperature = float(temp_elem.text) if temp_elem is not None and temp_elem.text else 0.0

        hum_val = float(hum_elem.text) if hum_elem is not None and hum_elem.text else 0.0
        humidity = int(hum_val) if hum_val.is_integer() else hum_val

        precipitation = float(precip_elem.text) if precip_elem is not None and precip_elem.text else 0.0

        parsed_data.append({
            "Date": date,
            "Temperature": temperature,
            "Humidity": humidity,
            "Precipitation": precipitation,
            # Додаткові ключі для сумісності з тестами
            "date": date,
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
        })

    return parsed_data


def save_to_csv(data: List[Dict[str, Any]], filename: Union[str, TextIO] = "parsed_weather_data.csv") -> None:
    """Save parsed weather data to a CSV file or file-like object.

    Args:
        data (list of dict): Parsed weather data.
        filename (str or file-like object): Path to output CSV file or buffer.

    Raises:
        IOError: If writing to the file or buffer fails.
    """
    headers = ["Date", "Temperature", "Humidity", "Precipitation"]

    def write_rows(writer: csv.DictWriter) -> None:
        writer.writeheader()
        for row in data:
            hum = row.get("Humidity", row.get("humidity", 0))
            if isinstance(hum, float) and hum.is_integer():
                hum = int(hum)

            writer.writerow({
                "Date": row.get("Date", row.get("date", "")),
                "Temperature": float(row.get("Temperature", row.get("temperature", 0.0))),
                "Humidity": hum,
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
        import os

        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")