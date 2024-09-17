import functools
import typing

__all__ = ["overloadable"]


class Holder: ...


def overloadable(old, /):
    holder = Holder()

    @functools.wraps(old)
    def new(*args, **kwargs):
        key = old(*args, **kwargs)
        value = holder._data.lookup[key]
        ans = value(*args, **kwargs)
        return ans

    holder._data = new
    new.lookup = dict()
    new.overload = functools.partial(tool, data=new)
    return new


def tool(key=None, **kwargs):
    return functools.partial(decorator, key=key, **kwargs)


def decorator(old, /, *, data, key):
    typing.overload(old)
    data.lookup[key] = old
    return data
