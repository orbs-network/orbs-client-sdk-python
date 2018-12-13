import unittest
from os import sys, path
from crypto.keys import Keys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestKeysFunctions(unittest.TestCase):

    def test_generate_ed25519_key(self):
        first_private_key, first_public_key = Keys.generate_ed25519_key()
        print(f'First private key: {first_private_key.hex()}')
        print(f'First public key: {first_public_key.hex()}')
        self.assertEqual(Keys.ED25519_PRIVATE_KEY_SIZE_BYTES, len(first_private_key), 'private key length should equal 64 bytes')
        self.assertEqual(Keys.ED25519_PUBLIC_KEY_SIZE_BYTES, len(first_public_key), 'public key length should equal 32 bytes')

        second_private_key, second_public_key = Keys.generate_ed25519_key()
        print(f'Second private key: {second_private_key.hex()}')
        print(f'Second public key: {second_public_key.hex()}')
        self.assertNotEqual(first_private_key, second_private_key, 'generated keys are equal')


if __name__ == '__main__':
    unittest.main()
