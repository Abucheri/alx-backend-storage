#!/usr/bin/env python3
"""
Cache module implementing Redis caching.
"""

import redis
import uuid
from typing import Union, Callable


class Cache:
    """
    Cache class for interacting with Redis as a cache.
    """
    def __init__(self):
        """
        Initializes the Cache object with a Redis client instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored
                                                  in the cache.
        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis using the given key and optionally applies
        a conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Callable, optional): A callable function used to convert the
                                     retrieved data. Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, converted
                                                 using the provided function
                                                 if applicable.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves data from Redis as a string.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Union[str, None]: The retrieved data as a string, or None if the
                              key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves data from Redis as an integer.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Union[int, None]: The retrieved data as an integer, or None if the
                              key does not exist.
        """
        return self.get(key, fn=int)
