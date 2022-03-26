import pandas as pd

class SymptomsDiagnosis:

    def __init__(self):
        self.dataset = pd.read_csv("./dataset/dataset.csv")
        self.dataset.drop(self.dataset.columns[10:], axis=1, inplace=True)
        self.dataset.fillna('नहीं है', inplace=True)

    def printer(self):
        print(self.dataset)

if __name__ == "__main__":
    obj = SymptomsDiagnosis()
    obj.printer()