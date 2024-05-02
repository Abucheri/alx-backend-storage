#!/usr/bin/env python3
"""
Module for implementing a web cache and tracker with a custom
decorator using functools.wraps.
"""

import requests
import redis
import time
from typing import Callable
from functools import wraps


def track_and_cache(method: Callable) -> Callable:
    """
    Custom decorator to track the number of accesses for a URL and cache the
    result with an expiration time of 10 seconds.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # Initialize Redis connection
        redis_conn = redis.Redis()

        # Track the number of accesses for this URL
        count_key = f"count:{url}"
        redis_conn.incr(count_key)

        # Check if the result is already cached
        cache_key = f"cache:{url}"
        cached_result = redis_conn.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')

        # If not cached, retrieve HTML content of the URL
        response = method(url)

        # Cache the result with an expiration time of 10 seconds
        redis_conn.setex(cache_key, 10, response)

        return response

    return wrapper


@track_and_cache
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL.

    Args:
        url (str): The URL of the webpage to retrieve.

    Returns:
        str: The HTML content of the webpage.
    """
    # Retrieve HTML content of the URL
    response = requests.get(url)
    return response.text
