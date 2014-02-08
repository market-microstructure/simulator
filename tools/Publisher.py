'''
Created on Nov 2, 2013

@author: Silver
'''
import pandas as pd

class Publisher:
    def __init__(self, services, filepath):
        self.services = services
        self.filepath = filepath
        
    def publish(self, id, indicators):
        # indicators is in dictionary format.
        indicators["id"] = id
        self.services.logger.info("Publishing new data: %s " % indicators)
        """        
        if self.services.bus.get_indicators().empty(): 
            self.services.bus._indicators = pd.DataFrame(indicators, index = [0])
            return
        """
        
        # TODO: optimization problem here. (don't use dataframes? )                
        df = self.services.bus._indicators
        self.services.bus._indicators = df.append(pd.DataFrame(indicators, index = [len(df)]))
        
    def export(self, id):
        df = self.services.bus.get_indicators()
        df.to_csv(self.filepath + "/%s.csv" % self.services.simulation["id"], sep = ";")
            
            
        
        
        
        
        