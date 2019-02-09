# -*- coding: utf-8 -*-
"""
    flaskext.sqlalchemy._compat
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Internal Python 2.x/3.x compatibility layer.

    :copyright: (c) 2013 by Daniel Neuhäuser
    :license: BSD, see LICENSE for more details.
"""


def iteritems(d):
    return iter(d.items())

def itervalues(d):
    return iter(d.values())


