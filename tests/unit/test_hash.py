import unittest
from forbiddenfruit import curse, reverse, cursed

class TestHashFeatures(unittest.TestCase):
    def test_hash(self):
        # We'll use a float as it is hashable and builtin.
        def constant_hash(self):
            return 42

        with cursed(float, "__hash__", constant_hash):
            self.assertEqual(hash(1.5), 42)
            self.assertEqual(hash(2.0), 42)

        # Verify it is reverted
        self.assertNotEqual(hash(1.5), 42)

    def test_set_hash(self):
        # set is normally unhashable
        with self.assertRaises(TypeError):
            hash(set([1]))

        def set_hash(self):
            return 123

        with cursed(set, "__hash__", set_hash):
            s = set([1, 2])
            self.assertEqual(hash(s), 123)
