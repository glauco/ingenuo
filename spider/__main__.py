import codecs
import os
import sys

from lib import RosettaExerciseSpider
from lib import RosettaCodeSpider


def serialize(solutions):
    for language, code in solutions.iteritems():
        source = codecs.open(language, 'w', 'utf-8')
        source.writelines(code)
        source.close()


def run(args):
    destination = args[1]

    if not os.path.exists(destination):
        os.mkdir(destination)

    os.chdir(destination)

    exercise_spider = RosettaExerciseSpider('https://bit.ly/2vCQ6sg')
    exercise_urls = exercise_spider.run()

    for exercise_url in exercise_urls:
        print(u'downloading exercise data from: %s' % exercise_url)
        code_spider = RosettaCodeSpider(exercise_url)
        code = code_spider.run()
        serialize(code)

if __name__ == '__main__':
    run(sys.argv)
