#!/usr/bin/python

class ConvertExceptions(object):
    func = None
    def __init__(self, exceptions, replacement=None):
        self.exceptions = exceptions
        self.replacement = replacement
    def __call__(self, *args, **kwargs):
        if self.func is None:
            self.func = args[0]
            return self
        try:
            return self.func(*args, **kwargs)
        except self.exceptions:
            return self.replacement
