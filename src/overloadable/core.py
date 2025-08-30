import functools
import types
from typing import *

__all__ = ["overloadable", "Overloadable"]

class Overloadable:

    def __call__(self:Self, *args:Any, **kwargs:Any)->Any:
        # Direct call acts like the plain function
        key:Any = self.dispatch(*args, **kwargs)
        value:Callable = self.lookup[key]
        ans:Any = value(*args, **kwargs)
        return ans

    def __get__(self:Self, *args:Any, **kwargs:Any)->Any:
        draft:Any = self.dispatch.__get__(*args, **kwargs)
        try:
            obj:Any = draft.__self__
        except AttributeError:
            return self._deco(draft)
        old:Callable
        try:
            old = draft.__func__
        except AttributeError:
            old = getattr(type(obj), draft.__name__)
        new:Any = self._deco(old)
        return types.MethodType(new, obj)
    
    def __init__(self:Self, dispatch:Any)->None:
        self.dispatch = dispatch
        self.lookup = dict()
    
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
    
    ans:Any
    try:
        ans = functools.wraps(old)(new)
    except:
        ans = new
    return ans

def overload(master:Overloadable, key:Any, value:Callable, /)->Overloadable:
    master.lookup[key] = value
    return master

