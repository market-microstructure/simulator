'''
Created on Jan 29, 2014

@author: Silver
'''
from objects.Order import *
from utils.generate_snapshots_SOR import generate_snapshot

class ZeroIntelligenceAgent:
    def __init__(self, service_locator, params):
        self.services = service_locator        
        self.orderbooks = generate_snapshot(1, 0)
        self.parameters = params
        if not self.parameters.has_key("id"):
            self.parameters["id"] = "ZeroIntelligenceAgent"
        
        self.sent_orders = False
            
    def process(self, symbol):
        if not self.sent_orders:
            self.sent_orders = True
            for venue in self.orderbooks:
                for price in self.orderbooks[venue]:
                    for o in self.orderbooks[venue][price]:
                        o.parent = self.parameters["id"]
                        self.services.order_dispatcher.new_order(o)
    
    def process_report(self, order_id):
        executions = self.services.bus.get_executions()[order_id]
        for e in executions:
            self.services.publisher.publish("Execution", {"venue": e.symbol, "price": e.price, "size": e.size})    
        
    def process_reject(self, order_id):
        pass 