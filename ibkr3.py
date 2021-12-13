from ib_insync import *
import multiprocessing
import time
from argparse import ArgumentParser

class Bot:
    def __init__(self, data, args):
        self.ib = IB()
        self.data = data
        self.ib.connect('127.0.0.1', 7497, clientId=1)
        contracts = []
        for con,sec,ex in zip(args['ticker'],args['security'],args['exchange']):
            contracts.append(Contract(symbol=con, secType=sec, exchange=ex))
        self.ib.pendingTickersEvent += self.onPendingTicker
        self.market_data = [self.ib.reqMktData(contract,'',False,False) for contract in contracts]
        self.ib.run()
        
    def onPendingTicker(self, tickers):
        self.data['marketPrice'] = [x.marketPrice() for x in self.market_data]

def init_bot(data, args):
    bot = Bot(data, args)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--ticker", help="Ticker code", default='ADT')
    parser.add_argument("-s", "--security", help="Security type", default='STK')
    parser.add_argument("-e", "--exchange", help="Exchange code", default='ASX')
    args = vars(parser.parse_args())
    args['ticker'] = [x.upper() for x in args['ticker'].split(',')]
    args['security'] = [x.upper() for x in args['security'].split(',')]
    args['exchange'] = [x.upper() for x in args['exchange'].split(',')]
    manager = multiprocessing.Manager()
    data = manager.dict()
    x = multiprocessing.Process(target=init_bot, args=[data, args])
    x.start()
    while True:
        print(data)
        time.sleep(2)

# class Contract(secType: str='', conId: int=0, symbol: str='', lastTradeDateOrContractMonth: str='', strike: float=0.0, right: str='', multiplier: str='', exchange: str='', primaryExchange: str='', currency: str='', localSymbol: str='', tradingClass: str='', includeExpired: bool=False, secIdType: str='', secId: str='', comboLegsDescrip: str='', comboLegs: List['ComboLeg']=field(default_factory=list), deltaNeutralContract: Optional['DeltaNeutralContract']=None)
# Contract(**kwargs) can create any contract using keyword arguments. To simplify working with contracts, there are also more specialized contracts that take optional positional arguments. Some examples

# Contract(conId=270639)
# Stock('AMD', 'SMART', 'USD')
# Stock('INTC', 'SMART', 'USD', primaryExchange='NASDAQ')
# Forex('EURUSD')
# CFD('IBUS30')
# Future('ES', '20180921', 'GLOBEX')
# Option('SPY', '20170721', 240, 'C', 'SMART')
# Bond(secIdType='ISIN', secId='US03076KAA60')
# Crypto('BTC', 'PAXOS', 'USD')
# Args: conId (int): The unique IB contract identifier. symbol (str): The contract (or its underlying) symbol. secType (str): The security type:

# * 'STK' = Stock (or ETF)
# * 'OPT' = Option
# * 'FUT' = Future
# * 'IND' = Index
# * 'FOP' = Futures option
# * 'CASH' = Forex pair
# * 'CFD' = CFD
# * 'BAG' = Combo
# * 'WAR' = Warrant
# * 'BOND' = Bond
# * 'CMDTY' = Commodity
# * 'NEWS' = News
# * 'FUND' = Mutual fund
# * 'CRYPTO' = Crypto currency
