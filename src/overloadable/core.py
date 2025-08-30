import functools
import types
from typing import *

__all__ = ["overloadable", "Overloadable"]

class Overloadable:
    def __init__(self:Self, original:Any)->None:
        self.original = original
        self.lookup = dict()

    def __get__(self:Self, *args:Any, **kwargs:Any)->Any:
        ans = self.original.__get__(*args, **kwargs)
        if isinstance(ans, types.FunctionType):
            ans = self._deco(ans)
            return ans
        else:
            obj = ans.__self__
            func = ans.__func__
            func = self._deco(func)
            ans = types.MethodType(func, obj)
            return ans

    def __call__(self, *args, **kwargs):
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
    def new(*args, **kwargs):
        key = old(*args, **kwargs)
        value = lookup[key]
        ans = value(*args, **kwargs)
        return ans

    return new

def overload(master:Overloadable, key:Any, value:Any, /)->Overloadable:
    master.lookup[key] = value
    return master

