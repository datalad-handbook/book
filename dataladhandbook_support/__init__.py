# -*- coding: utf-8 -*-

from . import roles
from . import directives


def setup(app):
    roles.setup(app)
    directives.setup(app)


from . import _version
__version__ = _version.get_versions()['version']
