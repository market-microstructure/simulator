'''
Created on Sep 23, 2013

@author: Silver
'''

from objects.Order import ExecutionReport

class Rulebook():
    def __init__(self, service_locator):
        self.services = service_locator
    
    def match_all(self, symbol):
        
        # TODO major performance issue here!!  
        for id, order in self.services.bus.get_orderbook().iteritems():
            if order.symbol == symbol:
                self.match_one(id)
    
    def match_one(self, id):        
                
        order = self.services.bus.get_orderbook()[id]
        if not isinstance(order.leaves, int): order.leaves = order.size
        market = self.services.bus.get_market_data()[order.symbol]
        executions = []
        if order.side == 1: 
            limit = 0
            while market.has_key("ask-%d" % limit) and order.price >= market["ask-%d" % limit]["price"]: #buy order check over ask                         
                # build the execution report for this limit
                e = ExecutionReport()
                e.price = market["ask-%d" % limit]["price"]
                e.size = min(market["ask-%d" % limit]["size"], order.leaves)                
                e.symbol = order.symbol
                e.id = order.id
                executions.append(e)
                
                # update the order
                order.executed += e.size
                order.leaves   -= e.size
                if order.leaves <= 0:                    
                    break 
            
                limit += 1
                
        if order.side == -1 and order.price <= market["bid-0"]["price"]: # sell order check over bid
            limit = 0
            while market.has_key("bid-%d" % limit) and order.price <= market["bid-%d" % limit]["price"]: #buy order check over bid                         
                # build the execution report for this limit
                e = ExecutionReport()
                e.price = market["bid-%d" % limit]["price"]
                e.size = min(market["bid-%d" % limit]["size"], order.leaves)                
                e.symbol = order.symbol
                e.id = order.id
                executions.append(e)
                
                # update the order
                order.executed += e.size
                order.leaves   -= e.size
                if order.leaves <= 0:                    
                    break 
                
                limit += 1
        
        if order.leaves <= 0:
            del order
        
        if executions:
            # push execution in the bus
            self.services.bus._last_execution[id] = executions    
            self.services.events['Execution'].emit(id)