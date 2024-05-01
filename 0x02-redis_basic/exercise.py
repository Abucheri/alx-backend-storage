#!/usr/bin/env python3
"""
Cache module implementing Redis caching.
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: Decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count for the method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: Decorated method:
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores input and output history.
        """
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Store input arguments
        self._redis.rpush(inputs_key, str(args))

        # Execute the original method to get the output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(outputs_key, output)

        return output
    return wrapper


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

    @call_history
    @count_calls
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
