import requests
import re
import json
import os

countries = [
    {"name": "ALGERIA", "codeCountry": "ALG"},
    {"name": "ARGENTINA", "codeCountry": "ARGN"},
    {"name": "AUSTRALIA", "codeCountry": "AUS"},
    {"name": "AZERBAIJAN", "codeCountry": "AZER"},
    {"name": "BANGLADESH", "codeCountry": "BGD"},
    {"name": "BELARUS", "codeCountry": "BELA"},
    {"name": "BOLIVIA", "codeCountry": "BOL"},
    {"name": "BRAZIL", "codeCountry": "BRAZ"},
    {"name": "BULGARIA", "codeCountry": "BGR"},
    {"name": "CANADA", "codeCountry": "CA"},
    {"name": "CHILE", "codeCountry": "CHLE"},
    {"name": "CZECHIA", "codeCountry": "CZ"},
    {"name": "DENMARK", "codeCountry": "DEN"},
    {"name": "ECUADOR", "codeCountry": "ECU"},
    {"name": "EGYPT", "codeCountry": "EGYP"},
    {"name": "ESTONIA", "codeCountry": "EST"},
    {"name": "FRANCE", "codeCountry": "FR"},
    {"name": "GERMANY", "codeCountry": "GER"},
    {"name": "GREECE", "codeCountry": "GREC"},
    {"name": "HUNGARY", "codeCountry": "HUN"},
    {"name": "INDIA", "codeCountry": "IND"},
    {"name": "INDONESIA", "codeCountry": "INDO"},
    {"name": "IRAN", "codeCountry": "IRAN"},
    {"name": "IRAQ", "codeCountry": "IRAK"},
    {"name": "ISRAEL", "codeCountry": "ISRA"},
    {"name": "ITALY", "codeCountry": "IT"},
    {"name": "JAPAN", "codeCountry": "JPN"},
    {"name": "KAZAKHSTAN", "codeCountry": "KAZ"},
    {"name": "KENYA", "codeCountry": "KEN"},
    {"name": "KUWAIT", "codeCountry": "KWT"},
    {"name": "LAOS", "codeCountry": "LAOS"},
    {"name": "LITHUANIA", "codeCountry": "LTU"},
    {"name": "LUXEMBOURG", "codeCountry": "LUXE"},
    {"name": "MALAYSIA", "codeCountry": "MALA"},
    {"name": "MEXICO", "codeCountry": "MEX"},
    {"name": "MOROCCO", "codeCountry": "MA"},
    {"name": "NETHERLANDS", "codeCountry": "NETH"},
    {"name": "NEW ZEALAND", "codeCountry": "NZ"},
    {"name": "NIGERIA", "codeCountry": "NIG"},
    {"name": "NORTH KOREA", "codeCountry": "NKOR"},
    {"name": "NORWAY", "codeCountry": "NOR"},
    {"name": "PAKISTAN", "codeCountry": "PAKI"},
    {"name": "PERU", "codeCountry": "PER"},
    {"name": "POLAND", "codeCountry": "POL"},
    {"name": "PORTUGAL", "codeCountry": "POR"},
    {"name": "QATAR", "codeCountry": "QAT"},
    {"name": "SAUDI ARABIA", "codeCountry": "SAUD"},
    {"name": "SINGAPORE", "codeCountry": "SING"},
    {"name": "SOUTH AFRICA", "codeCountry": "SAFR"},
    {"name": "SOUTH KOREA", "codeCountry": "SKOR"},
    {"name": "SPAIN", "codeCountry": "SPN"},
    {"name": "SWEDEN", "codeCountry": "SWED"},
    {"name": "THAILAND", "codeCountry": "THAI"},
    {"name": "TURKEY", "codeCountry": "TURK"},
    {"name": "UNITED ARAB EMIRATES", "codeCountry": "UAE"},
    {"name": "UNITED KINGDOM", "codeCountry": "UK"},
    # {"name": "UNITED STATES", "codeCountry": "US"},
    {"name": "URUGUAY", "codeCountry": "URY"},
    {"name": "VENEZUELA", "codeCountry": "VENZ"},
    {"name": "VIETNAM", "codeCountry": "VTNM"},
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
