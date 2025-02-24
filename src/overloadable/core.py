import dataclasses
import functools
import types
from typing import *

from identityfunction import identityfunction
from tofunc import tofunc

__all__ = ["overloadable"]


def overloadable(dispatch: Any) -> types.FunctionType:
    "This function returns an overloadable."
    return Data(dispatch).ans


class Data:
    def __init__(self, value: Any, /) -> None:
        "This method sets up the current instance."
        self.ans = self.makeans(value)

    def ans_1(self, *args: Any, **kwargs: Any) -> Any:
        "This method is used to make the overloadable."
        key = self.ans.dispatch(*args, **kwargs)
        return self.ans.lookup[key](*args, **kwargs)

    def makeans(self, value: Any, /) -> Any:
        "This method creates the overloadable."
        unpack = Unpack.byValue(value)
        ans = tofunc(self.ans_1)
        functools.wraps(unpack.func)(ans)
        ans = unpack.kind(ans)
        ans._data = self
        ans.lookup = dict()
        ans.dispatch = unpack.func
        ans.overload = tofunc(self.overload_1)
        functools.wraps(self.overload_1)(ans.overload)
        return ans

    def overload_1(self, key: Any = None) -> Any:
        "This method implements the overloading."
        return Overload(ans=self.ans, key=key)


@dataclasses.dataclass(frozen=True)
class Overload:
    ans: Any
    key: Any

    def __call__(self, value: Any) -> Any:
        "This magic method implements calling the current instance."
        self.ans.lookup[self.key] = value
        return self.ans


@dataclasses.dataclass(frozen=True)
class Unpack:
    kind: Any
    func: Any

    @classmethod
    def byValue(cls, value: Any) -> Self:
        "This classmethod creates a new instance from a dispatch."
        try:
            func = value.__func__
        except AttributeError:
            func = value
            kind = identityfunction
        else:
            kind = type(value)
        return cls(kind=kind, func=func)
