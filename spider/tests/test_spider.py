from lxml import html
import requests
import responses
import unittest

from spider.lib import ExerciseFinder
from spider.lib import HighlightedSourceFinder
from spider.lib import HighlightedSourceSpider
from spider.lib import RosettaCodeSpider
from spider.lib import RosettaExerciseSpider


class SpiderTest(unittest.TestCase):

    @responses.activate
    def setUp(self):
        self.url = 'https://rosettacode.org/wiki/Hello_world/Line_printer'
        body = """
<html>
<body>
<div id="toc" class="toc">
  <div id="toctitle"><h2>Contents</h2><span class="toctoggle">&nbsp;[<a href="#" id="togglelink">hide</a>]&nbsp;</span></div>
  <li class="toclevel-1 tocsection-2"><a href="#Ada"><span class="tocnumber">2</span> <span class="toctext">Ada</span></a>
  <ul>
  <li class="toclevel-2 tocsection-3"><a href="#Unix"><span class="tocnumber">2.1</span> <span class="toctext">Unix</span></a></li>
  </ul>
  </li>
</div>
<h2><span class="mw-headline" id="Ada"><a href="/wiki/Category:Ada" title="Category:Ada">Ada</a></span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/mw/index.php?title=Hello_world/Line_printer&amp;action=edit&amp;section=2" title="Edit section: Ada">edit</a><span class="mw-editsection-bracket">]</span></span></h2>
<pre class="ada highlighted_source">&nbsp;<br><span class="kw3">with</span> Ada.<span class="me1">Text_IO</span>; <span class="kw3">use</span> Ada.<span class="me1">Text_IO</span>;<br>&nbsp;<br><span class="kw3">procedure</span> Print_Line <span class="kw1">is</span><br>   Printer&nbsp;: File_Type;<br><span class="kw1">begin</span><br>   <span class="kw1">begin</span><br>      Open <span class="br0">(</span>Printer, Mode =&gt; Out_File, Name =&gt; <span class="st0">"/dev/lp0"</span><span class="br0">)</span>;<br>   <span class="kw1">exception</span><br>      <span class="kw3">when</span> <span class="kw3">others</span> =&gt;<br>         Put_Line <span class="br0">(</span><span class="st0">"Unable to open printer."</span><span class="br0">)</span>;<br>         <span class="kw1">return</span>;<br>   <span class="kw1">end</span>;<br>&nbsp;<br>   Set_Output <span class="br0">(</span>Printer<span class="br0">)</span>;<br>   Put_Line <span class="br0">(</span><span class="st0">"Hello World!"</span><span class="br0">)</span>;<br>   Close <span class="br0">(</span>Printer<span class="br0">)</span>;<br><span class="kw1">end</span> Print_Line;<br>&nbsp;</pre>
<h2><span class="mw-headline" id="Python"><a href="/wiki/Category:Python" title="Category:Python">Python</a></span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/mw/index.php?title=Hello_world/Line_printer&amp;action=edit&amp;section=58" title="Edit section: Python">edit</a><span class="mw-editsection-bracket">]</span></span></h2>
<pre class="python highlighted_source">lp <span class="sy0">=</span> <span class="kw2">open</span><span class="br0">(</span><span class="st0">"/dev/lp0"</span><span class="br0">)</span><br>lp.<span class="me1">write</span><span class="br0">(</span><span class="st0">"Hello World!<span class="es0">\n</span>"</span><span class="br0">)</span><br>lp.<span class="me1">close</span><span class="br0">(</span><span class="br0">)</span></pre>
</body>
</html>"""

        responses.add(**{
            'method': responses.GET,
            'url': self.url,
            'body': body,
            'status': 200,
            'content_type': 'text/html',
            })

        page = requests.get(self.url)
        self.tree = html.fromstring(page.content)


