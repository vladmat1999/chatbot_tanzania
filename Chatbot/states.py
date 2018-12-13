from functions import *

class Node():
    name = ""
    callOn = []
    state = None
    substate = None
    execute = None

    def __init__(self,callOn, state, execute, substate = 0, name = ""):
        self.callOn = callOn;
        self.state = state;
        self.execute = execute;
        self.name = name;
        self.substate = substate

nodes=[]

nodes.append(Node(["HELLO"], 1, sayHello))
