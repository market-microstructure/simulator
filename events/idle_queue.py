'''
Created on Sep 23, 2013

@author: Silver
'''
#idle_queue.py

import Queue

#Global queue, import it from anywhere, you get the same object instance.
idle_loop = Queue.Queue()

def idle_add(func, *args, **kwargs):
    def idle():
        func(*args, **kwargs)
        return False
    idle_loop.put(idle)