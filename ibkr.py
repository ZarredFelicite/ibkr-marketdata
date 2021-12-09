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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-t", "--ticker", help="Ticker code", required=True)
    parser.add_argument(
        "-e", "--exchange", help="Exchange code", required=True
    )
    args = vars(parser.parse_args())
    conids = {
        "adt": "316336245",
        "mlx": "44202491",
        "ctm": "74237654",
        "afm": "176898301",
        "fil": "244105117",
    }
    if args["ticker"] not in list(conids.keys()):
        args["ticker"] = args["ticker"].upper()
        args["exchange"] = args["exchange"].upper()
        print("Pulling conid from API")
        conid = str(get_conid(tickers=[args["ticker"]], exchange=args["exchange"])[0])
    else:
        print("Pulling conid from cache")
        conid = conids[args["ticker"]]
    url = "https://localhost:5000/v1/api/iserver/marketdata/history?period=1min&conid="
    url = url + conid
    while True:
        response = requests.get(url, verify=False)
        print(response)
        print(
            "Price of "
            + args["ticker"]
            + " is: "
            + str(response.json()["data"][0]["c"])
        )

"""

TO DO:
- add option for period customisation
- Make asychronous
- Update cache of conids to file

"""
