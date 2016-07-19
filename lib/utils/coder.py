from base64 import standard_b64decode, standard_b64encode


class Coder(object):
    @classmethod
    def encode(cls, s):
        return standard_b64encode(s).decode(encoding='utf-8', errors='strict')

    @classmethod
    def decode(cls, s):
        return standard_b64decode(s.encode(encoding='utf-8', errors='strict'))
