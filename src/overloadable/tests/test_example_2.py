import unittest
from typing import Any, Self

from overloadable.core.Overloadable import Overloadable

__all__ = ["TestBar"]


class Bar:

    @Overloadable
    @staticmethod
    def foo(x: Any) -> int | str:
        return type(x)

    @foo.overload(int)  # type: ignore[no-redef]
    def foo(x: int) -> int:
        return x**2

    @foo.overload(str)  # type: ignore[no-redef]
    def foo(x: str) -> str:
        return str(x)[::-1]


class TestBar(unittest.TestCase):
    def test_foo(self: Self) -> None:
        bar: Bar
        bar = Bar()
        self.assertEqual(bar.foo(5), 25)
        self.assertEqual(bar.foo("baz"), "zab")
        self.assertEqual(Bar.foo(5), 25)
        self.assertEqual(Bar.foo("baz"), "zab")


if __name__ == "__main__":
    unittest.main()
