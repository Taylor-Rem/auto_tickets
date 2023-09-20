import nltk
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag


class Interpretation:
    @staticmethod
    def _tokenize_and_tag(text):
        words = word_tokenize(text)
        tagged = pos_tag(words)
        return words, tagged

    @staticmethod
    def _keyword_proximity(text, keywords):
        words, _ = Interpretation._tokenize_and_tag(text)
        numbers_in_text = [word for word in words if word.isdigit()]

        if not numbers_in_text:
            return None

        keyword_proximity = []
        for number in numbers_in_text:
            proximity = float("inf")
            for keyword in keywords:
                if keyword in words:
                    before_distance = abs(words.index(number) - words.index(keyword))
                    proximity = min(proximity, before_distance)
            keyword_proximity.append(proximity)

        return numbers_in_text[keyword_proximity.index(min(keyword_proximity))]

    @staticmethod
    def determine_operation(title, description):
        text = title + " " + description.lower()

        # Check for patterns
        if re.search(r"monthly.*taxes", text):
            return "add_monthly_taxes"
        if re.search(r"remove.*\$\d+\.\d{2}", text) or re.search(
            r"delete.*\$\d+\.\d{2}", text
        ):
            return "delete_transaction"
        if re.search(r"move payment from unit \d+ to \d+", text):
            return "move_payment"

        return None

    def extract_unit_number(self, text):
        return self._keyword_proximity(text, ["unit", "space", "lot"])

    def extract_resident_name(self, text):
        keywords = ["resident", "tenant"]
        words, tagged = self._tokenize_and_tag(text)

        for i, (word, tag) in enumerate(tagged):
            if word.lower() in keywords and i < len(tagged) - 1:
                potential_name = []
                j = i + 1
                while j < len(tagged) and tagged[j][1] in ["NNP", "NNPS"]:
                    potential_name.append(tagged[j][0])
                    j += 1
                if potential_name:
                    return " ".join(potential_name)

        # If no names found next to "resident" or "tenant", return any name in the text.
        names = [word for word, tag in tagged if tag in ["NNP", "NNPS"]]
        if names:
            return " ".join(names)

        return None
