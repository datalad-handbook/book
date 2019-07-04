# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition


class gitusernote(nodes.Admonition, nodes.Element):
    """Custom "gitusernote" admonition."""


def visit_gitusernote_html(self, node):
    # it is a simple div with a dedicated CSS class assigned
    self.body.append(
        self.starttag(
            node, 'div', CLASS=('admonition ' + 'gitusernote')))
    node.insert(0, nodes.title(
        'first',
        'Note for Git users'))


def depart_gitusernote_html(self, node):
    self.depart_admonition(node)


def visit_gitusernote_latex(self, node):
    self.body.append('\n\n\\sphinxstrong{Note for Git users:}\n\n')


def depart_gitusernote_latex(self, node):
    self.body.append("\n\n")


class GitUserNote(BaseAdmonition):
    """
    An admonition mentioning things to look at as reference.
    """
    node_class = gitusernote


def setup(app):
    app.add_node(
        gitusernote,
        html=(visit_gitusernote_html, depart_gitusernote_html),
        latex=(visit_gitusernote_latex, depart_gitusernote_latex),
    )
    app.add_directive('gitusernote', GitUserNote)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
