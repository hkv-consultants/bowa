# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals


def version():
    """
    return version string
    """
    from pkginfo.installed import Installed
    import bowa
    installed = Installed(bowa)
    if installed.version:
        return 'Versie januari 2014 (%s)' % (installed.version)
    else:
        return 'Versie januari 2014'
