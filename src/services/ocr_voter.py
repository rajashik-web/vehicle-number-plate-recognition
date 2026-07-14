from collections import Counter


class OCRVoter:

    def __init__(self):

        self.results = []

    def add(self, text):

        if text != "":
            self.results.append(text)

    def best_result(self):

        if len(self.results) == 0:
            return ""

        counter = Counter(self.results)

        return counter.most_common(1)[0][0]

    def clear(self):

        self.results.clear()