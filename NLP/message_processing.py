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
def makeAnswer(message, user):
    symptoms = findKeyWords(message, symptomList)
    answer_message = makeSuggestion(symptoms)
    return ""

# Makes a request to receive some data about an event
def askForInformation(information, event):
    information_requested = information.lower()
    request_information_message = "Could you tell me "

    if information_requested in ["height", "weight", "blood type", "age"]:
        request_information_message += "your " + information_requested + "?"

    if information_requested == "times":
        request_information_message += " how many times " + event + " occurred?"

    if information_requested == "intensity":
        request_information_message += "on a scale form 1 to 10 how intense is the " + event + "?"

    if information_requested == "past time":
        request_information_message += "what time did the " + event + "happen?"

    if information_requested == "symptom":
        request_information_message += "if you also experienced " + event + "?"

    return request_information_message


# Checks if a request for information was made
def informationRequestedFromUser():
    return 0


# Uses some information to update the user
def getRequestedInformation(message, information, event):
    return 0


def mostProbableDiagnosys(symptoms):
    for diagnosys in diagnosys_list:
        counter = 0
        for symptom in symptoms:
            if symptom in diagnosys.getSymtoms():
                counter += 1
        diagnosys.setMatch(counter / len(diagnosys_list.getSymtoms()) * 100)

    most_probable_diagnosys = diagnosys_list[0]

    for diagnosys in diagnosys_list:
        if most_probable_diagnosys.getMatch() < diagnosys.getMatch():
            most_probable_diagnosys = diagnosys

    return most_probable_diagnosys


def makeSuggestion(symptoms):
    return mostProbableDiagnosys(symptoms).getSuggestion()
#Check if we need any more information
def checkInformationIntegrity(message_key_words):
    for key_word in message_key_words:
        if key_word == "appointment":

