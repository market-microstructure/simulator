'''
Created on Sep 23, 2013

@author: Silver
'''
from event import Event
from idle_queue import idle_loop
import sys

class _Events:
    #add some signals, example:
    #do_something = Event('do something') #args: my_arg1, my_arg_list2, my_arg_str3
    quit_app = Event('quit app') #args: some_arg

events = _Events()

if __name__ == "__main__":
    def quitter(some_arg):
        print some_arg
        sys.exit(0)

    events.quit_app.connect(quitter) #connect the callback/slot
    #events.quit_app.disconnect(quit) #disconnect
    something = "goodbye"
    events.quit_app.emit(something) #emit the signal
    
    #this should go in your main thread loop if your are using a gui.
    #example: http://code.activestate.com/recipes/578299-pyqt-pyside-thread-safe-global-queue-main-loop-int/
    callback = idle_loop.get()
    callback() #dispatch the event