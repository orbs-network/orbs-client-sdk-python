from securesystemslib import ed25519_keys
from crypto.keys import Keys


class Signature:

    ED25519_SIGNATURE_SIZE_BYTES = 64

    @staticmethod
    def sign_ed25519(private_key: bytes, data: bytes):
        if len(private_key) != Keys.ED25519_PRIVATE_KEY_SIZE_BYTES:
            raise ValueError(f'cannot sign with ed25519, invalid length of private key {len(private_key)}')
        private_key_value = private_key[:Keys.ED25519_PUBLIC_KEY_SIZE_BYTES]
        public_key = private_key[Keys.ED25519_PUBLIC_KEY_SIZE_BYTES:]

        scheme = 'ed25519'
        signature, scheme = ed25519_keys.create_signature(public_key, private_key_value, data, scheme)
        return signature

    @staticmethod
    def verify_ed25519(public_key: bytes, data: bytes, signature: bytes):
        if len(public_key) != Keys.ED25519_PUBLIC_KEY_SIZE_BYTES:
            raise ValueError(f'cannot verify with ed25519, invalid length of public key {len(public_key)}')
        scheme = 'ed25519'
        return ed25519_keys.verify_signature(public_key, scheme, signature, data, True)