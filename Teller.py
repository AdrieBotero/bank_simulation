'''
Created on Oct 5, 2014

@author: andreasbotero
'''
from Queue import Queue
class Teller:
    
    '''
    classdocs
    '''


    def __init__(self, number):
        
        self.line_of_customers = Queue()
        self.idle_time = 0
        self.number = number