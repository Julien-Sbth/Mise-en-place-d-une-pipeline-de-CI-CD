import unittest

class SimpleMath:
    @staticmethod
    def addition(a, b):
        return a + b

class TestSimpleMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(SimpleMath.addition(2, 3), 5)
        self.assertEqual(SimpleMath.addition(-1, 1), 0)
        self.assertEqual(SimpleMath.addition(0, 0), 0)
        self.assertEqual(SimpleMath.addition(2.5, 3.5), 6.0)

if __name__ == '__main__':
    unittest.main()
