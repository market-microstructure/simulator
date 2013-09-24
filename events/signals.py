'''
Created on Sep 23, 2013

@author: Silver
'''

from event import Event

Events = {"MarketData"          : Event("MarketData"), 
          "AckNew"              : Event("AckNew"),
          "NackNew"             : Event("NackNew"),
          "Execution"           : Event("Execution"),
          "SnapshotInject"      : Event("SimulatorInject"),
          "ValidNewOrder"       : Event("ValidNewOrder"),
          "ValidModifyOrder"    : Event("ValidModifyOrder"),
          "ValidCancelOrder"    : Event("ValidCancelOrder"),
          "Start"               : Event("Start"),
          "Stop"                : Event("Stop"),        
          }

 
