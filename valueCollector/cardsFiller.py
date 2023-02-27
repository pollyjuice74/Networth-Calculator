from bs4 import BeautifulSoup
import csv
import requests
import re


def main():
    with open('Networth_calculator/csvs/cards.csv', "r") as input, open('Networth_calculator/csvs/updated_cards.csv', "w", newline='') as out:
        reader = csv.reader(input)
        writer = csv.writer(out)

        rows = list(reader)

        print(rows)

        for card in rows[1:]:
            card_name = card[0]
            card_number = card[1]

            url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311&_nkw={card_name}{card_number}"
            get_html(url)
            price = get_card_price(card_name, card_number)

            card[2] = price

        writer.writerows(rows)


def get_card_price(card_name, card_number):
    # Open card url
    with open('output.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Creates soup object from content using lxml parser
    soup = BeautifulSoup(content, 'lxml')

    # Finds all 'span' tags in the html file
    tags = soup.find_all('span')
    data = ''

    for tag in tags[:10000]:
        data += tag.text.lower()
    print(data)

    # Specifying pattern 
        # '.*' is like LIKE '%something%' in SQL for the longest match possible
        # '.*?' matches the shortest match possible
        # '\d' digits, '\d+' one or more digits, '\d{2}' only two digits
        # Anything in parentheses is the match

    # If name matches, get price
    pattern = rf"{card_name}.*?{card_number}.*?(usd\d+\.\d{2})"

    print("Finding matches...")
    matches = re.findall(pattern, data)

    # Initialize variables
    prices = 0
    i = 0

    # Find the average price of card
    for match in matches:
        price = float(match.replace('usd', ''))
        prices += price
        i += 1

        median_price = round(prices / i, 2) 

    try: 
        print(median_price)
    except UnboundLocalError:
        print("No prices found for ", card_name)

    return median_price


def get_html(url):
    response = requests.get(url)

    # Truncate output.html contents 
    # AKA deleting the previous contents
    with open('output.html', 'w') as file:
        file.truncate()

    # Write html code of web page
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(response.text)


main()