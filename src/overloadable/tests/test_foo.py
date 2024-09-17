import unittest

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

    @foo.overload()  # key=None
    def foo(self, x):
        return str(x)[::-1]


class TestFoo(unittest.TestCase):
    def test_foo(self):
        bar = Bar(42)
        self.assertEqual(bar.foo(1), 43)
        self.assertEqual(bar.foo(3.14), "41.3")
        self.assertEqual(bar.foo("baz"), "zab")


if __name__ == "__main__":
    unittest.main()
