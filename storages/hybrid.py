import time
import uuid


class HybridStorage(object):

    _IS_PART_IN_REDIS = 1

    _DEFAULT_TIME_DELTA = 10*24*60*60

    _UUID_LENGTH = 16

    def __init__(self, strict_redis_client, cookie_name, max_cookie_limit=4000, time_delta=_DEFAULT_TIME_DELTA):
        self._redis_client = strict_redis_client
        self._cookie_name = cookie_name
        self._max_cookie_limit = max_cookie_limit
        self._time_delta = time_delta

    def store(self, response, storage_id, data, purge_old_data=True):
        metadata = bytes([0])

        if len(data) <= (self._max_cookie_limit - 1):
            response.set_cookie(self._cookie_name, metadata + data, expires=time.time() + self._time_delta)

            if purge_old_data:
                self._redis_client.delete(storage_id.hex())

            return metadata + data

        metadata = bytes([1])
        if storage_id is None:
            storage_id = uuid.uuid4()

        whole_data = metadata + storage_id.bytes() + data
        cookie_part = whole_data[0:self._max_cookie_limit]
        redis_part = whole_data[self._max_cookie_limit:len(whole_data)]

        response.set_cookie(self._cookie_name, cookie_part, expires=time.time() + self._time_delta)
        self._redis_client.set(storage_id.hex(), redis_part, self._time_delta)
        return whole_data

    def retrieve(self, request):
        cookie_part = request.cookies.get(self._cookie_name)
        if cookie_part is None:
            return None

        metadata = cookie_part[0]
        if metadata != 1 and metadata != 0:
            return None

        if len(cookie_part) < len(metadata) + self._UUID_LENGTH:
            return None

        storage_id = uuid.UUID(bytes=cookie_part[len(metadata):self._UUID_LENGTH+len(metadata)])

        redis_part = self._redis_client.get(storage_id.hex())
        if redis_part is None:
            return None

        self._redis_client.expire(redis_part, self._time_delta)

        return storage_id, cookie_part[(len(metadata)+self._UUID_LENGTH):len(cookie_part)] + redis_part
