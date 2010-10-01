import datetime
import unittest

from pills import closest, length, dt, attrs, fails, gt, lt, in_range, any_of
from pills.utils import validol


class TestCase(unittest.TestCase):

    def raises_on_validation(self, *args):
        self.assertRaises(validol.ValidationError,
                          validol.validate, *args)

    def check_result(self, *args, **kwargs):
        result = kwargs.pop('result')
        self.failUnlessEqual(validol.validate(*args), result)


class ClosestTest(TestCase):

    def test_bizarre_args(self):
        self.raises_on_validation(closest([]), 2)
        self.raises_on_validation(closest(set()), 2)
        self.raises_on_validation(closest(tuple()), 2)
        self.raises_on_validation(closest({}), 2)
        self.raises_on_validation(closest(1), [1])

    def test_result(self):
        stack, needle = [-10, 92, 52, 10], 7
        self.check_result(closest(stack), needle, result=10)

    def test_should_accept_iterable(self):
        self.check_result(closest(xrange(40)), 7, result=7)
        self.check_result(closest(range(40)), 7, result=7)
        self.check_result(closest([-1]), 7, result=-1)
        self.check_result(closest((100, 8, )), 7, result=8)


class LengthTest(TestCase):

    def test_simple(self):
        self.check_result(length(1), [123], result=[123])
        self.raises_on_validation(length(123), [123])

        self.raises_on_validation(length(), [123])

        result = [1, 2, 3, 4]
        self.check_result(length(4), result, result=result)

    def test_combined(self):
        self.check_result(length(lt(2)), [123], result=[123])
        self.raises_on_validation(length(gt(2)), [123])
        self.check_result(length(gt(0)), [123], result=[123])
        self.check_result(length(in_range(0, 1)), [123], result=[123])


class DtTest(TestCase):

    def test_correct(self):
        result = datetime.datetime(year=2001, month=9, day=1)
        self.check_result(dt('%d.%m.%Y'), '01.09.2001', result=result)

    def test_incorrect(self):
        self.raises_on_validation(dt('%Y'), '01.09.2010')
        self.raises_on_validation(dt('%Y'), '')
        self.raises_on_validation(dt('foo'), 'bar')


class AttrsTest(TestCase):

    def setUp(self):
        self.instance = type('Test', (), {'a': 1, 'b': 2})()

    def test_correct(self):
        self.check_result(attrs('b'), self.instance, result=self.instance)
        self.check_result(attrs('a', 'b'), self.instance, result=self.instance)
        self.check_result(attrs('a', b=2), self.instance,
                          result=self.instance)
        self.check_result(attrs(a=1, b=2), self.instance,
                          result=self.instance)

    def test_incorrect(self):
        self.raises_on_validation(attrs(a=1, bar='baz'), self.instance)
        self.raises_on_validation(attrs('foo', bar='baz'), self.instance)
        self.raises_on_validation(attrs('foo'), self.instance)


class FailsTest(TestCase):

    def test_correct(self):
        self.check_result(fails(lt(1)), 2, result=2)
        self.check_result(fails(any_of([0, 1])), 2, result=2)

    def test_incorrect(self):
        self.raises_on_validation(fails(any_of([0, 1, 2])), 2)
        self.raises_on_validation(fails(gt(1)), 2)


if __name__ == '__main__':
    unittest.main()
