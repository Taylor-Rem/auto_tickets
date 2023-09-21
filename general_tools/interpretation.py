import re
import spacy
import en_core_web_sm
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Load the English NLP model
nlp = en_core_web_sm.load()


class BaseInterpreter:
    def __init__(self):
        pass

    def _tokenize_and_tag(self, text):
        words = word_tokenize(text)
        tagged = pos_tag(words)
        return words, tagged

    def _keyword_proximity(self, text, keywords, numbers):
        words, _ = self._tokenize_and_tag(text)
        if not numbers:
            return None
        keyword_proximity = [
            min(
                abs(words.index(number) - words.index(keyword))
                for keyword in keywords
                if keyword in words
            )
            for number in numbers
        ]
        return numbers[keyword_proximity.index(min(keyword_proximity))]


class TaxInterpreter(BaseInterpreter):
    def determine_operation(self, text):
        keywords = ["monthly taxes", "recurring taxes", "taxes"]
        for keyword in keywords:
            if keyword in text and ("monthly" in keyword or "recurring" in keyword):
                return "add_monthly_taxes"
        return None


class NumberInterpreter(BaseInterpreter):
    def find_nouns_in_text(self, text, limit=4):
        words, tagged = self._tokenize_and_tag(text)
        return [
            word
            for word, pos in tagged
            if word.isdigit() and len(word) <= limit and pos in ["NN", "NNS"]
        ]

    def extract_unit_number(self, text):
        numbers = self.find_nouns_in_text(text)
        unit_number = self._keyword_proximity(text, ["unit", "space", "lot"], numbers)
        return None if unit_number and len(unit_number) > 4 else unit_number

    def extract_dollar_amount(self, text):
        match = re.search(r"\$\s?(\d+(?:,\d{3})*(?:\.\d{2})?)", text)
        return match.group(1) if match else None


class TextInterpreter(BaseInterpreter):
    def extract_resident_name(self, text):
        doc = nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        full_names = [name.split() for name in names if len(name.split()) >= 2]
        if full_names:
            return full_names[0][0], full_names[0][-1]
        return None

    def extract_month(self, text):
        month_pattern = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b"
        match = re.search(month_pattern, text, re.IGNORECASE)
        return match.group() if match else None


class Interpretation(NumberInterpreter, TaxInterpreter, TextInterpreter):
    pass