class TestHighlightedSourceSpider(SpiderTest):

    def test_it_retrieves_the_first_highlighted_source_code(self):
        expected = [
                u'\xa0with Ada.Text_IO; use Ada.Text_IO;',
                u'\xa0procedure Print_Line is   Printer\xa0: ',
                u'File_Type;begin   begin      Open (Printer, Mode => ',
                u'Out_File, Name => "/dev/lp0");   exception      when ',
                u'others =>         Put_Line ("Unable to open ',
                u'printer.");         return;   end;\xa0   Set_Output ',
                u'(Printer);   Put_Line ("Hello World!");   ',
                u'Close (Printer);end Print_Line;\xa0']

        spider = HighlightedSourceSpider(self.tree)
        source = spider.run('ada highlighted_source')
        self.assertEqual(source, ''.join(expected))

    def test_it_retrieves_the_second_highlighted_source_codes(self):
        expected = [
                u'lp = open("/dev/lp0")',
                u'lp.write("Hello World!\n")',
                u'lp.close()']

        spider = HighlightedSourceSpider(self.tree)
        source = spider.run('python highlighted_source')
        self.assertEqual(source, ''.join(expected))


class TestHighlightedSourceFinder(SpiderTest):

    def test_it_finds_a_code_snippet(self):
        expected = [
                u'ada highlighted_source',
                u'python highlighted_source']

        finder = HighlightedSourceFinder(self.tree)
        klasses = finder.find()
        self.assertEqual(klasses, expected)


class TestRosettaCodeSpider(unittest.TestCase):

    def setUp(self):
        self.url = 'https://rosettacode.org/wiki/Hello_world/Line_printer'
        body = """
<html>
<body>
<div id="toc" class="toc">
  <div id="toctitle"><h2>Contents</h2><span class="toctoggle">&nbsp;[<a href="#" id="togglelink">hide</a>]&nbsp;</span></div>
  <li class="toclevel-1 tocsection-2"><a href="#Ada"><span class="tocnumber">2</span> <span class="toctext">Ada</span></a>
  <ul>
  <li class="toclevel-2 tocsection-3"><a href="#Unix"><span class="tocnumber">2.1</span> <span class="toctext">Unix</span></a></li>
  </ul>
  </li>
</div>
<h2><span class="mw-headline" id="Ada"><a href="/wiki/Category:Ada" title="Category:Ada">Ada</a></span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/mw/index.php?title=Hello_world/Line_printer&amp;action=edit&amp;section=2" title="Edit section: Ada">edit</a><span class="mw-editsection-bracket">]</span></span></h2>
<pre class="ada highlighted_source">&nbsp;<br><span class="kw3">with</span> Ada.<span class="me1">Text_IO</span>; <span class="kw3">use</span> Ada.<span class="me1">Text_IO</span>;<br>&nbsp;<br><span class="kw3">procedure</span> Print_Line <span class="kw1">is</span><br>   Printer&nbsp;: File_Type;<br><span class="kw1">begin</span><br>   <span class="kw1">begin</span><br>      Open <span class="br0">(</span>Printer, Mode =&gt; Out_File, Name =&gt; <span class="st0">"/dev/lp0"</span><span class="br0">)</span>;<br>   <span class="kw1">exception</span><br>      <span class="kw3">when</span> <span class="kw3">others</span> =&gt;<br>         Put_Line <span class="br0">(</span><span class="st0">"Unable to open printer."</span><span class="br0">)</span>;<br>         <span class="kw1">return</span>;<br>   <span class="kw1">end</span>;<br>&nbsp;<br>   Set_Output <span class="br0">(</span>Printer<span class="br0">)</span>;<br>   Put_Line <span class="br0">(</span><span class="st0">"Hello World!"</span><span class="br0">)</span>;<br>   Close <span class="br0">(</span>Printer<span class="br0">)</span>;<br><span class="kw1">end</span> Print_Line;<br>&nbsp;</pre>
<h2><span class="mw-headline" id="Python"><a href="/wiki/Category:Python" title="Category:Python">Python</a></span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/mw/index.php?title=Hello_world/Line_printer&amp;action=edit&amp;section=58" title="Edit section: Python">edit</a><span class="mw-editsection-bracket">]</span></span></h2>
<pre class="python highlighted_source">lp <span class="sy0">=</span> <span class="kw2">open</span><span class="br0">(</span><span class="st0">"/dev/lp0"</span><span class="br0">)</span><br>lp.<span class="me1">write</span><span class="br0">(</span><span class="st0">"Hello World!<span class="es0">\n</span>"</span><span class="br0">)</span><br>lp.<span class="me1">close</span><span class="br0">(</span><span class="br0">)</span></pre>
</body>
</html>"""

        responses.add(**{
            'method': responses.GET,
            'url': self.url,
            'body': body,
            'status': 200,
            'content_type': 'text/html',
            })

    @responses.activate
    def test_it_retrieves_all_highlighted_source_code(self):
        ada = [
                u'\xa0with Ada.Text_IO; use Ada.Text_IO;',
                u'\xa0procedure Print_Line is   Printer\xa0: ',
                u'File_Type;begin   begin      Open (Printer, Mode => ',
                u'Out_File, Name => "/dev/lp0");   exception      when ',
                u'others =>         Put_Line ("Unable to open ',
                u'printer.");         return;   end;\xa0   Set_Output ',
                u'(Printer);   Put_Line ("Hello World!");   ',
                u'Close (Printer);end Print_Line;\xa0']

        python = [
                u'lp = open("/dev/lp0")',
                u'lp.write("Hello World!\n")',
                u'lp.close()']

        expected = {
                u'ada': ''.join(ada),
                u'python': ''.join(python)}

        spider = RosettaCodeSpider(self.url)
        content = spider.run()
        self.assertEqual(content, expected)


