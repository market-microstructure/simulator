'''
Created on Feb 8, 2014

@author: Silver
'''

from matching_engine.MatchingEngine import MatchingEngine

class ZeroIntelligenceMatchingEngine(MatchingEngine):
    def __init__(self, service_locator):
        MatchingEngine.__init__(self, service_locator)        
        
    def on_inject(self, symbol):        
        #self.services.bus.push_public_update(symbol)        
        #matching goes here
        self.services.events['MarketData'].emit(symbol)    
       
    def on_new_order(self, id):
        self.services.events['AckNew'].emit(id)
                
        # push order on the market        
        self.services.bus.push_private_update(id)
        
        
    def inject_modify_order(self, symbol, id, order):
        pass
    
    def inject_cancel_order(self, symbol, id):
        pass
    