#!/usr/bin/env python3
"""
web.py: A module for fetching web pages with caching and access counting.
"""

import redis
import requests
from functools import wraps

# Create a Redis client
redis_client = redis.Redis()

def cache_page(method):
    """
    Decorator to cache the result of the function call.

    Args:
        method: The function to be decorated.

    Returns:
        Wrapped function that caches results in Redis.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # Cache key
        cache_key = f"page:{url}"

        # Check if the page is already cached
        cached_page = redis_client.get(cache_key)
        if cached_page:
            # If cached, return the cached page
            return cached_page.decode('utf-8')

        # If not cached, call the original method
        page_content = method(url)

        # Cache the result in Redis with an expiration time of 10 seconds
        redis_client.setex(cache_key, 10, page_content)

        # Increment the access count for the URL
        redis_client.incr(f"count:{url}")

        return page_content

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
