# -*- coding: utf-8 -*-

from docutils.parsers.rst import roles
from .directives import (
    findoutmoreref,
    windowswitref,
)
from sphinx.addnodes import manpage
from sphinx.roles import (
    XRefRole,
)


class HandbookRefRole(XRefRole):
    """Custom :ref: roles base class"""
    refnodecls = None
    refnodeclsname = None

    def run(self):
        # must be 'ref' or sphinx will refuse to resolve the reference
        self.refdomain, self.reftype = 'std', 'ref'
        # values don't matter, sphinx will overwrite them when resolving
        # the pending ref
        self.classes = ['handbookref']
        return self.create_xref_node()

    def result_nodes(self, document, env, node, is_ref):
        nodes, messages = super().result_nodes(document, env, node, is_ref)
        # we wrap the generated reference into an inline (container)
        # to enable consistent markup etc.
        r = self.refnodecls(
            'handbookrawsrc', '', *nodes, classes=[self.refnodeclsname])
        return ([r], messages)


class FindOutMoreRole(HandbookRefRole):
    """:find-out-more: ref"""
    refnodecls = findoutmoreref
    refnodeclsname = 'findoutmoreref'


class WindowsWitRole(HandbookRefRole):
    """:windows-wit: ref"""
    refnodecls = windowswitref
    refnodeclsname = 'windowswitref'


class anycmd(manpage):
    visited = set()
    cmdname = ''
    manual_url_tmpl = None

    @classmethod
    def visit_html(cls, self, node):
        assert len(node.children) == 1, \
            f"`{cls.cmdname}` must not have more than one child node"
        self.visit_inline(node)
        self.body.append(f'<code>{cls.cmdname} ')

    @classmethod
    def depart_html(cls, self, node):
        self.depart_inline(node)
        self.body.append('</code>')
        # get the name of the subcommand
        subcmdname = str(node.children[0]).split()[0]
        # reference ID (source doc + command + subcommand)
        man_id = (self.document.attributes['source'], cls.cmdname, subcmdname)
        # only for the first reference, include a manual link
        if cls.manual_url_tmpl and man_id not in cls.visited:
            self.body.append(' (<a href="{url}">manual</a>)'.format(
                url=cls.manual_url_tmpl.format(
                    cmdname=subcmdname,
                )
            ))
            cls.visited.add(man_id)

    @classmethod
    def visit_latex(cls, self, node):
        self.visit_literal(node)
        self.body.append(f'{cls.cmdname} ')

    @classmethod
    def depart_latex(cls, self, node):
        self.depart_literal(node)


class shcmd(anycmd):
    cmdname = ''
    manual_url_tmpl = None


class dlcmd(anycmd):
    cmdname = 'datalad'
    manual_url_tmpl = \
        'https://docs.datalad.org/generated/man/datalad-{cmdname}.html'


class gitcmd(anycmd):
    cmdname = 'git'
    manual_url_tmpl = "https://git-scm.com/docs/git-{cmdname}"


class gitannexcmd(anycmd):
    cmdname = 'git annex'
    manual_url_tmpl = "https://git-annex.branchable.com/git-annex-{cmdname}"


hb_roles = {
    'find-out-more': FindOutMoreRole(),
    'windows-wit': WindowsWitRole(),
}

for rolename, cls in (
    ('dlcmd', dlcmd),
    ('gitcmd', gitcmd),
    ('gitannexcmd', gitannexcmd),
    ('shcmd', shcmd),
):
    hb_roles[rolename] = roles.CustomRole(
        rolename,
        roles.GenericRole(rolename, cls),
        {'classes': [rolename]},
    )


def setup(app):
    for rolename, func in hb_roles.items():
        roles.register_local_role(rolename, func)

    for cls in (dlcmd, gitcmd, gitannexcmd, shcmd):
        app.add_node(
            cls,
            html=(cls.visit_html, cls.depart_html),
            latex=(cls.visit_latex, cls.depart_latex),
        )

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

# vim: set expandtab shiftwidth=4 softtabstop=4 :
