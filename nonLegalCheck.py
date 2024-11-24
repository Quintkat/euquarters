import requests
import json

initialQuery = "https://api.scryfall.com/cards/search?q=-f%3Acommander&format=json"

commanderData: list = []

result = json.loads(requests.get(initialQuery).text)
commanderData = result['data']

while result['has_more']:
    result = json.loads(requests.get(result['next_page']).text)
    commanderData.extend(result['data'])

print(len(commanderData))

nonLegalAPI = []
for commander in commanderData:
    nonLegalAPI.append(commander['name'])


cardData = []
nonLegal = []

with open('oracle-cards-20241111100213.json', 'r', encoding='utf-8') as cardsFile:
    cardData = json.load(cardsFile)

for card in cardData:
    # if 'legalities' in card and 'commander' in card['legalities'] and card['legalities']['commander'] != "legal":
    if card['layout'] != 'art_series' and "Token" not in card['type_line'] and card['legalities']['commander'] != "legal":
        nonLegal.append(card['name'])

print(len(nonLegal))

# difference = []
# for i in nonLegal:
#     if i not in nonLegalAPI:
#         difference.append(i)

# print(len(difference))

# with open('difference.json', 'w', encoding='utf-8') as differenceFile:
#     json.dump(difference, differenceFile, ensure_ascii=False, indent=4)


# difference = []
# for i in nonLegalAPI:
#     if i not in nonLegal:
#         difference.append(i)
# with open('difference2.json', 'w', encoding='utf-8') as differenceFile:
#     json.dump(difference, differenceFile, ensure_ascii=False, indent=4)



# with open('.json', 'w', encoding='utf-8') as commanderFile:
#     commanderNames = []
#     for commander in commanderData:
#         commanderNames.append(commander['name'])
    
#     json.dump(commanderNames, commanderFile, ensure_ascii=False, indent=4)
