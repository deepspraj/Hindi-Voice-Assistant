import pandas as pd
from spacy.lang.hi import Hindi
from os.path import abspath, dirname, join
from sklearn.neighbors import KNeighborsClassifier


BASE_DIR = abspath(dirname(__file__))


class SymptomsDiagnosis:

    def __init__(self):
        # Reading the dataset from csv file
        self.dataset = pd.read_csv(join(BASE_DIR, "dataset", "datasetNew.csv"))

        # Spacy instance for stemming hindi words
        self.stemmer = Hindi()

        # Split the dataset in Independent Variable (X) and Dependent Variable (Y)
        self.Y = self.dataset['Disease']
        self.X = self.dataset.drop('Disease', axis=1)

        # Getting all symptoms 
        self.all_symptoms = list(set([x for x in (','.join(self.X['Symptoms'])).split(',')]))

        # Stemming all the symptoms
        # self.stemmed_symptoms = [self.stemmer.pipe(symptoms).text for symptoms in self.all_symptoms]
        self.stemmed_symptoms = list(self.stemmer.pipe(self.all_symptoms))

    def __symptoms_vectorizer(self, symptoms):
        """
        Vectorize all the user symptoms accoring to sequence of self.stemmed_symptoms
        """

        user_symptoms = []

        # stem all the user symptoms
        for symptom in list(self.stemmer.pipe(symptoms)):
          symptom = str(symptom).strip()
          if symptom not in user_symptoms:
            user_symptoms.append(symptom)

        # vectorize user symtoms
        vector = []
        for symptom in self.stemmed_symptoms:
            if str(symptom) in user_symptoms:
                vector.append(1)
            else:
                vector.append(0)

        return vector

    def __diseases_vectorizer(self):
        """
        Vectorize disease accoring to sequence of self.Y
        """
        # list to keep track of disease
        diseases_done = []

        vector = []
        count = 0

        for disease in self.Y:
            if disease in diseases_done:
                vector.append(diseases_done.index(str(disease)))
            else:
                vector.append(count)
                diseases_done.append(disease)
                count += 1

        return vector


    def __traindata(self):
        
        # vector of independent variable 
        independent = []
        for symptoms in self.X['Symptoms']:
            independent.append(self.__symptoms_vectorizer(symptoms.split(',')))

        # vector of response variable 
        dependent = self.__diseases_vectorizer()

        # ml model
        self.knn = KNeighborsClassifier(n_neighbors=10, p=3, metric='minkowski',weights='distance')

        # train model 
        self.knn.fit(independent, dependent)

        # acknowledge user about training 
        print("Done with Training")
        return True

    def __suggest_symptoms(self, user_symptoms):

        predicted_disease = self.__disease_prediction(user_symptoms)
        next_symptom = list(set(self.stemmed_symptoms[predicted_disease]) - set(user_symptoms))
        return next_symptom


    def symptoms_suggester(self, symptoms_from_user):
        return self.__suggest_symptoms(symptoms_from_user)


    def vectorizer(self,  user_symptoms):
        return self.__symptoms_vectorizer(user_symptoms)


    def train(self):
        return self.__traindata()


    def __disease_prediction(self, user_symptoms):
        
        # convert all the symptoms user stated to vector
        test_data = self.__symptoms_vectorizer(user_symptoms)

        # perform predict on test_data on ml model 
        predicted_disease = self.Y[self.knn.predict([test_data])]
        
        return predicted_disease

    def predict(self, user_symptoms):
        return self.__disease_prediction(user_symptoms)[:2]



    # Method for debugging purpose
    def printer(self):
        print(self.dataset)

if __name__ == "__main__":
    obj = SymptomsDiagnosis()
    obj.train()