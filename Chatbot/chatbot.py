import random
import states
from states import Node
from database import *
from difflib import SequenceMatcher

def sendDefault():
    responses = ["I'm sorry, I couldn't understand that","Blah blah blah"]
    print(responses[random.randint(0,len(responses) - 1)])

def sendSuccess(userId, userState, userInfo, message):
    print("Send success")
    
def isAMatch(callOn, message):
    message = message.split()
    for x in message:
        if(x.upper() in callOn):
            return True
    return False

nodes = states.nodes
default = True

while(True):
    default = True

    a = input()
    userId = int(a.split()[0])
    message = ""
    for x in a.split()[1:]:
        message += x + " "

    ID = userId
    
    print(userId, message)

    if(not userExists(ID)):
        insertUser(ID)
        insertUserState(ID, 1)

    userState = getUserState(ID)
    userInfo = getUserInfo(ID)

    print(userState.state, userState.substate, userState.data)


    for x in nodes:
        if(x.state == userState.state and x.substate == userState.substate):
            if(isAMatch(x.callOn, message)):
                default = False
                x.execute(userId, userState, userInfo, message)
    
    if(default):
        sendDefault()

