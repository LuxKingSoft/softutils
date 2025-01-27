import http.client
import json

API_KEY = "14f97290c2msh731153450ed254ep126589jsn5562f571d602"
CATEGORIES_FILENAME = 'categories_for_nations_or_leagues.json'

conn = http.client.HTTPSConnection("sofascore.p.rapidapi.com")
headers = {
	'x-rapidapi-key': API_KEY,
	'x-rapidapi-host': "sofascore.p.rapidapi.com"
}

categories = {}
with open(CATEGORIES_FILENAME, 'rb') as f:
	categories.update(json.load(f))

print(f"Number of tournaments for the category selected: {len(categories['categories'])}")

for category in categories['categories']:
	category_id = category['id']
	print(category['name'], category_id)
	conn.request("GET", f"/tournaments/list?categoryId={category_id}", headers=headers)
	res = conn.getresponse()
	data = res.read()

	# Decode data and convert to json format
	decoded_data = json.loads(data.decode("utf-8"))

	# Save data to json files
	with open(f'tournaments_{category_id}.json', 'w') as f:
		json.dump(decoded_data, f, indent=4)

print("\nDone....")