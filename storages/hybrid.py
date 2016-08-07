import time
import uuid


class HybridStorage(object):

    _DEFAULT_TIME_DELTA = 10*24*60*60

    _UUID_HEX_LENGTH = 32

    _HMAC_LENGTH = 64

    _META_DATA_LENGTH = 1

    _PARTIAL_COOKIE = 'r'

    _WHOLE_COOKIE = 'c'

    def __init__(self, strict_redis_client, cookie_name, hmac_secret_key, max_cookie_limit=4000, time_delta=_DEFAULT_TIME_DELTA):
        self._redis_client = strict_redis_client
        self._cookie_name = cookie_name
        self._max_cookie_limit = max_cookie_limit
        self._time_delta = time_delta
        self._hmac_secret_key = hmac_secret_key

    def delete(self, request, response):
        cookie_part = request.cookies.get(self._cookie_name)
        response.set_cookie(self._cookie_name, '', expires=0)

        if cookie_part is None:
            return

        metadata = cookie_part[0]
        if metadata != self._PARTIAL_COOKIE and metadata != self._WHOLE_COOKIE:
            return

        if metadata == self._WHOLE_COOKIE:
            return

        if len(cookie_part) < (len(metadata) + self._UUID_HEX_LENGTH):
            return

        storage_id = uuid.UUID(hex=cookie_part[len(metadata):self._UUID_HEX_LENGTH+len(metadata)])
        self._redis_client.delete(storage_id)

    def _attach_cookie_hmac(self, cookie_part):
        pass

    def store(self, response, storage_id, data, purge_old_data=True):
        metadata = self._WHOLE_COOKIE

        if len(data) <= (self._max_cookie_limit - self._META_DATA_LENGTH - self._HMAC_LENGTH):
            response.set_cookie(self._cookie_name, metadata + data,
                                expires=time.time() + self._time_delta)

            if purge_old_data and storage_id is not None:
                self._redis_client.delete(storage_id.hex)

            return metadata + data

        metadata = self._PARTIAL_COOKIE
        if storage_id is None:
            storage_id = uuid.uuid4()

        whole_data = metadata + storage_id.hex + data
        cookie_part = whole_data[0:(self._max_cookie_limit - self._HMAC_LENGTH)]
        cookie_part_with_hmac = self._attach_cookie_hmac(cookie_part)
        redis_part = whole_data[self._max_cookie_limit:len(whole_data)]

        response.set_cookie(self._cookie_name, cookie_part_with_hmac, expires=time.time() + self._time_delta)
        self._redis_client.set(storage_id.hex, redis_part, self._time_delta)
        return whole_data

    def _detach_cookie_hmac(self, cookie_part):
        pass

    def _verify_cookie_hmac(self, hmac, cookie_part):
        pass

    def retrieve(self, request):
        cookie_part_with_hmac = request.cookies.get(self._cookie_name)
        if cookie_part_with_hmac is None:
            return None, None

        hmac, cookie_part = self._detach_cookie_hmac(cookie_part_with_hmac)
        if hmac is None:
            return None, None

        if not self._verify_cookie_hmac(hmac, cookie_part):
            return None, None

        metadata = cookie_part[0]
        if metadata != self._PARTIAL_COOKIE and metadata != self._WHOLE_COOKIE:
            return None, None

        if metadata == self._WHOLE_COOKIE:
            return None, cookie_part[1:]

        if len(cookie_part) < (len(metadata) + self._UUID_HEX_LENGTH):
            return None, None

        storage_id = uuid.UUID(hex=cookie_part[len(metadata):self._UUID_HEX_LENGTH+len(metadata)])

        redis_part_binary = self._redis_client.get(storage_id.hex)
        if redis_part_binary is None:
            return None, None

        redis_part = redis_part_binary.decode(encoding='utf-8', errors='strict')
        if redis_part is None:
            return None, None

        self._redis_client.expire(storage_id.hex, self._time_delta)

        return storage_id, cookie_part[(len(metadata)+self._UUID_HEX_LENGTH):len(cookie_part)] + redis_part
