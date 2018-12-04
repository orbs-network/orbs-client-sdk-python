import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from crypto.hash import Hash


class TestHashFunctions(unittest.TestCase):

    data = b"testing"
    expected_sha256 = "cf80cd8aed482d5d1527d7dc72fceff84e6326592848447d2dc0b0e87dfc9a90"
    expected_ripemd160_sha256 = "1acb19a469206161ed7e5ed9feb996a6e24be441"

    def test_calc_sha256(self):
        result = Hash.calc_sha256(self.data)
        self.assertEqual(self.expected_sha256, result)

    def test_calc_ripemd160_sha256(self):
        result = Hash.calc_ripemd160_sha256(self.data)
        self.assertEqual(self.expected_ripemd160_sha256, result)


if __name__ == '__main__':
    unittest.main()
