import nltk
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


class Interpretation:
    def find_unit_number(self, text):
        keywords = ["unit", "space"]

        words = word_tokenize(text)
        tagged = pos_tag(words)

        noun_numbers = [
            word for word, tag in tagged if word.isdigit() and tag in ["NN", "NNS"]
        ]

        if not noun_numbers:
            return None

        keyword_proximity = []
        for number in noun_numbers:
            proximity = float("inf")
            for keyword in keywords:
                before_index = text.rfind(keyword, 0, text.find(number))
