'''
Created on Sep 23, 2013

@author: Silver
'''


class MatchingEngine:
    def __init__(self, service_locator):
        self.services = service_locator
        
    def inject_snapshot(self, symbol, snapshot):
        pass
    
    def inject_update(self, symbol, update):
        pass
    
    def on_new_order(self, symbol, id, order):
        pass
    
    def on_modify_order(self, symbol, id, order):
        pass
    
    def on_cancel_order(self, symbol, id):
        pass