class TestExerciseSpider(unittest.TestCase):

    @responses.activate
    def setUp(self):
        self.url = 'https://bit.ly/2vCQ6sg'
        body = """
<html>
<body>
<table>
  <tbody>
    <tr class="row-odd"><td class="smwtype_wpg"><a href="/wiki/Set_puzzle" title="Set puzzle">Set puzzle</a></td></tr>
    <tr class="row-even"><td class="smwtype_wpg"><a href="/wiki/Ordered_words" title="Ordered words">Ordered words</a></td></tr>
  </tbody>
</table>
</body>
</html>"""

        responses.add(**{
            'method': responses.GET,
            'url': self.url,
            'body': body,
            'status': 200,
            'content_type': 'text/html',
            })

        page = requests.get(self.url)
        self.tree = html.fromstring(page.content)

    def test_it_retrieves_all_exercise_relative_links(self):
        expected = ['/wiki/Set_puzzle', '/wiki/Ordered_words']

        finder = ExerciseFinder(self.tree)
        exercises = finder.find()
        self.assertEqual(exercises, expected)


class TestRosettaExerciseSpider(unittest.TestCase):
    def setUp(self):
        self.url = 'https://bit.ly/2vCQ6sg'
        body = """
<html>
<body>
<table>
  <tbody>
    <tr class="row-odd"><td class="smwtype_wpg"><a href="/wiki/Set_puzzle" title="Set puzzle">Set puzzle</a></td></tr>
    <tr class="row-even"><td class="smwtype_wpg"><a href="/wiki/Ordered_words" title="Ordered words">Ordered words</a></td></tr>
  </tbody>
</table>
</body>
</html>"""

        responses.add(**{
            'method': responses.GET,
            'url': self.url,
            'body': body,
            'status': 200,
            'content_type': 'text/html',
            })

    @responses.activate
    def test_it_retrieves_all_exercise_links(self):
        expected = [
                u'https://rosettacode.org/wiki/Set_puzzle',
                u'https://rosettacode.org/wiki/Ordered_words']

        spider = RosettaExerciseSpider(self.url)
        exercises = spider.run()
        self.assertEqual(exercises, expected)


if __name__ == '__main__':
    unittest.main()
