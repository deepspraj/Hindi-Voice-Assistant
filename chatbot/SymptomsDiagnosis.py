import pandas as pd
from spacy.lang.hi import Hindi
from os.path import abspath, dirname, join
from sklearn.neighbors import KNeighborsClassifier

response_variable = 'बीमारी'

BASE_DIR = abspath(dirname(__file__))


class SymptomsDiagnosis:

    def __init__(self):
        # Reading the dataset from csv file
        self.dataset = pd.read_excel(join(BASE_DIR, "dataset.xlsx"))

        # Spacy instance for stemming hindi words
        self.stemmer = Hindi()

        # Split the dataset in Independent Variable (X) and Dependent Variable (Y)
        self.Y = self.dataset[response_variable]
        self.X = self.dataset.drop([response_variable, 'नहीं'], axis=1)

        # Getting all symptoms 
        self.all_symptoms = self.X.columns

        # Stemming all the symptoms
        # self.stemmed_symptoms = [self.stemmer.pipe(symptoms).text for symptoms in self.all_symptoms]
        self.stemmed_symptoms = list(self.stemmer.pipe(self.all_symptoms))

    def __symptoms_vectorizer(self, symptoms):
        """
        Vectorize all the user symptoms accoring to sequence of self.stemmed_symptoms
        """

        # vectorize user symtoms for testing data
        vector = []
        for symptom in self.stemmed_symptoms:
            if str(symptom) in symptoms:
                vector.append(1)
            else:
                vector.append(0)

        return vector

    def __traindata(self):        

        # ml model
        self.knn = KNeighborsClassifier(n_neighbors=10, p=3, metric='minkowski',weights='distance')

        # train model 
        self.knn.fit(self.X, self.Y)

        # acknowledge user about training 
        print("Done with Training")
        return True

    def __suggest_symptoms(self, user_symptoms, suggested_so_far):

        # method 1: but not working 
        # next_symptom = list(set(self.stemmed_symptoms) - set(user_symptoms))
        
        next_symptom = []
        for symp in self.stemmed_symptoms:
            if str(symp) not in user_symptoms and str(symp) not in suggested_so_far:
                next_symptom.append(str(symp))
        
        return next_symptom


    def symptoms_suggester(self, symptoms_from_user, suggested_so_far):
        return self.__suggest_symptoms(symptoms_from_user, suggested_so_far)


    def vectorizer(self,  user_symptoms):
        return self.__symptoms_vectorizer(user_symptoms)


    def train(self):
        return self.__traindata()


    def __disease_prediction(self, user_symptoms):
        
        # convert all the symptoms user stated to vector
        test_data = self.__symptoms_vectorizer(user_symptoms)

        # perform predict on test_data on ml model
        print(self.knn.predict([test_data]))
        predicted_disease = self.Y[self.knn.predict([test_data])[0]]
        
        return predicted_disease

    def predict(self, user_symptoms):
        return self.__disease_prediction(user_symptoms)



    # Method for debugging purpose
    def printer(self):
        print(self.dataset)

if __name__ == "__main__":
    obj = SymptomsDiagnosis()
    obj.train()