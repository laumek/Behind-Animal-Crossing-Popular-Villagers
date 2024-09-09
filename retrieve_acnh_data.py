import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

#Step 1: Fetch the villagers ranking info
url = "https://www.animalcrossingportal.com/tier-lists/new-horizons/all-villagers/"
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page with status code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')

obj = soup.body.find_all(attrs={"class": "c-tier"})
villager_data =[]


for tag in obj:
  tier_name = tag.find('p').text.strip()

  # Find all candidate containers within the tier
  candidates = tag.find_all(attrs={"class":"c-candidate-name-rank flex align-center"})
  for candidate in candidates:
    name = candidate.find('p', class_='c-candidate-name').text.strip()
    rank = candidate.find('p', class_='c-candidate-rank').text.strip()

    villager_data.append({
      'name': name,
      'rank': rank,
      'tier': tier_name
    })

villager_data = pd.DataFrame(villager_data)
villager_data.to_csv('villager_data.csv', index=False)

#Step 2: Fetch other details about villagers
url = "https://nookipedia.com/wiki/Villager/New_Horizons"
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page with status code: {response.status_code}")


soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr', {"style" : "text-align:center;"})

characters = []

for r in rows:  # Assuming each character has 6 rows
  print(r.text)
  characters.append(r.text)

info_villager = []
# Iterate through each character data string
for data in characters:
    # Strip whitespace and split the string into a list
    values = [value.strip() for value in data.split('\n') if value.strip()]

    # Create a dictionary for each character
    if len(values) == 6:  # Ensure there are exactly 6 elements
        character = {
            'Name': values[0],
            'Species': values[1],
            'Gender': values[2],
            'Personality': values[3],
            'Birthday': values[4],
            'Catchphrase': values[5],
        }
        info_villager.append(character)

info_villager = pd.DataFrame(info_villager)

df_final = pd.merge(villager_data, info_villager, how='left', left_on=['name'], right_on=['Name'])
df_final.to_csv('villager_data_final.csv', index=False)
df_final.head() # Check merged DataFrame