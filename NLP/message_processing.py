# Returns a list with the keywords found in the message
def findKeyWords(message, keyWords):
    messageWords = message.split()
    messageKeyWords = []
    for keyWord in keyWords:
        for messageWord in messageWords:
            if messageWord.lower() == keyWord.lower():
                messageKeyWords.append(keyWord.lower())
    return messageKeyWords

# Returns a string representing an answer to the message
def makeAnswer(message):

# Makes a request to receive some data
def askForInformation(information):

# Checks if a request for information was made
def informationRequestedFromUser():

# Uses some information to update the user
def getRequestedInformation(message):

#test