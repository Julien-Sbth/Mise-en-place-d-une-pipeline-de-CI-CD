# pylint: disable=too-few-public-methods

"""
Module providing a simple math class with unit tests.
"""

import unittest

class SimpleMath:
    """Class for basic mathematical operations."""

    @staticmethod
    def addition(a, b):
        """Return the sum of a and b."""
        return a + b

class TestSimpleMath(unittest.TestCase):
    """Unit tests for the SimpleMath class."""

    def test_addition(self):
        """Test the addition method with different inputs."""
        self.assertEqual(SimpleMath.addition(2, 3), 5)
        self.assertEqual(SimpleMath.addition(-1, 1), 0)
        self.assertEqual(SimpleMath.addition(0, 0), 0)
        self.assertEqual(SimpleMath.addition(2.5, 3.5), 6.0)

if __name__ == '__main__':
    unittest.main()
