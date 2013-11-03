'''
Created on Nov 1, 2013

@author: Silver
'''
import pandas as pd
from datetime import datetime, timedelta

class Level2HDFInjecter():
    def __init__(self, service_locator, filename):
        self.services = service_locator
        self.filename = filename
        self.symbol = "a" # TODO
     
    def main_loop(self, parameter):
        data = pd.HDFStore(self.filename, "r")
        orderbooks = data.get("/df_obs")
        trades     = data.get("/df_trades")
        
        i_ob = 0
        i_tr = 0
        
        while i_ob < len(orderbooks) or i_tr < len(trades): 
            # decide which event to insert
            if i_tr >= len(trades) or orderbooks.ix[i_ob]["ts_recv"] <= trades.ix[i_tr]["ts_market"]:                
                row = orderbooks.ix[i_ob]
                i_ob += 1
                
                if row["Pbid 1"] == 0 or row["Pask 1"] == 0: continue                    
                
                snapshot = {"time": row["ts_recv"],
                            "bid-0": {"price": row["Pbid 1"], "size": row["Qbid 1"]},
                            "bid-1": {"price": row["Pbid 2"], "size": row["Qbid 2"]},
                            "bid-2": {"price": row["Pbid 3"], "size": row["Qbid 3"]},
                            "bid-3": {"price": row["Pbid 4"], "size": row["Qbid 4"]},
                            "bid-4": {"price": row["Pbid 5"], "size": row["Qbid 5"]},
                            
                            "ask-0": {"price": row["Pask 1"], "size": row["Qask 1"]},
                            "ask-1": {"price": row["Pask 2"], "size": row["Qask 2"]},
                            "ask-2": {"price": row["Pask 3"], "size": row["Qask 3"]},
                            "ask-3": {"price": row["Pask 4"], "size": row["Qask 4"]},
                            "ask-4": {"price": row["Pask 5"], "size": row["Qask 5"]},
                            "depth": 5,
                            "event": "lob"                            
                            }
                                
                self.services.logger.info("injecting orderbook row: %s" % snapshot)
                self.services.bus.inject_snapshot(self.symbol, snapshot)
                self.services.events['SnapshotInject'].emit(self.symbol)
                
            else:
                row = trades.ix[i_tr]
                i_tr += 1
                if row["qty"] == 0: continue;
                
                snapshot = {"time": row["ts_market"],
                            "last": {"price": row["price"], "quantity": row["qty"], "exchange": row["source"], "side": row["side"], "type": row["type"]},
                            "stats": {"volume": row["volume"], "vwap": row["vwap"]},
                            "event": "trade"  
                            }
                
                self.services.logger.info("injecting trades row: %s" % snapshot)
                self.services.bus.inject_snapshot(self.symbol, snapshot)
                self.services.events['SnapshotInject'].emit(self.symbol)
                
                
            
            
            
            
        