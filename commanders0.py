import json


cardsData = {}
commanders = []

with open('oracle-cards-20241111100213.json', 'r', encoding='utf-8') as cardsFile:
    cardsData = json.load(cardsFile)

for card in cardsData:
    # if "Adun Oakenshield" == card['name']:
    #     # print(card)
    #     print("-----")
    #     print('legalities' in card)
    #     print('commander' in card['legalities'])
    #     print(card['legalities']['commander'] == 'legal')
    #     print(card['legalities']['commander'])
    #     print('games' in card)
    #     print("paper" in card['games'])
    #     print("Legendary" in card['type_line'])
    #     print("Creature" in card['type_line'])
    #     print('oracle_text' in card)
    #     print("can be your commander" in card['oracle_text'])
    if (
        'legalities' in card and
        'commander' in card['legalities'] and
        card['legalities']['commander'] == 'legal' and
        'games' in card and
        ("paper" in card['games'] or
        ("mtgo" in card['games'] and not ("paper" in card['games']))) and
        'layout' in card and
        card['layout'] != "flip" and
        (card['layout'] != "meld" or ('mana_cost' in card and card['mana_cost'] > "")) and
        (("Legendary" in card['type_line'] and
        "Creature" in card['type_line']) or
        ('oracle_text' in card and 
        "can be your commander" in card['oracle_text']) or
        "Background" in card['type_line'])
        ):
        commanders.append(card['name'])

print(len(commanders))
commanders.sort()
# print(commanders[120])
for i in range(376, 386):
    print(i, commanders[i])