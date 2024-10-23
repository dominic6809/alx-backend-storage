#!/usr/bin/env python3
""" Test script for web.py """

from web import get_page
import redis

# Connect to Redis
redis_client = redis.Redis()  # Ensure this matches your Redis server configuration

# Define the URL to test
url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://example.com"

# Fetch the page
print("Fetching page...")
content = get_page(url)
print(content)  # Prints the HTML content of the page

# Fetch the page again to check caching
print("Fetching page again...")
cached_content = get_page(url)
print(cached_content)  # Should print the cached content

# Check the access count
count = redis_client.get(f"count:{url}")
print(f"Access count for {url}: {count.decode('utf-8')}")
