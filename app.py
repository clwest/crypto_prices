import requests
from lxml import html
import json
import csv
import click


def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()

def write_to_csv(filename, data):
    headers = ['title', 'price', 'market_cap', 'volume_24H']
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerow(data)


@click.command()
@click.option('--cryptourl', default="https://www.coindesk.com/price/bitcoin", help='Please provide a crypto from coindesk.com')
@click.option('--filename', default='output.json', help='Please provide a filename CSV/JSON')
def scrape(cryptourl, filename):

    resp = requests.get(url=cryptourl, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    })
    tree = html.fromstring(html=resp.text)

    title = tree.xpath("//div[@class='coin-title']/h2/text()")[0]
    price = tree.xpath("//div[@class='price-large']/text()")[0]
    market_cap = tree.xpath("(//div[@class='price-medium']/text())[1]")[0]
    volume_24H = tree.xpath("(//div[@class='price-medium']/text())[2]")[0]
    low_24H = tree.xpath("(//div[@class='price-medium']/text())[3]")[0]
    high_24H = tree.xpath("(//div[@class='price-medium']/text())[4]")[0]
    crypto_info = {
        'title': title,
        'price': price,
        'market_cap': market_cap,
        'volume_24H': volume_24H,
        '24h_low': low_24H,
        '24H_high': high_24H
    }
    print(crypto_info)
    extension = filename.split('.')[1]

    if extension == 'json':
        write_to_json(filename, crypto_info)
    elif extension == 'csv':
        write_to_csv(filename, crypto_info)
    else:
        click.echo("The extension you provided is not supported, please use json or csv")
if __name__ == '__main__':
    scrape()

    