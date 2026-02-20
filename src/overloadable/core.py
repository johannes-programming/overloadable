import functools
import types
from typing import *

import datarepr
import setdoc
from copyable import Copyable

__all__ = ["overloadable", "Overloadable"]


class Overloadable(Copyable):

    __slots__ = ("dispatch", "lookup")
    dispatch: Any
    lookup: Any

    def __call__(self: Self, *args: Any, **kwargs: Any) -> Any:
        "This magic method implements self(*args, **kwargs)."
        key: Any
        value: Callable
        key = self.dispatch(*args, **kwargs)
        value = self.lookup[key]
        return value(*args, **kwargs)

    def __get__(
        self: Self,
        *args: Any,
        **kwargs: Any,
    ) -> types.FunctionType | types.MethodType:
        "This magic method implements getting as an attribute from a class or an object."
        draft: Any
        new: Any
        obj: Any
        old: Callable
        draft = self.dispatch.__get__(*args, **kwargs)
        try:
            obj = draft.__self__
        except AttributeError:
            return self._deco(draft)
        try:
            old = draft.__func__
        except AttributeError:
            old = getattr(type(obj), draft.__name__)
        new = self._deco(old)
        return types.MethodType(new, obj)

    @setdoc.basic
    def __init__(self: Self, dispatch: Any) -> None:
        self.dispatch = dispatch
        self.lookup = dict()

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr.datarepr(
            type(self).__name__,
            dispatch=self.dispatch,
            lookup=self.lookup,
        )

    def _deco(self: Self, old: Callable) -> Any:
        return deco(old, lookup=dict(self.lookup))

    @setdoc.basic
    def copy(self: Self) -> Self:
        ans: Self
        ans = type(self)(self.dispatch)
        ans.lookup = self.lookup
        return ans

    def overload(self: Self, key: Any = None) -> functools.partial:
        "This method returns a decorator for overloading."
        return functools.partial(overload_, self, key)


overloadable = Overloadable


def deco(old: Callable, *, lookup: dict) -> types.FunctionType:
    def new(*args: Any, **kwargs: Any) -> Any:
        "This function implements overloaded calling. This docstring should be overwritten."
        key: Any
        value: Any
        key = old(*args, **kwargs)
        value = lookup[key]
        return value(*args, **kwargs)

    try:
        return functools.wraps(old)(new)
    except Exception:
        return new


def overload_(
    master: Overloadable,
    key: Any,
    value: Callable,
    /,
) -> Overloadable:
    "This function saves a given overload."
    overload(value)
    master.lookup[key] = value
    return master
