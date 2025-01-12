import requests
import re
import json
import os

countries = [
    {"name": "France", "codeCountry": "FR"},
    {"name": "Azerbaijan", "codeCountry": "AZER"},
    {"name": "Bangladesh", "codeCountry": "BGD"},
    {"name": "Belarus", "codeCountry": "BELA"},
    {"name": "Bolivia", "codeCountry": "BOL"},
    {"name": "Bulgaria", "codeCountry": "BGR"},
    {"name": "Denmark", "codeCountry": "DEN"},
    {"name": "Egypt", "codeCountry": "EGYP"},
    {"name": "Italy", "codeCountry": "IT"},
    {"name": "Kazakhstan", "codeCountry": "KAZ"},
    {"name": "Lithuania", "codeCountry": "LTU"},
    {"name": "Australia", "codeCountry": "AUS"},
]

pattern = re.compile(r"\[sat_id\]\s*=>\s*(\d+)")
satellites_data = {}

for country in countries:
    country_name = country["name"]
    code_country = country["codeCountry"]

    base_url = f"https://www.n2yo.com/satellites/?c={code_country}&t=country&p="
    page_number = 0
    country_satellites = []

    print(f"Processing for country: {country_name}")

    while True:
        url = f"{base_url}{page_number}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error retrieving data for {country_name}: {e}")
            break

        html_content = response.text
        matches = pattern.findall(html_content)

        if not matches:
            print(f"No sat_id found on page {page_number} for {country_name}.")
            break

        country_satellites.extend(matches)
        print(f"Page {page_number}: {len(matches)} sat_id found.")

        page_number += 1

    satellites_data[country_name] = country_satellites

output_file = os.path.join(os.path.dirname(__file__), "satellites_data.json")
with open(output_file, "w") as json_file:
    json.dump(satellites_data, json_file, indent=4)

print(f"Satellite data saved in {output_file}")
