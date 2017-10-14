"""
"""

import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

link_finder = re.compile(r'\[\[(?P<link>[^\|\]]*)(?P<slug>\|[^\[]*)?\]\]')
title_finder = re.compile(r'(?P<level>[=]{2,6})( )?(?P<title>[^=]*)( )?[=]{2,6}')


class DokuWikiLinks(Preprocessor):


    def run(self, lines):
        #try:
        lines = self.parse_links(lines)
        lines = self.parse_titles(lines)
        lines = self.parse_tables(lines)
        #except Exception as e:
        #    return "Dokuwiki Parser error: " + str(e)
        
        return lines

    def parse_links(self, lines):

        def _render(match):
            matches = match.groupdict()
            if matches['slug'] == None:
                # no slug, must be link
                return u"<a href=''>{}</a>".format(matches['link'])
            else:
                slug = matches['slug'].replace('|', '')
                return u"<a href='{}'>{}</a>".format(matches['link'], slug)

        return [link_finder.sub(_render, line) for line in lines]

    def parse_titles(self, lines):

        def _render(match):
            matches = match.groupdict()
            # highest level of dokuwiki titles has 6 ='s, 7 - 6 gived 1 for h1,
            # 7 - 5 for h2, etc.
            level = (7 - len(matches['level']))
            return "<h{}>{}</h{}>".format(level, matches['title'], level)

        return [title_finder.sub(_render, line) for line in lines]

    def parse_tables(self, lines):
        return lines

class DokuWikiLinksExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('dokuwiki_links', DokuWikiLinks(md), '_end')
