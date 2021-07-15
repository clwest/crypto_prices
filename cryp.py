import requests 
from lxml import html
import json


def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()

# @click.command()
# @click.option('--cryptourl', default="https://www.coindesk.com/price/bitcoin", help='Please provide a crypto from coindesk.com')
# @click.option('--filename', default='output.json', help='Please provide a filename CSV/JSON')
# def scrape(cryptourl, filename):

all_currencies = []

resp = requests.get(url="https://www.coindesk.com/coindesk20", headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
})



tree = html.fromstring(html=resp.content)

currencies = tree.xpath("//section[@class='tr-section']")
for currency in currencies:
    crypto = {
        'name': currency.xpath(".//span[@class='cell cell-asset']/strong/text()")[0],
        'price': currency.xpath(".//div[@class='tr-right has-scroll']//span/text()[1]")[0],
        'market_cap': currency.xpath(".//div[@class='td active']/span/text()")[0],
        'total_exchange_volume': currency.xpath(".//div[@class='dragscroll-container scroll-wrapper']//div[3]/span/text()[1]")[0],
        'returns(24H)': currency.xpath(".//div[@class='tr tr-right-wrapper']//div[4]/span/text()[1]")[0],
        'total_supply': currency.xpath(".//div[@class='tr tr-right-wrapper']//div[5]/span/text()[1]")[0],
        'category': currency.xpath(".//div[@class='tr tr-right-wrapper']//div[6]/span/text()[1]")[0],
        'value_proposition': currency.xpath(".//div[@class='tr tr-right-wrapper']//div[7]/span/text()[1]")[0],
        'consensus_mechanism': currency.xpath(".//div[@class='tr tr-right-wrapper']//div[8]/span/text()[1]")[0],
        'url': currency.xpath(".//img[@class='coin-logo']/@src")
        
    }

    all_currencies.append(crypto)
print(all_currencies)
