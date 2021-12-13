from ib_insync import *
import threading
import time



class Bot:
    def __init__(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)
        self.ib.pendingTickersEvent += self.onPendingTicker
        ib_thread = threading.Thread(target=self.run_loop)
        ib_thread.start()
        time.sleep(1)
        symbol = input("Enter symbol to trade: ")
        contract = Stock(symbol.upper(),'SMART','AUD')
        self.market_data = self.ib.reqMktData(contract,'221',False,False)
        
    def onPendingTicker(self, tickers):
        print(self.market_data)
    def run_loop(self):
        self.ib.run()


bot = Bot()
t = time.time()
while True:
    if t-time.time() > 100:
        print("hello")
        t = time.time()



