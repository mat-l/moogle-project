"""
This module contains 2 things:
1) The open_redis_connection() to be called anywhere in the code when we need to talk to Redis.
It is build such as it uses a unique connection pool (in case of TCP socket connection, while
no connection pool in required in case of unix socket connection). It returns a `redis.StrictRedis`
object, see: http://redis-py.readthedocs.org/en/latest/index.html#redis.StrictRedis
Use it like this:
    redis = open_redis_connection()
    print(redis.info())

2) RedisStore class with some helper methods to do some operations required by this codebase.
Use it like this:
    redis_store = RedisStore()
    redis_store.store_entry_to_be_downloaded(...)
"""

import redis

from magpie.settings import settings
from .exceptions import ImproperlyConfigured


pool = 0


def open_redis_connection():
    """
    Generic function to call in order to talk to Redis. It is build such as it uses a unique
    connection pool (in case of TCP socket connection, while no connection pool in required
    in case of unix socket connection).
    Use it like this:
        redis = open_redis_connection()
        print(redis.info())
    """
    global pool

    if 'TCP_SOCKET' in settings.REDIS:
        if pool == 0:
            pool = _build_connection_pool()
        # TODO change this prints to log.debug to console
        print("+++++++++++++++++++++++++++ Opening a connection to Redis")
        return redis.StrictRedis(connection_pool=pool)

    if 'UNIX_SOCKET' in settings.REDIS:
        print("+++++++++++++++++++++++++++ Opening a connection to Redis")
        return redis.Redis(unix_socket_path=settings.REDIS['UNIX_SOCKET']['PATH'])

    raise ImproperlyConfigured('You must set proper Redis connection details in the'
                               ' settings file.')


def _build_connection_pool():
    print("+++++++++++++++++++++++++++ Building a connection pool to Redis")
    if 'TCP_SOCKET' in settings.REDIS:
        return redis.ConnectionPool(
            host=settings.REDIS['TCP_SOCKET']['HOST'],
            port=settings.REDIS['TCP_SOCKET']['PORT'],
            db=settings.REDIS['TCP_SOCKET']['DB']
        )
    return None


class RedisStore:
    """
    Class with some helper methods to do some operations required by this codebase.
    Use it like this:
        redis_store = RedisStore()
        redis_store.store_entry_to_be_downloaded(...)
    """
    def __init__(self, bearertoken_id):
        #self.bearertoken_id = bearertoken_id
        self._download_list_name = 'token:{}:dw'.format(bearertoken_id)
        self._index_list_name = 'token:{}:ix'.format(bearertoken_id)
        self._download_buffer = None

    def add_to_download_list_buffer(self, entry):
        """
        Add `DropboxResponseEntry` to the download pipeline (Redis' buffer).
        Each entry in the download pipeline maps a file to be downloaded from Dropbox.
        """
        print("Storing {} in Redis.".format(entry))

        if not self._download_buffer:
            r = open_redis_connection()
            self._download_buffer = r.pipeline()

        self._download_buffer.rpush(
            self._download_list_name,
            '{}{}'.format(entry.operation_type, entry.path)
        )

    def flush_download_list_buffer(self):
        """
        Flush the download pipeline (Redis' buffer) to Redis.
        Each entry in the download pipeline maps a file to be downloaded from Dropbox.
        """
        if self._download_buffer:
            self._download_buffer.execute()

    def iter_over_download_list(self):
        """
        Iterate over the Redis download list for the current `bearertoken_id`.
        Return a iterator object which iterates over `RedisDownloadEntry` objects.
        Usage:
            redis_store = RedisStore(self.bearertoken_id)
            for redis_dw_entry in redis_store.iter_over_download_list():
                print(redis_dw_entry.operation_type, redis_dw_entry.remote_path)
        """
        r = open_redis_connection()

        def _lpop_dw():
            """
            Pop from the head of the Redis download list for the current `bearertoken_id`.
            Convert the item to `RedisDownloadEntry`.
            """
            redis_entry = r.lpop(self._download_list_name)
            if redis_entry:
                redis_entry = RedisDownloadEntry(redis_entry)
            return redis_entry

        # The first argument of iter must be a callable, that's why we created the _lpop_dw()
        # closure. This closure will be called for each iteration and the result is returned
        # until the result is None.
        return iter(_lpop_dw, None)


class RedisDownloadEntry:
    """
    A entry of a Redis download list.

    Parameters:
    redis_bytes_string -- a original entry of a Redis download list, like: b"+/dir1/file2.txt"
    It is a bytes string in Python.
    """
    def __init__(self, redis_bytes_string):
        self.operation_type = redis_bytes_string[:1].decode(encoding='UTF-8')
        self.remote_path = redis_bytes_string[1:].decode(encoding='UTF-8')