============
overloadable
============

Overview
--------

Create an overloaded function around a core choosing function.

Installation
------------

To install ``overloadable``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install overloadable

Implementation
--------------

.. code-block:: python

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

Example
-------

.. code-block:: python

    from overloadable import overloadable

    class Bar:
        def __init__(self, addon) -> None:
            self.addon = addon

        @overloadable
        def foo(self, x):
            if type(x) is int:
                return "int"

        @foo.overload("int")
        def foo(self, x):
            return x * x + self.addon

        @foo.overload() # key=None
        def foo(self, x):
            return str(x)[::-1]

    bar = Bar(42)
    print(bar.foo(1)) # prints 43
    print(bar.foo(3.14)) # prints 41.3
    print(bar.foo("baz")) # prints zab

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/overloadable>`_
* `Download <https://pypi.org/project/overloadable/#files>`_
* `Source <https://github.com/johannes-programming/overloadable>`_

Credits
-------

* Author: Johannes
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``overloadable``!