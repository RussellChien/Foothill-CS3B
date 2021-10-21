import json
from enum import Enum
from datalist import *


class DictionaryEntry:
    def __init__(self, word, part_of_speech, definition, example=None):
        self.word = word
        self.part_of_speech = part_of_speech
        self.definition = definition
        self.example = example

    def __str__(self):
        s = '\n'
        return str(self.word) + s + self.part_of_speech + s + self.definition + s + str(self.example)


class LocalDictionary:
    def __init__(self, dictionary_json_name="dictionary.json"):
        with open(dictionary_json_name) as file:
            self.data = []

            json.load(file, object_hook=self.decode)

    def decode(self, file):
        if 'word' in file:
            self.decoder_helper(file)
        return file

    def decoder_helper(self, entry):
        word = entry["word"]
        part_of_speech = entry["partOfSpeech"]
        definition = entry["definition"]
        if 'example' in entry:
            example = entry["example"]
            self.data.append(DictionaryEntry(word, part_of_speech, definition, example))
        else:
            self.data.append(DictionaryEntry(word, part_of_speech, definition))

    def search(self, word):
        for i in self.data:
            if word == i.word:
                return i
        raise KeyError("Word not found.")


class DictionaryEntryCache(DataList):
    def __init__(self, capacity=10):
        super().__init__()
        if capacity < 1:
            raise ValueError("Invalid Capacity")
        self.capacity = capacity
        self.counter = 0

    def add(self, entry):
        if not isinstance(entry, DictionaryEntry):
            raise TypeError("Invalid Entry")
        if self.counter < self.capacity:
            super().add_to_head(entry)
            self.counter += 1
        else:
            self.remove()
            super().add_to_head(entry)

    def remove(self):
        temp = self.head
        while temp:
            if temp.next.next is None:
                temp.remove_after()
                return True
            temp = temp.next
        return False

    def search(self, word):
        temp = self.head
        while temp.next:
            if temp.next.data.word == word:
                return temp.next.data
            temp = temp.next


class DictionarySource(Enum):
    CACHE = '(CACHE)'
    LOCAL = '(LOCAL)'


class Dictionary:
    def __init__(self, size):
        self.local_dictionary = LocalDictionary()
        self.dictionary_cache = DictionaryEntryCache(size)

    def search(self, word):
        search = self.dictionary_cache.search(word)
        if isinstance(search, DictionaryEntry):
            return '{}\n{}'.format(str(search), DictionarySource.CACHE)
        search = self.local_dictionary.search(word)
        if isinstance(search, DictionaryEntry):
            self.dictionary_cache.add(search)
            return '{}\n{}'.format(str(search), DictionarySource.LOCAL)


def main():
    dictionary = Dictionary(2)
    for i in range(10):
        search = input("Search a word to define:")
        print(str(dictionary.search(search))+"\n")


if __name__ == '__main__':
    main()
