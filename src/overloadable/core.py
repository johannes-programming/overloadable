import dataclasses
import functools
import types
from typing import *

import tofunc

__all__ = ["overloadable"]


def identity(value: object, /) -> object:
    return value


def overloadable(dispatch: Any) -> types.FunctionType:
    return Data(dispatch).ans


class Data:
    def __init__(self: Self, value: Any, /) -> None:
        self.ans = self.makeans(value)

    def ans_1(self: Self, *args: Any, **kwargs: Any) -> Any:
        key: Any
        key = self.ans.dispatch(*args, **kwargs)
        return self.ans.lookup[key](*args, **kwargs)

    def makeans(self: Self, value: Any, /) -> Any:
        ans: Any
        unpack: Unpack
        unpack = Unpack.byValue(value)
        ans = tofunc.tofunc(self.ans_1)
        functools.wraps(unpack.func)(ans)
        ans = unpack.kind(ans)
        ans._data = self
        ans.lookup = dict()
        ans.dispatch = unpack.func
        ans.overload = tofunc.tofunc(self.overload_1)
        functools.wraps(self.overload_1)(ans.overload)
        return ans

    def overload_1(self: Self, key: Any = None) -> Any:
        return Overload(ans=self.ans, key=key)


@dataclasses.dataclass(frozen=True)
class Overload:
    ans: Any
    key: Any

    def __call__(self: Self, value: Any) -> Any:
        self.ans.lookup[self.key] = value
        return self.ans


@dataclasses.dataclass(frozen=True)
class Unpack:
    kind: Any
    func: Any

    @classmethod
    def byValue(cls: type[Self], value: Any) -> Self:
        func: Any
        kind: Any
        try:
            func = value.__func__
        except AttributeError:
            func = value
            kind = identity
        else:
            kind = type(value)
        return cls(kind=kind, func=func)
