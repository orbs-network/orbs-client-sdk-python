import unittest
from os import sys, path
from crypto.signature import Signature
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestSignatureFunctions(unittest.TestCase):

    def test_sign_ed25519(self):
        private_key = bytes.fromhex('3b24b5f9e6b1371c3b5de2e402a96930eeafe52111bb4a1b003e5ecad3fab53892d469d7c004cc0b24a192d9457836bf38effa27536627ef60718b00b0f33152')
        public_key = bytes.fromhex('92d469d7c004cc0b24a192d9457836bf38effa27536627ef60718b00b0f33152')
        data = b'This is what we want to sign'

        sig = Signature.sign_ed25519(private_key, data)
        self.assertEqual(Signature.ED25519_SIGNATURE_SIZE_BYTES, len(sig), 'signature length should equal 64 bytes')
        self.assertEqual(Signature.verify_ed25519(public_key, data, sig), True, 'signature cannot be verified')

        modified_sig = bytearray(sig)
        modified_sig[0] += 1  # corrupt the signature
        sig = bytes(modified_sig)
        self.assertEqual(Signature.verify_ed25519(public_key, data, sig), False)


if __name__ == '__main__':
    unittest.main()
