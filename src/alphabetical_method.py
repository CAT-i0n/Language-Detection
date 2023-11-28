import json
import os


class AlphabeticalMethod:
    def __init__(self, path="./"):
        self.__global_symbol_frequency: dict
        self.__load_symbol_frequensy(path)

    def __load_symbol_frequensy(self, path):

        try:
            file = open('global_symbol_frequency.json', 'r+', encoding="utf-8")
            self.__global_symbol_frequency = json.load(file)
        except:
            file = open('global_symbol_frequency.json', "w")
            self.__global_symbol_frequency = {"eng": {}, "rus": {}}
            folder_path = path + "documents/training"

            for item in os.listdir(folder_path):
                for document in os.listdir(folder_path + "/" + item):
                    local_symbol_amount = self.__count_local_symbol_amount(
                        folder_path + "/" + item + "/" + document)
                    for symbol in local_symbol_amount:
                        self.__global_symbol_frequency[item][symbol] = self.__global_symbol_frequency[item].get(
                            symbol, 0) + local_symbol_amount[symbol]

                self.__calculate_symbol_frequency(
                    self.__global_symbol_frequency[item])

            json.dump(self.__global_symbol_frequency,
                      file, indent=4, ensure_ascii=False)
            file.close()

    @staticmethod
    def __count_local_symbol_amount(path: str) -> 'dict[str: float]':
        local_symbol_amount = {}
        text = open(path).read()
        for symbol in text.lower():
            if symbol.isalpha():
                local_symbol_amount[symbol] = local_symbol_amount.get(
                    symbol, 0) + 1
        return dict(sorted(local_symbol_amount.items()))

    def __calculate_symbol_frequency(self, symbol_amount: 'dict[str, int]') -> 'dict[str, float]':
        symbols_num = sum(symbol_amount.values())
        for symbol, frequency in symbol_amount.items():
            symbol_amount[symbol] /= symbols_num
        return symbol_amount

    def find_language(self, path: str) -> str:
        local_symbol_frequency = self.__calculate_symbol_frequency(self.__count_local_symbol_amount(path))
        distances = {}
        for item in self.__global_symbol_frequency:
            squared_difference = [
                pow(global_frequency - local_symbol_frequency.get(symbol, 0), 2)
                for symbol, global_frequency in self.__global_symbol_frequency[item].items()
            ]
            distances[item] = sum(squared_difference)**0.5
        return min(distances, key=distances.get)

