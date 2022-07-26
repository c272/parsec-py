from enum import Enum


class KeyType(Enum):
    RAW_DATA = 0
    HMAC = 1
    DERIVE = 2
    AES = 3
    DES = 4
    CAMELLIA = 5
    ARC4 = 6
    CHACHA20 = 7
    RSA_PUBLIC_KEY = 8
    RSA_KEY_PAIR = 9
    ECC_KEY_PAIR = 10
    ECC_PUBLIC_KEY = 11
    DH_KEY_PAIR = 12
    DH_PUBLIC_KEY = 13


class KeyPolicy:

    def __init__(self,
                 export=False,
                 copy=False,
                 cache=False,
                 encrypt=False,
                 decrypt=False,
                 sign_message=False,
                 verify_message=False,
                 sign_hash=False,
                 verify_hash=False,
                 derive=False):
        self.export = export
        self.copy = copy
        self.cache = cache
        self.encrypt = encrypt
        self.decrypt = decrypt
        self.sign_message = sign_message
        self.verify_message = verify_message
        self.sign_hash = sign_hash
        self.verify_hash = verify_hash
        self.derive = derive

        # Automatic
        if self.sign_hash:
            self.sign_message = 1
        if verify_hash:
            self.verify_message = 1


class KeyAttributes:

    def __init__(self, key_type: KeyType, key_bits: int, key_policy: KeyPolicy):
        self.key_type = key_type
        self.key_bits = key_bits
        self.key_policy = key_policy




