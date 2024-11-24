import requests
import json

initialQuery = "https://api.scryfall.com/cards/search?format=json&include_extras=false&include_multilingual=false&include_variations=false&order=name&page=1&q=is%3Acommander+%28game%3Apaper%29+f%3Acommander&unique=cards"

commanderData: list = []

result = json.loads(requests.get(initialQuery).text)
commanderData = result['data']

while result['has_more']:
    result = json.loads(requests.get(result['next_page']).text)
    commanderData.extend(result['data'])


with open('commanders.json', 'w', encoding='utf-8') as commanderFile:
    commanderNames = []
    for commander in commanderData:
        commanderNames.append(commander['name'])
    
    json.dump(commanderNames, commanderFile, ensure_ascii=False, indent=4)
