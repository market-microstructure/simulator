'''
Created on Feb 8, 2014

@author: Silver
'''

from objects.Order import *

class SORAgent():
    def __init__(self, service_locator, params):
        self.services = service_locator
        self.parameters = params
        if not self.parameters.has_key("id"):
            self.parameters["id"] = "ZeroIntelligenceAgent"
    
    def process(self, symbol):        
        data = self.services.bus.get_market_data()        
        self.services.logger.info("Market data received %s" % (data))
        
        self.services.logger.info("Sending Order Now:")
        o = Order()
        o.side = 1 if str(self.parameters["side"]).lower() == "buy" else -1
        o.price = self.parameters["price"]
        o.size = self.parameters["size"]
        o.leaves = o.size
        o.symbol = "Euronext"
        o.id = "MyOrder"
        o.timeinforce = "ioc"
        o.parent = self.parameters["id"]
        
        self.services.order_dispatcher.new_order(o)
        
    def process_report(self, id):
        execs = self.services.bus.get_executions()[id]
        self.services.logger.info("execution!!!!!!!!!!!!" + str(id)  + " number: " +  str(len(execs)))
        for e in execs:
            self.services.logger.info( e)
            
            
    def process_reject(self, order_id):
        reject = self.services.bus.get_rejects()[order_id]        
        self.services.logger.info("reject: %s. RemainingQty: %d" % (order_id, reject.leaves))