# -*- coding: utf-8 -*-

from . import roles
from . import directives


def setup(app):
    roles.setup(app)
    directives.setup(app)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
