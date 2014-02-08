

import pandas as pd
from scheduler.ServiceLocator import ServiceLocator
import logging

class ZIInjecter():
    def __init__(self, service_locator, filename):
        self.services = service_locator        
        self.symbol = "Euronext"
     
    def main_loop(self, parameter):
        self.services.events['SnapshotInject'].emit(self.symbol)
            
        