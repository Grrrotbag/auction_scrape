import requests
from bs4 import BeautifulSoup
import csv

file_name = "auction_list.csv"
f = csv.writer(open(file_name, 'w', newline=''))
f.writerow(['Item', 'Price', 'Link'])

for x in range(1, 10):
    page = requests.get(
        'https://www.euroauctionslive.com/servlet/Search.do?auctionId=475&page=' + str(x) + '&perPage=100&orderBy=')

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find(class_='item-listing')

    items = table.find_all('tr')

    title_result = []
    price_result = []
    link_result = []

    for item in items:
        title = item.find_all('h3')
        price = item.find_all('strong', {'style' : 'color: #00A'})
        for t in title:
            link = t.parent.get('href')
            title_result.append(t.text[33:-33])
            link_result.append('https://www.euroauctionslive.com' + link)
        for p in price:
            price_result.append(p.text[:-4])

    result = list(zip(title_result, price_result, link_result))

    for r in result:
        f.writerow([r[0], r[1], r[2]])
