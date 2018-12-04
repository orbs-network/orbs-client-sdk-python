from securesystemslib import ed25519_keys


class Keys:

    ED25519_PUBLIC_KEY_SIZE_BYTES = 32
    ED25519_PRIVATE_KEY_SIZE_BYTES = 64

    @staticmethod
    def generate_ed25519_key():
        public_key, private_key = ed25519_keys.generate_public_and_private()

        # added this concatenation to be compatible with Go's EDDSA library implementation
        key_pair = private_key + public_key
        return key_pair, public_key
