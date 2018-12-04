from base58 import b58encode, b58decode


class Base58:
    @staticmethod
    def encode(data):
        return b58encode(data)

    @staticmethod
    def decode(data):
        return b58decode(data)
