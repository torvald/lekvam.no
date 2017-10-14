# -*- coding: utf-8 -*-

"""
"""

import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

link_finder = re.compile(r'\[\[(?P<link>[^\|\]]*)(?P<slug>\|[^\[]*)?\]\]')
title_finder = re.compile(r'(?P<level>[=]{2,6})( )?(?P<title>[^=]*)( )?[=]{2,6}')

internal_link_icon = ''
external_link_icon = '<span class="glyphicon glyphicon-globe" aria-hidden="true"></span> '

class DokuWikiLinks(Preprocessor):


    def run(self, lines):
        # TODO add
        #try:
        lines = self._parse_newlines(lines)
        lines = self._parse_links(lines)
        lines = self._parse_titles(lines)
        lines = self._parse_tables(lines)
        #except Exception as e:
        #    return "Dokuwiki Parser error: " + str(e)
        
        return lines


    def _parse_links(self, lines):

        def _render(match):
            link = match.groupdict()['link']
            slug = match.groupdict()['slug']

            if '.' in link:
                # . are not allowed in slugs anyway 
                icon = external_link_icon
            else:
                icon = internal_link_icon

            if slug == None:
                # no slug, must be link-only
                return u"{}<a href='{}'>{}</a>".format(icon, self._link_to_slug(link), link)
            else:
                slug = slug.replace('|', '')
                return u"{}<a href='{}'>{}</a>".format(icon, link, slug)

        return [link_finder.sub(_render, line) for line in lines]


    def _parse_titles(self, lines):

        def _render(match):
            matches = match.groupdict()
            # highest level of dokuwiki titles has 6 ='s, 7 - 6 gived 1 for h1,
            # 7 - 5 for h2, etc.
            level = (7 - len(matches['level']))
            return u"<h{}>{}</h{}>".format(level, matches['title'], level)

        return [title_finder.sub(_render, line) for line in lines]


    def _parse_newlines(self, lines):
        newlines_finder = re.compile(r'\\\\')
        return [newlines_finder.sub("<br>", line) for line in lines]


    def _parse_tables(self, lines):
        new_lines = []
        context = None # (None|"header"|"body")
        for line in lines:
            new_line = ""

            # update context, add tags if changes states
            if line.startswith("^"):
                if context == None:
                    new_line += "<div class='table-responsive'><table class='table'>"
                context = "header"

            elif line.startswith("|"):
                if context == 'header':
                    new_line += "<tbody>"
                context = "body"

            else:
                # Not in table context, add original line
                if context == "body":
                    new_line = "</tbody></table>" + line
                else:
                    new_line = line
                context = None


            if context == "header":
                new_line += "<thead><tr>"
                columns = line.split('^')
                for column in columns:
                    new_line += u"<th>{}</th>".format(column)
                new_line += "</tr></thead>"
                
            elif context == "body":
                new_line += "<tr>"
                columns = line.split('|')
                for column in columns:
                    new_line += u"<td>{}</td>".format(column)
                new_line += "</tr>"

            new_lines.append(new_line)

        return new_lines

    def _link_to_slug(self, link):
        link = link.lower()
        link = link.replace(' ', '_')
        link = link.replace(u'æ', 'ae_')
        link = link.replace(u'å', 'a')
        link = link.replace(u'ø', 'o')
        return link


class DokuWikiLinksExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('dokuwiki_parser', DokuWikiLinks(md), '_end')
