
from objects.Order import ExecutionReport


class ZIRulebook():
    def __init__(self, service_locator):
        self.services = service_locator    
    
    
    def match_one(self, id):        
        order = self.services.bus._new_order        
        order.leaves = order.size
        order.executed = 0
        executions = []        
        if order.side == 1: # buy
            if order.symbol not in self.services.bus._private_data_sell.keys():
                return
            ask = self.services.bus._private_data_sell[order.symbol]
            prices = sorted(ask.keys())
            i = 0
            current_price = prices[i]
            while order.leaves > 0 and current_price <= order.price:
                for o in ask[current_price]:
                    e = ExecutionReport()
                    e.price = current_price
                    e.size = min(o.leaves, order.leaves)                
                    e.symbol = order.symbol
                    e.id = order.id
                    e.parent = order.parent
                    executions.append(e)
                    
                    e = ExecutionReport()
                    e.price = current_price
                    e.size = min(o.leaves, order.leaves)                
                    e.symbol = order.symbol
                    e.id = o.id    
                    e.parent = o.parent
                    self.services.bus._last_execution[o.id] = []                
                    self.services.bus._last_execution[o.id].append(e)
                    self.services.events['Execution'].emit(o.id)
                    
                    order.leaves -= e.size
                    order.executed += e.size
                    if order.leaves == 0:
                        self.services.bus._new_order = None
                        break
                
                i = i+1
                current_price = prices[i]
        elif order.side == -1: # buy
            if order.symbol not in self.services.bus._private_data_buy.keys():
                return
            bid = self.services.bus._private_data_buy[order.symbol]
            prices = sorted(bid.keys(), reverse = True)
            i = 0
            current_price = prices[i]
            while order.leaves > 0 and current_price >= order.price:
                for o in bid[current_price]:
                    e = ExecutionReport()
                    e.price = current_price
                    e.size = min(o.leaves, order.leaves)                
                    e.symbol = order.symbol
                    e.id = order.id
                    e.parent = order.parent
                    executions.append(e)
                    
                    e = ExecutionReport()
                    e.price = current_price
                    e.size = min(o.leaves, order.leaves)                
                    e.symbol = order.symbol
                    e.id = o.id
                    e.parent = o.parent
                    
                    o.leaves -= e.size
                    o.executed += e.size
                    
                    id = o.id
                    if o.leaves <= 0:
                        self.services.logger.debug("Order %s fully filled. Removing from market" % o)
                        del o
                                                           
                    self.services.bus._last_execution[id] = []
                    self.services.bus._last_execution[id].append(e)
                    self.services.events['Execution'].emit(id)
                    
                    
                    order.leaves -= e.size
                    order.executed += e.size
                    if order.leaves == 0:
                        self.services.bus._new_order = None
                        break
                
                i = i+1
                current_price = prices[i]
               
            
        if len(executions) > 0:
            self.services.bus._last_execution[order.id] = []
            self.services.bus._last_execution[order.id].extend(executions)
            self.services.events['Execution'].emit(order.id)
            
        if str(order.timeinforce).upper() == 'IOC':
            self.services.bus._last_reject[order.id] = order
            #self.services.bus._last_reject[order.id].append(order)
            self.services.events['Reject'].emit(order.id)
            
                
            
            
        
                
        return False        
        