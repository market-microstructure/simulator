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
        self.services.logger.info("Publishing new data: %s " % indicators)        
        if not self.services.bus.get_indicators().has_key(id): 
            self.services.bus.get_indicators()[id] = pd.DataFrame(indicators, index = [0])
            return
        
        # TODO: optimization problem here. (don't use dataframes? )
                
        df = self.services.bus.get_indicators()[id]
        self.services.bus.get_indicators()[id] = df.append(pd.DataFrame(indicators, index = [len(df)]))
        
        
        
        
        
        
    def export(self, id):
        for k, v in self.services.bus.get_indicators().iteritems():
            v.to_csv(self.filepath + "/%s_export.csv" % k, sep = ";")
            
            
        
        
        
        
        