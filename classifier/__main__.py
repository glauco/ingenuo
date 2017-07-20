import codecs
import sys
import os

from lib import NaiveBayesClassifier

def deserialize(filename):
    source = codecs.open(filename, 'r', 'utf-8')
    data = source.readlines()
    source.close()

    return data

def run(args):
    source = args[1]
    os.chdir(source)

    labels = os.listdir('.')
    data = {label: deserialize(label) for label in labels}

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

    results = results[0:10]

    sorted_results = sorted(results, key = lambda tup: -tup[1])
    print(sorted_results)

if __name__ == '__main__':
    run(sys.argv)
