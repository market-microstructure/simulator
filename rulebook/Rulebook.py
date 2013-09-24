'''
Created on Sep 23, 2013

@author: Silver
'''

from tools.Order import ExecutionReport

class Rulebook():
    def __init__(self, service_locator):
        self.services = service_locator
    
    def match(self, symbol = "", id = ""):
        # returns a list of executions
        if id != "":
            order = self.services.bus.get_orderbook()[id]
            market = self.services.bus.get_market_data()[order.symbol]
            if order.side == 1 and order.price >= market["ask"]: #buy order check over ask
                # very simple matching logic
                e = ExecutionReport()
                e.price = order.price
                e.size = order.size
                e.leaves = 0
                e.symbol = order.symbol
                e.id = order.id
                return [e]
            
            if order.side == -1 and order.price <= market["bid"]: # sell order check over bid
                # very simple matching logic
                e = ExecutionReport()
                e.price = order.price
                e.size = order.size
                e.leaves = 0
                e.symbol = order.symbol
                e.id = order.id
                return [e]
        
        return []