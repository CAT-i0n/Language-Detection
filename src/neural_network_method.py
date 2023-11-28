from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
import os


class NeuralNetworkMethod:
    def __init__(self):
        self.label_dict = {0:"eng", 1:"rus"}
        labels = [*[0] * 5, *[1] * 5]
        folder_path = "./documents/training"
        training_texts = []
        for item in os.listdir(folder_path):
            for document in os.listdir(folder_path + "/" + item):
                training_texts.append(open(folder_path + "/" + item + "/" + document).read())

        self.__vectorizer = TfidfVectorizer()
        training_input = self.__vectorizer.fit_transform(training_texts)
        training_output = labels

        self.__classifier = MLPClassifier()
        self.__classifier.fit(training_input, training_output)

    def predict_language(self, path) -> str:
        text = open(path).read()
        test_input = self.__vectorizer.transform([text])
        return self.label_dict[self.__classifier.predict(test_input)[0]]