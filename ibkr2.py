import requests
import json
import urllib3
from argparse import ArgumentParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""Test implementation making requests to IBKR REST API to display stock price"""


def get_conid(tickers, exchange):
    conids = []
    for tick in tickers:
        url = "https://localhost:5000/v1/api/trsrv/stocks?symbols=" + tick
        response = requests.get(url, verify=False).json()
        response = [
            x for x in response[tick] if x["contracts"][0]["exchange"] == exchange
        ]
        conids.append(response[0]["contracts"][0]["conid"])
    return conids

def parse_cache(filename):
    with open(filename, 'r') as f:
        conids = json.load(f)
    return conids
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-t", "--ticker", help="Ticker code", default='pls')
    parser.add_argument("-e", "--exchange", help="Exchange code", default='asx')
    args = vars(parser.parse_args())
    conids = parse_cache(filename='conid_cache.txt')
    if args["ticker"] not in list(conids.keys()):
        args["ticker"] = args["ticker"].upper()
        args["exchange"] = args["exchange"].upper()
        print("Pulling conid from API")
        conid = str(get_conid(tickers=[args["ticker"]], exchange=args["exchange"])[0])
        #writing conid to cache
        with open('conid_cache.txt', 'w') as f:
            conids[args["ticker"].lower()] = conid
            json.dump(conids, f, ensure_ascii=False)
    else:
        print("Pulling conid from cache")
        conid = conids[args["ticker"]]
    fields = '83'
    url = "https://localhost:5000/v1/api/iserver/marketdata/snapshot?conids="
    url = url + conid + '&fields=' + fields
    while True:
        response = requests.get(url, verify=False)
        print(response.json()[0]['83'])
        # print(
        #     "Price of "
        #     + args["ticker"]
        #     + " is: "
        #     + str(response.json()["data"][0]["c"])
        # )