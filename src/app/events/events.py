# Using dispatcher 1.0 here [https://pypi.python.org/pypi/dispatcher/1.0]
from dispatch import Signal


E_TRANSLATOR_WAITING = Signal()


def respond(sender, **kwargs):
    print "*" * 70; print "Handler called by %s with args %s" % (sender, kwargs); print "*" * 70

E_TRANSLATOR_WAITING.connect(respond)