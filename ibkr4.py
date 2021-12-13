from ib_insync import *
import time
import multiprocessing

def onPendingTicker(tickers):
    print(list(tickers)[0].marketPrice())
def ib():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    ib.pendingTickersEvent += onPendingTicker
    # #symbol = input("Enter symbol to trade: ")
    contract = Crypto('BTC', 'PAXOS', 'USD')
    # #contract = Stock(symbol.upper(),'SMART','AUD')
    market_data = ib.reqMktData(contract,'',False,False)
    ib.run()

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    x = multiprocessing.Process(target=ib)
    x.start()
    y=1
    while True:
        y+=1
        print(y)
        time.sleep(1)