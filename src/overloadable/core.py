import functools
import types
from typing import *

__all__ = ["overloadable", "Overloadable"]

class Overloadable:
    def __init__(self:Self, original:Any)->None:
        self.original = original
        self.lookup = dict()

    def __get__(self:Self, *args:Any, **kwargs:Any)->Any:
        draft = self.original.__get__(*args, **kwargs)
        try:
            obj:Any = draft.__self__
        except AttributeError:
            return self._deco(draft)
        old:Callable
        try:
            old = draft.__func__
        except AttributeError:
            old = getattr(type(obj), draft.__name__)
        new = self._deco(old)
        return types.MethodType(new, obj)

    def __call__(self:Self, *args:Any, **kwargs:Any)->Any:
        # Direct call acts like the plain function
        key = self.original(*args, **kwargs)
        value = self.lookup[key]
        ans = value(*args, **kwargs)
        return ans
    
    def _deco(self:Self, old:Callable)->Any:
        return deco(old, lookup=dict(self.lookup))


    def overload(self:Self, key=None)->functools.partial:
        return functools.partial(overload, self, key)

overloadable = Overloadable

def deco(old, *, lookup):
    def new(*args:Any, **kwargs:Any)->Any:
        key = old(*args, **kwargs)
        value = lookup[key]
        ans = value(*args, **kwargs)
        return ans

    return new

def overload(master:Overloadable, key:Any, value:Any, /)->Overloadable:
    master.lookup[key] = value
    return master

