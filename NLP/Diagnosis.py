class Diagnosis:
    def __init__(self, name, symptoms, suggestion):
        self.name = name
        self.symptoms = symptoms
        self.suggestion = suggestion

    def get_suggestion(self):
        return self.suggestion

    def probability(self, symptoms):
        counter = 0
        for symptom in symptoms:
            if symptom in self.symptoms:
                counter += 1
        return counter / len(self.symptoms) * 100

    def get_symptoms(self):
        return self.symptoms