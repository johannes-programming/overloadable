import unittest

__all__ = ["test"]


def test() -> unittest.TextTestResult:
    loader: unittest.TestLoader
    suite: unittest.TestSuite
    runner: unittest.TextTestRunner
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="overloadable.tests")
    runner = unittest.TextTestRunner()
    return runner.run(suite)
