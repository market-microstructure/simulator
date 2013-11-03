'''
Created on Sep 23, 2013

@author: Silver
'''

from MatchingEngine import *

class Level1MatchingEngine(MatchingEngine):
    def __init__(self, service_locator):
        MatchingEngine.__init__(self, service_locator)      
        
        
    def on_inject(self, symbol):        
        self.services.bus.push_public_update(symbol)        
        #matching goes here
        self.services.events['MarketData'].emit(symbol)    
       
    def on_new_order(self, id):
        # push order on the market
        self.services.bus.push_private_update(id)
        
        # add rejection logic here if needed
        self.services.events['AckNew'].emit(id)
    
    def inject_modify_order(self, symbol, id, order):
        pass
    
    def inject_cancel_order(self, symbol, id):
        pass