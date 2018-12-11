from dateutil.parser import parse
from Diagnosis import Diagnosis

important_words = ["appointment", "medicine", "check"]
diagnosis_list = testInitializeDiagnosisList()

# Returns a list with the keywords found in the message
def findKeyWords(message, key_words):
    message_words = message.split()
    message_key_words = []
    for key_word in key_words:
        for message_word in message_words:
            if message_word.lower() == key_word.lower():
                message_key_words.append(key_word.lower())
    return message_key_words

# Returns a string representing an answer to the message
def makeAnswer(message):
    medicinenames = findKeyWords(message, )
    symptoms = findKeyWords(message, symptomList)
    typeofmessage = findKeyWords(important_words)
    if"appointment" in typeofmessage:
        return "Contact the doctor at the link to arrange an appointment, he will tell you the time and place: " + getDoctor(user);
    elif("medicine" in typeofmessage) and ("check" in typeofmessage):
        if


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


def mostProbableDiagnosis(symptoms):
    global diagnosis_list
    for diagnosis in diagnosis_list:
        counter = 0
        for symptom in symptoms:
            if symptom in diagnosis.getSymtoms():
                counter += 1
        diagnosis.setMatch(counter / len(diagnosis_list.getSymtoms()) * 100)

    most_probable_diagnosis = diagnosis_list[0]

    for diagnosis in diagnosis_list:
        if most_probable_diagnosis.getMatch() < diagnosis.getMatch():
            most_probable_diagnosis = diagnosis

    return most_probable_diagnosis


def makeSuggestion(symptoms):
    return mostProbableDiagnosis(symptoms).getSuggestion()


#Check if we need any more information
def checkInformationIntegrity(message_key_words):
    for key_word in message_key_words:
        if key_word == "appointment":

def testInitializeDiagnosisList():
    diagnosis = Diagnosis()