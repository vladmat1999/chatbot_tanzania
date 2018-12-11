class Diagnosis:
    def __init__(self, name, symptoms, suggestion):
        self.name = name
        self.symptoms = symptoms
        self.suggestion = suggestion

    def getSuggestion(self):
        return self.suggestion

    def setMatch(self, probability):
        self.probability_to_match = probability

    def getMatch(self):
        return self.probability_to_match

    def getSymtoms(self):
        return self.symptoms