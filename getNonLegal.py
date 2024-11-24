import json


cardData = []
nonLegal = []

with open('scryfall_all_cards.json', 'r', encoding='utf-8') as cardsFile:
    cardData = json.load(cardsFile)

for card in cardData:
    # if 'legalities' in card and 'commander' in card['legalities'] and card['legalities']['commander'] != "legal":
    if card['layout'] != 'art_series' and "Token" not in card['type_line'] and card['legalities']['commander'] != "legal":
        nonLegal.append(card['name'])

print("amount of commander non-legal cards:", len(nonLegal))

with open('nonLegal.json', 'w', encoding='utf-8') as nonLegalFile:
    json.dump(nonLegal, nonLegalFile, ensure_ascii=False, indent=4)