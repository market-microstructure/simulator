'''
Created on Sep 23, 2013

@author: Silver
'''
import pandas as pd
from scheduler.ServiceLocator import ServiceLocator
import logging

class Level1FastInjecter():
    def __init__(self, service_locator, filename):
        self.services = service_locator
        self.filename = filename
        self.symbol = "a"
     
    def main_loop(self, parameter):
        data = pd.read_csv(self.filename, sep = ';')
        for i in range(len(data)):
            row = data.ix[i] 
            logging.info(1, "injecting row: %s" % row)     
            
            self.services.bus.inject_snapshot(self.symbol, row)
            self.services.events['SnapshotInject'].emit(self.symbol)
            
        
        
         
            