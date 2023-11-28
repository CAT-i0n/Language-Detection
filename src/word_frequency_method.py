import json
import os
import re
from pymorphy3 import MorphAnalyzer
from nltk import WordNetLemmatizer
import nltk

try:
    from nltk.corpus import stopwords
except ImportError:
    nltk.download("stopwords")


stop_words_rus = set(stopwords.words('russian'))
stop_words_eng = set(stopwords.words("english"))


class WordFrequency:
    def __init__(self, path="./"):
        self.__global_word_frequency: dict
        self.__rus_lemmatizer = MorphAnalyzer()
        self.__eng_lemmatizer = WordNetLemmatizer()
        self.__load_word_frequensy(path)

    def __load_word_frequensy(self, path):

        try:
            file = open('global_word_frequency.json', 'r+', encoding="utf-8")
            self.__global_word_frequency = json.load(file)
        except:
            file = open('global_word_frequency.json', "w")
            self.__global_word_frequency = {"eng": {}, "rus": {}}
            folder_path = path + "documents/training"

            for item in os.listdir(folder_path):
                for document in os.listdir(folder_path + "/" + item):
                    local_word_amount = self.__count_local_word_amount(
                        folder_path + "/" + item + "/" + document)
                    for word in local_word_amount:
                        self.__global_word_frequency[item][word] = self.__global_word_frequency[item].get(
                            word, 0) + local_word_amount[word]

                self.__calculate_word_frequency(
                    self.__global_word_frequency[item])

            json.dump(self.__global_word_frequency,
                      file, indent=4, ensure_ascii=False)
            file.close()

    def __count_local_word_amount(self, path: str) -> 'dict[str: float]':
        local_word_amount = {}
        text = open(path).read()
        words = self.__get_words(text)
        for word in words:
            if word.isalpha():
                local_word_amount[word] = local_word_amount.get(
                    word, 0) + 1
        return dict(sorted(local_word_amount.items()))

    def __calculate_word_frequency(self, word_amount: 'dict[str, int]') -> 'dict[str, float]':
        words_num = sum(word_amount.values())
        for word, frequency in word_amount.items():
            word_amount[word] /= words_num
        return word_amount

    def find_language(self, path: str) -> str:
        local_word_frequency = self.__calculate_word_frequency(self.__count_local_word_amount(path))
        distances = {}
        for item in self.__global_word_frequency:
            squared_difference = [
                global_frequency - local_word_frequency.get(word, 0)
                for word, global_frequency in self.__global_word_frequency[item].items()
            ]
            distances[item] = sum(squared_difference)
        print(distances)
        return min(distances, key=distances.get)

    def __get_words(self, text):
        text = re.sub('[^А-яЁёA-z]', ' ', text.lower())
        words = self.__normalize_words(text.split(" "))
        return words

    def __normalize_words(self, words):
        for i, word in enumerate(words):
            words[i] = self.__rus_lemmatizer.parse(word)[0].normal_form
            words[i] = self.__eng_lemmatizer.lemmatize(words[i])
        words = [word for word in words if word not in stop_words_rus and word not in stop_words_eng] 
        return words