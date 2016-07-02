from base64 import standard_b64decode, standard_b64encode


def encode(s):
    return standard_b64encode(s).decode(encoding='utf-8', errors='strict')


def decode(s):
    return standard_b64decode(s.encode(encoding='utf-8', errors='strict'))
