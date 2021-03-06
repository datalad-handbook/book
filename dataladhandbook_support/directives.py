# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst.directives import unchanged


class HandbookAdmonition(BaseAdmonition):
    """RST directive
    """
    node_class = nodes.admonition
    # empty is no allowed
    has_content = True
    # needs at least a one word titel
    required_arguments = 1
    option_spec = {
        'name': unchanged,
        'float': unchanged,
    }
    hba_cls = None
    hba_label = None
    # whether an admonition should be allowed to be displayed
    # in a toggle container (HTML only)
    toggle = True

    def run(self):
        # this uses the admonition code for RST parsing
        toggle = _make_std_nodes(
            self,
            super().run(),
            self.hba_cls,
            [self.hba_label])
        return [toggle]


def _make_std_nodes(admonition, docnodes, cls, classes):
    # throw away the title, because we want to mark
    # it up as a 'header' further down
    del docnodes[0][0]
    # now put the entire admonition structure into a container
    # that we assign the necessary class to make it 'toggle-able'
    # in HTML
    # outer container
    return cls(
        'handbookbox',
        # header line with 'Find out more' prefix
        nodes.paragraph(
            # place actual admonition title we removed
            # above
            'title', admonition.arguments[0],
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
        classes=(['toggle'] if admonition.toggle else []) + classes,
        # propagate all other attributes
        **{k: v for k, v in docnodes[0].attributes.items() if k != 'classes'}
    )


def _get_counted_boxstart(label, node):
    title = node.children[0].astext()
    # we have used the title for the colorbox header
    # already, do not duplicate in the body
    del node.children[0]
    float_args = ''
    if 'float' in node.attributes:
        flt = node.attributes['float']
        float_args = ', float, floatplacement={}'.format(flt) \
            if flt else ', float'
    return \
        "\\begin{{{label}}}" \
        "[before title={{\\thetcbcounter\\ }}{float_args}]" \
        "{{{title}}}\n".format(
            label=label,
            title=title,
            float_args=float_args,
        )


def _add_label(body, node):
    """If we can construct a latex label for a node, add to body"""
    parent_docname = node.parent.attributes.get('docname')
    node_id = [i for i in node.attributes.get('ids') or []]
    node_id = node_id[0] if len(node_id) else None
    # build the same form that sphinx does
    label = '\\detokenize{{{parent}:{id}}}'.format(
        parent=parent_docname, id=node_id) \
        if parent_docname and node_id else ''
    if label:
        body.append('\\label{{{}}}\n'.format(label))


class gitusernote(nodes.Admonition, nodes.Element):
    """Custom "gitusernote" admonition."""


def visit_gitusernote_html(self, node):
    self.visit_container(node)


def depart_gitusernote_html(self, node):
    self.depart_container(node)


def visit_gitusernote_latex(self, node):
    self.body.append(_get_counted_boxstart('gitusernote', node))
    _add_label(self.body, node)


def depart_gitusernote_latex(self, node):
    self.body.append('\n\n\\end{gitusernote}\n')


class GitUserNote(HandbookAdmonition):
    """
    An admonition mentioning things to look at as reference.
    """
    hba_cls = gitusernote
    hba_label = 'gitusernote'
    toggle = False


class findoutmore(nodes.container):
    """Custom "findoutmore" container."""
    pass


def visit_findoutmore_html(self, node):
    self.visit_container(node)


def depart_findoutmore_html(self, node):
    self.depart_container(node)


def visit_findoutmore_latex(self, node):
    self.body.append(_get_counted_boxstart('findoutmore', node))
    _add_label(self.body, node)


def depart_findoutmore_latex(self, node):
    self.body.append('\n\n\\end{findoutmore}\n')


class FindOutMore(HandbookAdmonition):
    """findoutmore RST directive

    The idea here is to use an admonition to parse the RST,
    but actually fully replace it afterwards with a custom
    node structure. This is done to be able to replace a
    rather verbose custom markup that was used before in the
    book. Eventually, it may be replaced (in here) with
    something completely different -- without having to change
    content and markup in the book sources.
    """
    hba_cls = findoutmore
    hba_label = 'findoutmore'


class windowsworkarounds(nodes.container):
    """Custom "windowsworkarounds" container."""
    pass


class WindowsWorkArounds(HandbookAdmonition):
    """windowsworkaround RST directive

    This is identical to the FindOutMore directive, and allows a custom markup
    for notes targeted at Windows users
    """
    hba_cls = windowsworkarounds
    hba_label = 'windowsworkarounds'


def visit_windowsworkarounds_html(self, node):
    self.visit_container(node)


def depart_windowsworkarounds_html(self, node):
    self.depart_container(node)


def visit_windowsworkarounds_latex(self, node):
    self.body.append(_get_counted_boxstart('windowsworkaround', node))
    _add_label(self.body, node)


def depart_windowsworkarounds_latex(self, node):
    self.body.append('\n\n\\end{windowsworkaround}\n')


class importantnote(nodes.container):
    pass


def visit_importantnote_html(self, node):
    self.visit_container(node)


def depart_importantnote_html(self, node):
    self.depart_container(node)


def visit_importantnote_latex(self, node):
    self.body.append(_get_counted_boxstart('importantnote', node))
    _add_label(self.body, node)


def depart_importantnote_latex(self, node):
    self.body.append('\n\n\\end{importantnote}\n')


class ImportantNote(HandbookAdmonition):
    hba_cls = importantnote
    hba_label = 'importantnote'
    toggle = False


class findoutmoreref(nodes.inline):
    pass


def visit_findoutmoreref_html(self, node):
    self.visit_inline(node)
    self.body.append('Find-out-more ')


def depart_findoutmoreref_html(self, node):
    self.depart_inline(node)


def visit_findoutmoreref_latex(self, node):
    self.body.append('{\\findoutmoreiconinline}Find-out-more ')


def depart_findoutmoreref_latex(self, node):
    pass


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
    app.add_directive('find-out-more', FindOutMore)
    app.add_node(
        windowsworkarounds,
        html=(visit_windowsworkarounds_html, depart_windowsworkarounds_html),
        latex=(visit_windowsworkarounds_latex, depart_windowsworkarounds_latex),
    )
    app.add_directive('windowsworkarounds', WindowsWorkArounds)
    app.add_node(
        importantnote,
        html=(visit_importantnote_html, depart_importantnote_html),
        latex=(visit_importantnote_latex, depart_importantnote_latex),
    )
    app.add_directive('importantnote', ImportantNote)
    app.add_node(
        findoutmoreref,
        html=(visit_findoutmoreref_html, depart_findoutmoreref_html),
        latex=(visit_findoutmoreref_latex, depart_findoutmoreref_latex),
    )

# vim: set expandtab shiftwidth=4 softtabstop=4 :
