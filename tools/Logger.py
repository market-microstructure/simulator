'''
Created on Oct 7, 2013

@author: Silver
'''

import logging, sys


class LowerLevelFilter(logging.Filter):
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        """
            this filter helps push messages below a certain level to stdout while leaving the rest to stderr
        """                   
        if self.reject:
            return (record.levelno > self.passlevel)
        else:
            return (record.levelno <= self.passlevel)

def get_logger():
    # create logger
    #logging.basicConfig(format = '%(asctime)s %(levelname)s %(module)s:%(lineno)d >> %(message)s')
    formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(module)s:%(lineno)d\t%(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = []
          
    j = logging.StreamHandler(sys.stderr)     
    j.setLevel(logging.DEBUG)
    j.addFilter(LowerLevelFilter(logging.INFO, True))
    j.setFormatter(formatter)    
        
    h = logging.StreamHandler(sys.stdout)     
    h.setLevel(logging.DEBUG)
    h.addFilter(LowerLevelFilter(logging.INFO, False))
    h.setFormatter(formatter)
    
    root_logger.addHandler(h)
    root_logger.addHandler(j)
        
    return root_logger      
      

