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
    def new(*args, **kwargs) -> Any:
        key = func(*args, **kwargs)
        value = holder._data.registry[key]
        ans = value(*args, **kwargs)
        return ans

    holder._data = new
    new.registry = dict()
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
    data.registry[key] = old
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
