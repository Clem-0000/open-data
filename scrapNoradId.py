import requests
import re
import json
import os

# URL of the French satellites page
base_url = 'https://www.n2yo.com/satellites/?c=FR&t=country&p='

page_number = 0
pattern = re.compile(r'\[sat_id\]\s*=>\s*(\d+)')
satellites_data = []

while True:
    url = f"{base_url}{page_number}"

    response = requests.get(url)
    html_content = response.text

    matches = pattern.findall(html_content)

    if not matches:
        print(f"Aucun sat_id trouvé sur la page {page_number}. Arrêt du script.")
        break

    for match in matches:
        satellites_data.append({"sat_id": match})
        print("sat_id trouvé:", match)

    page_number += 1

# Write result in a JSON file
output_file = os.path.join(os.path.dirname(__file__), "satellites_data.json")
with open(output_file, 'w') as json_file:
    json.dump(satellites_data, json_file, indent=4)

print(f"Données de satellites enregistrées dans {output_file}")
