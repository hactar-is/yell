from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals


class Reg(object):
    """ Registry mapping notification names to backends """

    def __init__(self):
        self.notifications = {}


registry = Reg()
