import unittest
from os import sys, path
from crypto.base58_encoding import Base58
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestBase58Functions(unittest.TestCase):

    def test_encode_base58(self):
        data = "helloworldandstuff1124z24"
        expected_base58string = "j1Q1Y54mCcVfR5jVAQMMJEy6VbZEtYeM3R"
        encoded = Base58.encode(data)
        self.assertEqual(expected_base58string, encoded)

    def test_encode_binary_data(self):
        source = bytes([1, 2, 3, 4])
        encoded = Base58.encode(source)
        decoded = Base58.decode(encoded)
        self.assertEqual(decoded, source)


if __name__ == '__main__':
    unittest.main()
