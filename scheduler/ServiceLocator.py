'''
Created on Sep 23, 2013

@author: Silver
'''

class ServiceLocator():
    def __init__(self):
        self.scheduler = []
        self.matching_engine = []
        self.bus = []
        self.rulebook = []
        self.injecter = []
        self.events = []
        self.order_dispatcher = []
        