# -*- coding: utf-8 -*-

from docutils.parsers.rst import roles
from .directives import (
    findoutmoreref,
    windowswitref,
)
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


hb_roles = {
    'find-out-more': FindOutMoreRole(),
    'windows-wit': WindowsWitRole(),
}


def setup(app):
    for rolename, func in hb_roles.items():
        roles.register_local_role(rolename, func)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

# vim: set expandtab shiftwidth=4 softtabstop=4 :
