import codecs
import os
import re
import string
import tokenize

import nltk
from serializer import deserialize
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import FreqDist

class NaiveBayesClassifier:
    def __init__(self):
        self.feature_count = {}
        self.category_count = {}

    def probability(self, item, category):
        category_probability = self.get_category_count(category) / sum(self.category_count.values())
        return self.document_probability(item, category) * category_probability

    def document_probability(self, item, category):
        features = self.get_features(item)

        p = 1
        for feature in features:
            print "%s - %s - %s" % (feature, category, self.weighted_probability(feature, category))
            p *= self.weighted_probability(feature, category)

        return p

    def train_from_data(self, data):
        for category, documents in data.items():
            for document in documents:
                self.train(document, category)

    def train(self, document, category):
        features = self.get_features(document)

        for feature in features:
            self.increment_feature(feature, category)

        self.increment_category(category)

    def weighted_probability(self, feature, category, weight=1.0, ap=0.5):
        basic_probability = self.feature_probability(feature, category)
        totals = sum([self.get_feature_count(feature, category) for category in self.category_count.keys()])

        return ((weight * ap) + (totals * basic_probability)) / (weight + totals)

    def feature_probability(self, feature, category):
        if self.get_category_count(category) == 0:
            return 0

        return (self.get_feature_count(feature, category) / self.get_category_count(category))

    def get_category_count(self, category):
        if category in self.category_count:
            return float(self.category_count[category])
        else:
            return 0.0

    def get_feature_count(self, feature, category):
        if feature in self.feature_count and category in self.feature_count[feature]:
            return float(self.feature_count[feature][category])
        else:
            return 0.0

    def increment_category(self, category):
        self.category_count.setdefault(category, 0)
        self.category_count[category] += 1

    def increment_feature(self, feature, category):
        self.feature_count.setdefault(feature, {})
        self.feature_count[feature].setdefault(category, 0)
        self.feature_count[feature][category] += 1

    def glauco_tokenize(self, document):
        splitted = document.split()
        return [x.strip(' ') for x in splitted]

    def get_features(self, document):
        #document = re.sub('[%s]' % re.escape(string.punctuation), '', document) # removes punctuation
        document = document.lower() # make everything lowercase
        #all_words = [w for w in word_tokenize(document) if len(w) > 3 and len(w) < 16]
        all_words = [w for w in word_tokenize(document)]
        #all_words = [w for w in self.glauco_tokenize(document)]
        all_words_freq = FreqDist(all_words)

        # print sorted(all_words_freq.items(), key=lambda(w,c):(-c, w))
        return all_words_freq

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    labels = os.listdir('../data')

    data = { label: deserialize(label) for label in labels }

    nb = NaiveBayesClassifier()
    nb.train_from_data(data)

    code = """
#!/usr/bin/env python
def normalize_space(s):
    \"\"\"Return s stripped of leading/trailing whitespace
    and with internal runs of whitespace replaced by a single SPACE\"\"\"
    # This should be a str method :-(
    return ' '.join(s.split())

    replacement = [normalize_space(i) for i in hello]}return
    """

    results = []
    for language in labels:
        results.append((language, nb.probability(code, language)))

    sorted_results = sorted(results, key = lambda tup: -tup[1])
    print(sorted_results)
