import json
# import getNonLegal
# import getCommanders

singlesData = {}
priceData = {}
commanders = []
nonLegal = []

singles = {}
nonSingles = []
prices = {}
pricesCommanders = {}

problems = []
quarters = []
qCommanders = []

nonsenseExpansions = [105]

with open('products_singles_1.json', 'r', encoding='utf-8') as singlesFile:
    singlesData = json.load(singlesFile)

with open('price_guide_1.json', 'r', encoding='utf-8') as priceFile:
    priceData = json.load(priceFile)

with open('commanders.json', 'r', encoding='utf-8') as commandersFile:
    commanders = json.load(commandersFile)

with open('nonLegal.json', 'r', encoding='utf-8') as nonLegalFile:
    nonLegal = json.load(nonLegalFile)

print("amount of commander cards:", len(commanders))
print("amount of commander non-legal cards:", len(nonLegal))

def isCardLegal(name, maxPrice, priceList):
    single = singles[name]
    for id in single:
        if not (id in priceList):
            continue

        if priceList[id] is None:
            continue

        if priceList[id] <= maxPrice:
            return True
    
    return False


for product in singlesData['products']:
    name : str = (
        product['name']
        .replace('//', '/')
        .replace('""', '"')
        .replace("Muerra, Thrash Tactician", "Muerra, Trash Tactician")
        .replace("Surtr, Fiery Jötum", "Surtr, Fiery Jötun")
    )
    if (
        name.startswith("Art Series:") or 
        name.startswith("Jumpstart Pack Summary Card:") or 
        "Token" in name or 
        name in nonLegal or 
        product['idExpansion'] in nonsenseExpansions
    ):
        nonSingles.append(product['idProduct'])
        continue

    if not (name in singles):
        singles[name] = []
    
    singles[name].append(product['idProduct'])


for product in priceData['priceGuides']:
    if product['idProduct'] in nonSingles:
        continue

    trend = 0
    low = 0
    if 'trend' in product and product['trend'] != None and product['trend'] != 0:
        trend = product['trend']
        if 'low' in product:
            low = product['low']
        elif 'low-foil' in product:
            low = product['low-foil']
    elif 'trend-foil' in product:
        trend = product['trend-foil']
        if 'low-foil' in product:
            low = product['low-foil']
    
    # if 'low' in product:
    #     low = product['low']
    # elif 'low-foil' in product:
    #     low = product['low-foil']
    
    # if not (low is None) and low > 0 and not (trend is None) and trend > 0:
    #     if low > trend and trend <= 0.25 and low > 0.25 and low < 0.35:
    #         problems.append(product['idProduct'])

    if not (low is None) and low > 0 and not (trend is None) and trend > 0:
        if (trend <= 0.25 and low > 0.30) or (trend <= 0.05 and low > 0.25):
            prices[product['idProduct']] = low
        else:
            prices[product['idProduct']] = trend
    
    if not (low is None) and low > 0 and not (trend is None) and trend > 0:
        if (trend <= 1 and low > 1.1) or (trend <= 0.20 and low > 1):
            pricesCommanders[product['idProduct']] = low
        else:
            pricesCommanders[product['idProduct']] = trend


for i in range(len(commanders)):
    commander : str = commanders[i]
    commanders[i] = commander.replace('//', '/').replace('""', '"').replace('꞉', ':')


for name in singles:
    if isCardLegal(name, 0.25, prices):
        quarters.append(name)


for commander in commanders:
    name = ""
    if commander not in singles:
        if '/' in commander:
            commander2 = commander.split('/')[0][0:-1]
            if commander2 in singles:
                name = commander2
        else:
            for singleName in singles:
                if commander in singleName:
                    name = singleName
                    break
    else:
        name = commander
    
    if isCardLegal(name, 1, pricesCommanders):
        qCommanders.append(name)

def printPrices(name:str):
    print(name, ": legal" if isCardLegal(name, 0.25, prices) else ": not legal")
    for id in singles[name]:
        if id in prices:
            print(id, ":", prices[id])
        else:
            print(id, ": not in prices")
        # print()
        # if id
        # print(prices[id])
    

