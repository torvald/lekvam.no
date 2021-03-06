# -*- coding: utf-8 -*-

"""
"""

import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

link_finder = re.compile(r'\[\[(?P<link>[^\|\]]*)(?P<slug>\|[^\[]*)?\]\]')
title_finder = re.compile(r'(?P<level>[=]{2,6})( )?(?P<title>[^=]*)( )?[=]{2,6}')
#image_finder = re.compile(r'\{\{(?P<media>[^\|\}]*)(?P<title>|[^\}]*)?\}\}')
image_finder = re.compile(r'\{\{(?P<media>[^\}]*)\}\}')

internal_link_icon = ''
external_link_icon = '<span class="glyphicon glyphicon-globe" aria-hidden="true"></span> '

media_url = "https://wiki.lekvam.no/_media/"

class DokuWikiLinks(Preprocessor):


    def run(self, lines):
        # TODO add
        #try:
        lines = self._parse_newlines(lines)
        lines = self._parse_links(lines)
        lines = self._parse_titles(lines)
        lines = self._parse_tables(lines)
        lines = self._parse_images(lines)
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
                classes = "external-link"
            else:
                icon = internal_link_icon
                classes = "internal-link"

            if slug == None:
                # no slug, must be link-only
                return u"{}<a class={} href='{}'>{}</a>".format(icon, classes, self._link_to_slug(link), link)
            else:
                slug = slug.replace('|', '')
                return u"{}<a class={} href='{}'>{}</a>".format(icon, classes, link, slug)

        return [link_finder.sub(_render, line) for line in lines]


    def _parse_images(self, lines):

        def _render(match):
            width = ""
            # get elemens from media on form mediafil.jpg?nocahce&ost|title
            pipe_split = match.groupdict()['media'].split('|')
            media = pipe_split[0]
            # media resource fist
            supported_media = ['.jpg', '.png', '.jpeg', '.gif']
            if not any(fileending in media for fileending in supported_media):
                return "DokuWikiParser; not supported media"
            media_arguments = media.replace("?", "&").split("&")[1:]
            for arg in media_arguments:
                if arg.isdigit():
                    width = "width='{}'".format(arg)
                
            if len(pipe_split) == 2:
                title = pipe_split[1]

            # poor mans uri search
            if 'http' in media:
                src = media
            else:
                # asume internal media
                media = media.replace(':', '/')
                src = media_url + media

            return u"<img class='img-thumbnail img-responsive' {} src='{}'/>".format(width, src)
            
        return [image_finder.sub(_render, line) for line in lines]


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
                    new_line = "</tbody></table></div>" + line
                else:
                    new_line = line
                context = None


            if context == "header":
                new_line += "<thead><tr>"
                columns = line.split('^')[1:-1]
                for column in columns:
                    new_line += u"<th>{}</th>".format(column)
                new_line += "</tr></thead>"
                
            elif context == "body":
                new_line += "<tr>"
                columns = line.split('|')[1:-1]
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
