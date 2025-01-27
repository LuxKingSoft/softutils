import http.client
import json

"""
This script is to get all valid categories/countries of a given sport and save that data to a file locally.
"""

sport = "football"
filename = '../categories_for_nations_or_leagues.json'
conn = http.client.HTTPSConnection("sofascore.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "14f97290c2msh731153450ed254ep126589jsn5562f571d602",
    'x-rapidapi-host': "sofascore.p.rapidapi.com"
}

conn.request("GET", f"/categories/list?sport={sport}", headers=headers)

res = conn.getresponse()
data = res.read()

# Save data to file
with open(filename, 'w') as file:
	json_data_object = json.loads(data.decode("utf-8"))
	json.dump(json_data_object, file, indent=4)

print("Done...")