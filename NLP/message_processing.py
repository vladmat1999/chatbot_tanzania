from dateutil.parser import parse
from Diagnosis import Diagnosis
diagnosis_list = []
important_words = ["appointment", "medicine", "check"]


# Returns a list with the keywords found in the message
def find_key_words(message, key_words):
    message_words = message.split()
    message_key_words = []
    for key_word in key_words:
        for message_word in message_words:
            if message_word.lower() == key_word.lower():
                message_key_words.append(key_word.lower())
    return message_key_words

# Returns a string representing an answer to the message
def make_answer(message):
    symptoms = find_key_words(message, ["s1", "s2", "s3", "s4"])
    typeofmessage = find_key_words(important_words)
    if("appointment" in typeofmessage):
        getDoctor(user)

    answer_message = make_suggestion(symptoms)
    return answer_message

# Makes a request to receive some data about an event
def ask_for_information(information, event):
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
def information_requested_from_user():
    return 0


# Uses some information to update the user
def get_requested_information(message, information, event):
    return 0


def most_probable_diagnosis(symptoms):
    global diagnosis_list
    test_initialize_diagnosis_list()

    mpd = diagnosis_list[0]

    for diagnosis in diagnosis_list:
        if mpd.probability(symptoms) < diagnosis.probability(symptoms):
            mpd = diagnosis

    return mpd


def make_suggestion(symptoms):
    return most_probable_diagnosis(symptoms).getSuggestion()


# Check if we need any more information
def check_information_integrity(message_key_words):
    for key_word in message_key_words:
        if key_word == "appointment":
            return 0


def test_initialize_diagnosis_list():
    global diagnosis_list
    diagnosis = Diagnosis("D1", ["s1", "s4"], "suggestion1")
    diagnosis_list.append(diagnosis)

    diagnosis = Diagnosis("D2", ["s1", "s3"], "suggestion2")
    diagnosis_list.append(diagnosis)

    diagnosis = Diagnosis("D2", ["s4", "s2", "s3"], "suggestion3")
    diagnosis_list.append(diagnosis)


if __name__ == "__main__":
    print(make_answer("I sometimes fell odd and i have s1 s3 last night", 0))
    print(make_answer("Today i have seen that my heat s2 and s3", 0))