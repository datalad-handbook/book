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
    self.body.append("""
    \\begin{tcolorbox}[
        enhanced,
        breakable,
        drop lifted shadow,
        sharp corners,
        title=Note for Git users,
        coltitle=dataladgray,
        colbacktitle=dataladblue,
        colframe=dataladblue!70!black,
        fonttitle=\\bfseries]
    """)


def depart_gitusernote_latex(self, node):
    self.body.append('\n\n\\end{tcolorbox}\n')


class GitUserNote(BaseAdmonition):
    """
    An admonition mentioning things to look at as reference.
    """
    node_class = gitusernote


class findoutmore(nodes.container):
    """Custom "findoutmore" container."""
    pass


def visit_findoutmore_html(self, node):
    self.visit_container(node)


def depart_findoutmore_html(self, node):
    self.depart_container(node)


def visit_findoutmore_latex(self, node):
    self.body.append("""
    \\begin{tcolorbox}[
        enhanced,
        breakable,
        drop lifted shadow,
        sharp corners,
        title=Find out more,
        coltitle=dataladgray,
        colbacktitle=dataladyellow,
        colframe=dataladyellow!70!black,
        fonttitle=\\bfseries]
    """)


def depart_findoutmore_latex(self, node):
    self.body.append('\n\n\\end{tcolorbox}\n')


class FindOutMore(BaseAdmonition):
    """findoutmore RST directive

    The idea here is to use an admonition to parse the RST,
    but actually fully replace it afterwards with a custom
    node structure. This is done to be able to replace a
    rather verbose custom markup that was used before in the
    book. Eventually, it may be replaced (in here) with
    something completely different -- without having to change
    content and markup in the book sources.
    """
    node_class = nodes.admonition
    # empty is no allowed
    has_content = True
    # needs at least a one word titel
    required_arguments = 1

    def run(self):
        # this uses the admonition code for RST parsion
        docnodes = super(FindOutMore, self).run()
        # but we throw away the title, because we want to mark
        # it up as a 'header' further down
        del docnodes[0][0]
        # now put the entire admonition structure into a container
        # that we assign the necessary class to make it 'toggle-able'
        # in HTML
        # outer container
        toggle = findoutmore(
            'toogle',
            # header line with 'Find out more' prefix
            nodes.paragraph(
                # place actual admonition title we removed
                # above
                'title', self.arguments[0],
                # add (CSS) class
                classes=['header'],
            ),
            # place the rest of the admonition structure after the header,
            # but still inside the container
            *docnodes[0].children,
            # properly identify as 'findoutmore' to enable easy custom
            # styling, and also tag with 'toggle'. The later is actually
            # not 100% necessary, as 'findoutmore' could get that
            # functional assigned in CSS instead (maybe streamline later)
            classes=['toggle', 'findoutmore'],
        )
        return [toggle]


class WindowsWorkArounds(BaseAdmonition):
    """windowsworkaround RST directive

    This is identical to the FindOutMore directive, and allows a custom markup
    for notes targeted at Windows users
    """
    node_class = nodes.admonition
    # empty is no allowed
    has_content = True
    # needs at least a one word titel
    required_arguments = 1

    def run(self):
        # this uses the admonition code for RST parsion
        docnodes = super(WindowsWorkArounds, self).run()
        # but we throw away the title, because we want to mark
        # it up as a 'header' further down
        del docnodes[0][0]
        # now put the entire admonition structure into a container
        # that we assign the necessary class to make it 'toggle-able'
        # in HTML
        # outer container
        toggle = windowsworkarounds(
            'toogle',
            # header line with 'Windows Workaround' prefix
            nodes.paragraph(
                # place actual admonition title we removed
                # above
                'title', self.arguments[0],
                # add (CSS) class
                classes=['header'],
            ),
            # place the rest of the admonition structure after the header,
            # but still inside the container
            *docnodes[0].children,
            # properly identify as 'windowsworkarounds' to enable easy custom
            # styling, and also tag with 'toggle'. The later is actually
            # not 100% necessary, as 'windowsworkarounds' could get that
            # functional assigned in CSS instead (maybe streamline later)
            classes=['toggle', 'windowsworkarounds'],
        )
        return [toggle]


class windowsworkarounds(nodes.container):
    """Custom "windowsworkarounds" container."""
    pass


def visit_windowsworkarounds_html(self, node):
    self.visit_container(node)


def depart_windowsworkarounds_html(self, node):
    self.depart_container(node)


def visit_windowsworkarounds_latex(self, node):
    self.body.append("""
    \\begin{tcolorbox}[
        enhanced,
        breakable,
        drop lifted shadow,
        sharp corners,
        title=Windows Workaround,
        coltitle=dataladgray,
        colbacktitle=windowsgreen,
        colframe=windowsblue!70!black,
        fonttitle=\\bfseries]
    """)


def depart_windowsworkarounds_latex(self, node):
    self.body.append('\n\n\\end{tcolorbox}\n')



def setup(app):
    app.add_node(
        gitusernote,
        html=(visit_gitusernote_html, depart_gitusernote_html),
        latex=(visit_gitusernote_latex, depart_gitusernote_latex),
    )
    app.add_directive('gitusernote', GitUserNote)
    app.add_node(
        findoutmore,
        html=(visit_findoutmore_html, depart_findoutmore_html),
        latex=(visit_findoutmore_latex, depart_findoutmore_latex),
    )
    app.add_directive('findoutmore', FindOutMore)
    app.add_node(
        windowsworkarounds,
        html=(visit_windowsworkarounds_html, depart_windowsworkarounds_html),
        latex=(visit_windowsworkarounds_latex, depart_windowsworkarounds_latex),
    )
    app.add_directive('windowsworkarounds', WindowsWorkArounds)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
