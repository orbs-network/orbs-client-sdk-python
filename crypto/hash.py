import hashlib


class Hash:
    @staticmethod
    def calc_sha256(data: bytes):
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def calc_ripemd160_sha256(data: bytes):
        sha_output = hashlib.sha256(data).digest()
        ripemd = hashlib.new('ripemd160')
        ripemd.update(sha_output)
        return ripemd.hexdigest()
