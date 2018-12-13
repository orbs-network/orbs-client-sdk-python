from base58 import b58encode, b58decode


class Base58:
    @staticmethod
    def encode(data: bytes) -> str:
        return b58encode(data).decode('utf-8')

    @staticmethod
    def decode(data: str) -> bytes:
        return b58decode(data)
