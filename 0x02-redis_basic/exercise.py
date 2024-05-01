#!/usr/bin/env python3
"""
Cache module implementing Redis caching.
"""

import redis
import uuid
from typing import Union


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
