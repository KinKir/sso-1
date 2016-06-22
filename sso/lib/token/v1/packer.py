
IV_LENGTH = 32

TAG_LENGTH = 16

KEYID_LENGTH = 16


def pack(iv, ciphertext, tag, aad, keyid):

    if len(iv) != IV_LENGTH:
        pass

    if len(tag) != TAG_LENGTH:
        pass

    if len(keyid) != KEYID_LENGTH:
        pass

    if aad is None:
        meta = bytes([0]) + len(ciphertext).to_bytes(8, 'big')
        package_length = len(iv) + len(ciphertext) + len(tag) + len(keyid) + len(meta)
    else:
        meta = bytes([len(aad)]) + len(ciphertext).to_bytes(8, 'big')
        package_length = len(iv) + len(ciphertext) + len(tag) + len(aad) + len(keyid) + len(meta)

    result = bytearray(0**package_length)

    filledup_length = 0

    result[filledup_length:filledup_length+len(meta)] = meta
    filledup_length += len(meta)

    result[filledup_length:filledup_length+len(iv)] = iv
    filledup_length += len(iv)

    result[filledup_length:filledup_length+len(tag)] = tag
    filledup_length += len(tag)

    result[filledup_length:filledup_length+len(keyid)] = keyid
    filledup_length += len(keyid)

    if aad is not None:
        result[filledup_length:filledup_length+len(aad)] = aad
        filledup_length += len(aad)

    result[filledup_length:filledup_length+len(ciphertext)] = ciphertext
    filledup_length += len(ciphertext)

    return result


def unpack(packed):
    meta = packed[0:2]

    aad_length = meta[0]
    ciphertext_length = meta[1]


