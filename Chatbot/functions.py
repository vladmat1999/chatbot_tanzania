from database import *

def sayHello(*args):
    print("Hello")
    setUserState(args[0],0)