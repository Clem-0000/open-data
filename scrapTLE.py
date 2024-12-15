import requests
import json
import os

satellites_data_file = os.path.join(os.path.dirname(__file__), "satellites_data.json")
with open(satellites_data_file) as json_file:
    satellites_data = json.load(json_file)

tle_data = {}

for country, satellites in satellites_data.items():
    for sat_id in satellites:
        print(f"Processing for sat_id: {sat_id}")
        url = f"https://www.n2yo.com/satellite/?s={sat_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error retrieving data for {sat_id}: {e}")
            continue

        html_content = response.text

        tle_start = html_content.find('<div id="tle">')

        if tle_start == -1:
            print(f"No TLE found for {sat_id}.")
            continue

        pre_start = html_content.find("<pre>", tle_start)
        pre_end = html_content.find("</pre>", pre_start)

        tle = html_content[pre_start + 5 : pre_end].replace("\r", "").strip()

        satinfo_start = html_content.find('<div id="satinfo">')

        if satinfo_start == -1:
            print(f"No satinfo found for {sat_id}.")
            continue

        satname_start = html_content.find("<H1>", satinfo_start)
        satname_end = html_content.find("</H1>", satname_start)

        satname = html_content[satname_start + 4 : satname_end].strip()

        tle_data[sat_id] = {
            "satname": satname,
            "tle": tle,
        }

output_file = os.path.join(os.path.dirname(__file__), "tle_data.json")
with open(output_file, "w") as json_file:
    json.dump(tle_data, json_file, indent=4)

print(f"Data saved to {output_file}.")
