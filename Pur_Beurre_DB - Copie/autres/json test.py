#file name; 10 most popular products on OFF.json

import json
import requests

get = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&sort_by=unique_scans_n&page_size=2&axis_x=energy-kj&axis_y=products_n&action=display&json=1")
print(json.loads(get.text))




"""response = json.loads(get.text)

type(response)
print(response)
"""
