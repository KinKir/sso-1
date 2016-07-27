import time
import uuid


class HybridStorage(object):

    _IS_PART_IN_REDIS = 1

    _DEFAULT_TIME_DELTA = 10*24*60*60

    _UUID_HEX_LENGTH = 32

    _PARTIAL_COOKIE = 'r'

    _WHOLE_COOKIE = 'c'

    def __init__(self, strict_redis_client, cookie_name, max_cookie_limit=4000, time_delta=_DEFAULT_TIME_DELTA):
        self._redis_client = strict_redis_client
        self._cookie_name = cookie_name
        self._max_cookie_limit = max_cookie_limit
        self._time_delta = time_delta

    def store(self, response, storage_id, data, purge_old_data=True):
        metadata = self._WHOLE_COOKIE

        if len(data) <= (self._max_cookie_limit - 1):
            response.set_cookie(self._cookie_name, metadata + data,
                                expires=time.time() + self._time_delta)

            if purge_old_data:
                self._redis_client.delete(storage_id)

            return metadata + data

        metadata = self._PARTIAL_COOKIE
        if storage_id is None:
            storage_id = uuid.uuid4()

        whole_data = metadata + storage_id.hex + data
        cookie_part = whole_data[0:self._max_cookie_limit]
        redis_part = whole_data[self._max_cookie_limit:len(whole_data)]

        response.set_cookie(self._cookie_name, cookie_part, expires=time.time() + self._time_delta)
        self._redis_client.set(storage_id.hex, redis_part, self._time_delta)
        return whole_data

    def retrieve(self, request):
        cookie_part = request.cookies.get(self._cookie_name)
        if cookie_part is None:
            return None

        metadata = cookie_part[0]
        if metadata != self._PARTIAL_COOKIE and metadata != self._WHOLE_COOKIE:
            return None

        if metadata == self._WHOLE_COOKIE:
            return cookie_part[1:]

        if len(cookie_part) < (len(metadata) + self._UUID_HEX_LENGTH):
            return None

        storage_id = uuid.UUID(hex=cookie_part[len(metadata):self._UUID_HEX_LENGTH+len(metadata)])

        redis_part = self._redis_client.get(storage_id).decode(encoding='utf-8', errors='strict')
        if redis_part is None:
            return None

        self._redis_client.expire(storage_id, self._time_delta)

        return storage_id, cookie_part[(len(metadata)+self._UUID_HEX_LENGTH):len(cookie_part)] + redis_part