print(len(singles))
print(len(prices))
print(len(quarters))
print(len(qCommanders))
# printPrices("Invoke Calamity")
# printPrices("Powerbalance")
# printPrices("Fire Servant")


with open('quartersLegal99.txt', 'w', encoding='utf-8') as quartersFile:
    quartersFile.write('\n'.join(sorted(quarters)))

    
with open('quartersLegalCommanders.txt', 'w', encoding='utf-8') as quartersCommanderFile:
    quartersCommanderFile.write('\n'.join(sorted(qCommanders)))


htmlStart = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="/euquarters/style.css" rel="stylesheet" type="text/css" media="all">
    <link rel="stylesheet" href="https://cdn.datatables.net/2.1.8/css/dataTables.dataTables.css" />
</head>
<body>
    <header>
      <a href="/euquarters/index.html" class="headerMainLink indexLink">Quarters (A budget commander variant) (Europe version)</a>
      <a href="/euquarters/legal99.html" class="headerMainLink otherLinks">Legal cards</a>
      <a href="/euquarters/legalCommanders.html" class="headerMainLink otherLinks">Legal commanders</a>
      <a href="/euquarters/legalCheck.html" class="headerMainLink otherLinks">Deck checker</a>
    </header>
    <div class="bodyContent">
"""

tableStart = """
    <table id="example" class="display" style="width:100%">
        <thead>
            <tr>
                <th>Name</th>
                <th>Scryfall</th>
                <th>Cardmarket</th>
            </tr>
        </thead>
        <tbody>
"""

htmlEnd = """
        </tbody>
    </table>
    <footer>
      Website made and maintained by Anna. <br>
      Quarters is unofficial Fan Content permitted under the Fan Content Policy. Not approved/endorsed by Wizards. Portions of the materials used are property of Wizards of the Coast. ©Wizards of the Coast LLC.
    </footer>
    </div>
    <script src="https://code.jquery.com/jquery-3.7.1.js"></script>
    <script src="https://cdn.datatables.net/2.1.8/js/dataTables.js"></script>
    <script>
      let table = new DataTable('#example', {
        layout: {
          top2Start: 'search',
          top2End: null,
          topStart: 'info',
          topEnd: 'paging',
          bottomStart: 'info',
          bottomEnd: 'paging'
        },
        pageLength: 100
      });
    </script>
  </body>
</html>
"""

with open('legalCommanders.html', 'w', encoding='utf-8') as table:
    table.write(htmlStart.format(title="Quarters legal commanders")+'\n')
    table.write("    <h2>Legal commanders</h2>\n")
    table.write(tableStart)
    for commander in qCommanders:
        table.write(f"            <tr><td>{commander}</td><td><a href=\"https://scryfall.com/search?q={commander.replace(' ', '+')}\" target=\"_blank\">on Scryfall</a></td><td><a href=\"https://www.cardmarket.com/en/Magic/Products/Search?searchString={commander.replace(' ', '+')}\" target=\"_blank\">on Cardmarket</a></td></tr>\n")
    table.write(htmlEnd)



with open('legal99.html', 'w', encoding='utf-8') as table:
    table.write(htmlStart.format(title="Quarters legal in the 99")+'\n')
    table.write("    <h2>Legal cards in the 99</h2>\n")
    table.write(tableStart)
    for card in sorted(quarters):
        table.write(f"            <tr><td>{card}</td><td><a href=\"https://scryfall.com/search?q={card.replace(' ', '+')}\" target=\"_blank\">on Scryfall</a></td><td><a href=\"https://www.cardmarket.com/en/Magic/Products/Search?searchString={card.replace(' ', '+')}\" target=\"_blank\">on Cardmarket</a></td></tr>\n")
        # table.write(f"            <tr><td>{card}</td><td></td><td></td></tr>\n")
    table.write(htmlEnd)
