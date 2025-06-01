import unittest
from funge98 import funge98


class TestFunge98Space(unittest.TestCase):
    def test_abstract_class(self):
        with self.assertRaises(TypeError):
            space = funge98.FungeSpace(self)


class TestUnefungeSpace(unittest.TestCase):
    def test_space_from_string_list(self):
        space = funge98.UnefungeSpace()
        string = ">123"
        space.set_space("s", string)
        self.assertEqual(space.space, string)


if __name__ == '__main__':
    unittest.main()
