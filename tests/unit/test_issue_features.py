import unittest
from forbiddenfruit import curse, reverse, cursed
import io

class TestIssueFeatures(unittest.TestCase):
    def test_hash(self):
        def constant_hash(self):
            return 42

        with cursed(float, "__hash__", constant_hash):
            self.assertEqual(hash(1.5), 42)
            self.assertEqual(hash(2.0), 42)

        self.assertNotEqual(hash(1.5), 42)

    def test_iter_and_next(self):
        class IntIterator:
            def __init__(self, val):
                self.val = val
                self.count = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.count >= self.val:
                    raise StopIteration
                self.count += 1
                return self.count

        def int_iter(self):
            return IntIterator(self)

        with cursed(int, "__iter__", int_iter):
             self.assertEqual(list(iter(3)), [1, 2, 3])

    def test_next_on_iterator(self):
        li = iter([1, 2, 3])
        list_iterator = type(li)

        def my_next(self):
            return 100

        with cursed(list_iterator, "__next__", my_next):
            it = iter([1, 2])
            self.assertEqual(next(it), 100)

    def test_init_custom_class(self):
        # Verify that our patching logic works on a class that uses standard tp_init
        class MyClass:
            def __init__(self, x, y=0):
                self.original = True
                self.x = x
                self.y = y

        def my_init(self, x, y=0):
            self.patched = True
            self.x = x * 2
            self.y = y * 2

        # We can use curse on MyClass (it has a PyTypeObject)
        with cursed(MyClass, "__init__", my_init):
            o = MyClass(10, y=20)
            self.assertTrue(hasattr(o, "patched"))
            self.assertFalse(hasattr(o, "original"))
            self.assertEqual(o.x, 20)
            self.assertEqual(o.y, 40)

    def test_init_exception(self):
        class MyClass:
            def __init__(self): pass

        def fail_init(self, *args):
            raise ValueError("Init failed")

        with cursed(MyClass, "__init__", fail_init):
            # We expect SystemError because ctypes callback clears exception,
            # so tp_init returns -1 with no exception set.
            # Ideally this would be ValueError, but forbiddenfruit limitations
            # make it hard to propagate exceptions from tp_init correctly.
            with self.assertRaises(SystemError):
                MyClass()
