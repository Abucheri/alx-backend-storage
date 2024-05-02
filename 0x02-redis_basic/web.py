#!/usr/bin/env python3
"""
Module for implementing a web cache and tracker with a custom
decorator using functools.wraps.
"""

import requests
import redis
from typing import Callable
from functools import wraps

cache = redis.Redis()


def track_and_cache(method: Callable) -> Callable:
    """
    Custom decorator to track the number of accesses for a URL and cache the
    result with an expiration time of 10 seconds.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function
    """
    @wraps(method)
    def wrapper(url):
        """
        The wrapper
        """
        cache.incr(f"count:{url}")
        cached_html = cache.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        html_content = method(url)
        cache.setex(f"cached:{url}", 10, html_content)
        return html_content
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
