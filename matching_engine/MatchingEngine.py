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
    
    def inject_new_order(self, symbol, id, order):
        pass
    
    def inject_modify_order(self, symbol, id, order):
        pass
    
    def inject_cancel_order(self, symbol, id):
        pass