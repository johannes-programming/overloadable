import dataclasses
import functools
import types
from typing import *

import tofunc

__all__ = ["overloadable", "Overloadable"]


def foo(old, *, lookup):
    def new(*args, **kwargs):
        key = old(*args, **kwargs)
        value = lookup[key]
        ans = value(*args, **kwargs)
        return ans

    return new


class Overloadable:
    def __init__(self, original):
        self.original = original
        self.lookup = dict()

    def __get__(self, *args, **kwargs):
        ans = self.original.__get__(*args, **kwargs)
        if isinstance(ans, types.FunctionType):
            ans = foo(ans, lookup=self.lookup)
            return ans
        else:
            obj = ans.__self__
            func = ans.__func__
            func = foo(func, lookup=self.lookup)
            ans = types.MethodType(func, obj)
            return ans

    def __call__(self, *args, **kwargs):
        # Direct call acts like the plain function
        key = self.original(*args, **kwargs)
        value = self.lookup[key]
        ans = value(*args, **kwargs)
        return ans

    def overload(self, key=None):
        return Overload(self, key)


class Overload:
    def __call__(self: Self, value: Any) -> Overloadable:
        self.overloadable.lookup[self.key] = value
        return self.overloadable

    def __init__(self: Self, overloadable: Overloadable, key: Any):
        self.overloadable = overloadable
        self.key = key


overloadable = Overloadable
