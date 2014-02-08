'''
Created on Feb 8, 2014

@author: Silver
'''
from datetime import datetime
from pandas import DataFrame
class ZIBus(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._public_data     = {}
        self._private_data_buy    = {}
        self._private_data_sell    = {}
        
        self._last_execution = {}
        self._last_reject = {}
        
        self._new_order = None

        self._indicators = DataFrame()
        
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def get_market_data(self):      
        
        snapshot = {"time": datetime.now(),
                    "event": "lob"                            
                    }
        
        for symbol, ob in self._private_data_buy.iteritems():
            if not snapshot.has_key(symbol):
                snapshot[symbol] = {}
            bid_prices = sorted(ob.keys(), reverse = True)   
            for i in range(len(bid_prices)): 
                price = bid_prices[i]               
                snapshot[symbol]["bid-%d" % i] = {"price": price, "size": sum([o.shown for o in ob[price]])}
                i += 1
                
        for symbol, ob in self._private_data_sell.iteritems():
            if not snapshot.has_key(symbol):
                snapshot[symbol] = {}            
            
            ask_prices =  sorted(ob.keys())       
            for i in range(len(ask_prices)):
                price = ask_prices[i]            
                snapshot[symbol]["ask-%d" % i] = {"price": price, "size": sum([o.shown for o in ob[price]])}
                        
        return snapshot
    
       
    def get_executions(self):
        return self._last_execution
    
    def get_rejects(self):
        return self._last_reject
    
    def get_indicators(self):
        return self._indicators

    def inject_snapshot(self, symbol, snapshot):
        self._public_data_update[symbol] = snapshot

    def insert_new_order(self, order):
        self._new_order = order        
            
    def push_private_update(self, id):
        order = self._new_order
        if order == None:
            return
        
        side = order.side
        symbol = order.symbol
        price  = order.price
        if side == 1:
            if not self._private_data_buy.has_key(symbol):
                self._private_data_buy[symbol] = {}
            
            if not self._private_data_buy[symbol].has_key(price):
                self._private_data_buy[symbol][price] = []        
            
            self._private_data_buy[symbol][price].append(order)
        elif side == -1:
            if not self._private_data_sell.has_key(symbol):
                self._private_data_sell[symbol] = {}
            
            if not self._private_data_sell[symbol].has_key(price):
                self._private_data_sell[symbol][price] = []        
            
            self._private_data_sell[symbol][price].append(order)
            

