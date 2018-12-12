from typing import NamedTuple
from crypto.keys import Keys
from crypto.hash import Hash
from crypto.base58_encoding import Base58


class Account(NamedTuple):
    public_key: bytes
    private_key: bytes
    address: str
    raw_address: bytes

    @staticmethod
    def create_account():
        private_key, public_key = Keys.generate_ed25519_key()
        raw_address = Hash.calc_ripemd160_sha256(public_key)
        return Account(public_key, private_key, Base58.encode(raw_address), raw_address)
