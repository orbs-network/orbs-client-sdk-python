from crypto.hash import Hash


class Digest:

    __TX_HASH_BYTES = 32
    TX_TIMESTAMP_BYTES = 8
    TX_ID_SIZE_BYTES = __TX_HASH_BYTES + TX_TIMESTAMP_BYTES

    @staticmethod
    def calc_tx_hash(transaction_buf: bytes):
        return Hash.calc_sha256(transaction_buf)

    @staticmethod
    def generate_tx_id(tx_hash: bytes, tx_timestamp: int):
        formatted_timestamp = tx_timestamp.to_bytes(8, byteorder='little', signed=False)
        result = formatted_timestamp + tx_hash
        return result

    @staticmethod
    def extract_tx_id(tx_id: bytes):
        if len(tx_id) != Digest.TX_ID_SIZE_BYTES:
            raise ValueError(f'tx_id has an invalid length: {len(tx_id)}')
        tx_timestamp = int.from_bytes(tx_id[:Digest.TX_TIMESTAMP_BYTES], byteorder='little', signed=False)
        tx_hash = tx_id[Digest.TX_TIMESTAMP_BYTES:]
        return tx_hash, tx_timestamp

