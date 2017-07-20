from lxml import html
import requests


class HighlightedSourceSpider:
    def __init__(self, tree):
        self.tree = tree

    def run(self, klass):
        query = '//pre[contains(@class, "%s")]//text()' % klass
        snippet = self.tree.xpath(query)
        return ''.join(snippet)


class HighlightedSourceFinder:
    def __init__(self, tree):
        self.tree = tree

    def find(self):
        query = '//pre[contains(@class, "highlighted_source")]/@class'
        klasses = self.tree.xpath(query)
        ignored = ['text highlighted_source']
        return filter(lambda klass: klass not in ignored, klasses)


class RosettaCodeSpider:
    def __init__(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        self.finder = HighlightedSourceFinder(tree)
        self.spider = HighlightedSourceSpider(tree)

    def run(self):
        klasses = self.finder.find()
        languages = map(lambda klass: klass.split()[0], klasses)
        sources = [self.spider.run(klass) for klass in klasses]
        return {language: source
                for (language, source)
                in zip(languages, sources)}


class ExerciseFinder:
    def __init__(self, tree):
        self.tree = tree

    def find(self):
        query = '//td[contains(@class, "smwtype_wpg")]//@href'
        return self.tree.xpath(query)


class RosettaExerciseSpider:
    def __init__(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        self.finder = ExerciseFinder(tree)

    def run(self):
        exercises = self.finder.find()
        return [u'https://rosettacode.org%s' % exercise
                for exercise
                in exercises]
