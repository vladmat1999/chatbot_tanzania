from dateutil.parser import parse

important_words = ["appointment", "check medicine", ""]

# Returns a list with the keywords found in the message
def findKeyWords(message, key_words):
    message_words = message.split()
    message_key_words = []
    for key_word in key_words:
        for message_word in message_words:
            if message_word.lower() == key_word.lower():
                message_key_words.append(key_word.lower())
    return message_key_words

#Analyze the main keyword of the message
def analyzeKeyWords(message_kew_words):
    for key_word in message_kew_words:
        if key_word in important_words:
            makeAnswer(key_word)
            break


# Returns a string representing an answer to the message
def makeAnswer(message):

# Makes a request to receive some data
def askForInformation(information):

# Checks if a request for information was made
def informationRequestedFromUser():

# Uses some information to update the user
def getRequestedInformation(message):

#Check if we need any more information
def checkInformationIntegrity(message_key_words):
    for key_word in message_key_words:
        if key_word == "appointment":

