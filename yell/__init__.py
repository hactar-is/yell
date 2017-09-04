# -*- coding: utf-8 -*-

"""
    yell
    ~~~~~~~~~~~~~
    Pluggable notifications.
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()

from builtins import *
from builtins import object
from future.utils import with_metaclass

__version__ = "0.3.2"


import hues


class Reg(object):
    """ Registry mapping notification names to backends """

    notifications = {}

    def __new__(cls):
        obj = super(Reg, cls).__new__(cls)
        obj.notifications = {}
        return obj


registry = Reg()


class MetaNotification(type):
    """
    Metaclass that stores all notifications in the registry.
    """
    def __init__(self, name, bases, attrs):
        super(MetaNotification, self).__init__(name, bases, attrs)
        reg = registry.notifications
        hues.info("META NOTIFICATION")
        hues.info(self)
        if self.name is not None:
            reg[self.name] = reg.get(self.name, []) + [self]

            sendfn = lambda *args, **kwargs: notify(self.name, backends=[self], *args, **kwargs)
            setattr(self, 'send', staticmethod(sendfn))

        return


class Notification(with_metaclass(MetaNotification, object)):
    """
    Base class for any kind of notifications. Inherit from this class to create
    your own notification types and backends.

    Subclasses need to implement :meth:`notify`.
    """

    name = None
    """
    A name for this notification.
    """

    data = {}
    """
    Allow arbitrary data to be stored in the base notification.
    """

    def notify(self, *args, **kwargs):
        """
        A method that delivers a notification.
        """
        raise NotImplementedError


def notify(name, *args, **kwargs):
    """
    Send notifications. If ``backends==None``, all backends with the same name
    will be used to deliver a notification.

    If ``backends`` is a list, only the specified backends will be used.

    :param name: The notification to send
    :param backends: A list of backends to be used or ``None`` to use all associated backends
    """
    assert name in registry.notifications, "'{0}' is not a valid notification.".format(repr(name))

    backends = kwargs.pop('backends', None)

    if backends is None:
        backends = registry.notifications[name]

    results = []

    for Backend in backends:
        backend = Backend()
        results.append(backend.notify(*args, **kwargs))

    return results
