import unittest
from os import sys, path
from crypto.hash import Hash
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestHashFunctions(unittest.TestCase):

    __DATA = b'testing'
    __EXPECTED_SHA256 = 'cf80cd8aed482d5d1527d7dc72fceff84e6326592848447d2dc0b0e87dfc9a90'
    __EXPECTED_RIPEMD160_SHA256 = '1acb19a469206161ed7e5ed9feb996a6e24be441'

    def test_calc_sha256(self):
        result = Hash.calc_sha256(self.__DATA)
        self.assertEqual(self.__EXPECTED_SHA256, result.hex())

    def test_calc_ripemd160_sha256(self):
        result = Hash.calc_ripemd160_sha256(self.__DATA)
        self.assertEqual(self.__EXPECTED_RIPEMD160_SHA256, result.hex())


if __name__ == '__main__':
    unittest.main()
