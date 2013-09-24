'''
Created on Sep 23, 2013

@author: Silver
'''

class Bus(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._public_data     = {}
        self._private_data    = {}
        
        self._public_data_update  = {}
        self._private_data_update = {}
        
        self._last_execution = {}

    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def get_market_data(self):
        return self._public_data
    
    def get_orderbook(self):
        return self._private_data

    def inject_snapshot(self, symbol, snapshot):
        self._public_data_update[symbol] = snapshot

    def insert_new_order(self, order):
        #if not self._order_update.has_key(order.symbol): self._order_update[order.symbol] = {}
        self._private_data_update[order.id] = order

    def push_public_update(self, symbol):
        self._public_data[symbol] =  self._public_data_update[symbol]
        del self._public_data_update[symbol]
        
    def push_private_update(self, id):
        self._private_data[id] = self._private_data_update[id]
        del self._private_data_update[id]