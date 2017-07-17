import codecs
import os
import sys

def serialize(content):
    for language, snippet in content.iteritems():
        source = codecs.open(language, 'w', 'utf-8')

        for line in snippet:
            source.write('%s' % line)

        source.close()

def deserialize(filename):
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    os.chdir('../data')
    source = codecs.open(filename, 'r', 'utf-8')
    data = source.readlines()
    source.close()

    return data
