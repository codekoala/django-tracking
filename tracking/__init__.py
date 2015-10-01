from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import *
VERSION = (0, 5, 7)


def get_version():
    "Returns the version as a human-format string."
    return '.'.join([str(i) for i in VERSION])
