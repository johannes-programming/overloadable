import functools
from typing import *

__all__ = ["overloadable"]


class Holder: ...


def identity(old: Any, /) -> Any:
    return old


def overloadable(
    old: Callable,
    /,
) -> Callable:
    holder = Holder()
    try:
        func = old.__func__
    except AttributeError:
        func = old
        bind = identity
    else:
        bind = type(old)

    @bind
    @functools.wraps(func)
    def new(*args, **kwargs):
        key = func(*args, **kwargs)
        value = holder._data.lookup[key]
        ans = value(*args, **kwargs)
        return ans

    holder._data = new
    new.lookup = dict()
    new.overload = functools.partial(
        overloadtool,
        bind=bind,
        data=new,
    )
    return new


def overloaddecorator(
    old: Callable,
    /,
    *,
    bind: Callable,
    data: Any,
    key: Hashable,
) -> Any:
    data.lookup[key] = old
    overload(bind(old))
    return data


def overloadtool(
    key: Hashable = None,
    **kwargs,
) -> Any:
    return functools.partial(
        overloaddecorator,
        key=key,
        **kwargs,
    )
