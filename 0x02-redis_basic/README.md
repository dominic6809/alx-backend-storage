# 0x02-redis_basic
# Redis Caching and Tracking with Python

## Overview

This project demonstrates how to use Redis for caching data and tracking method calls in Python. We implement a caching system to store web page content and count how many times specific methods are called.

## Concepts Covered

1. **Redis Basics**: 
   - Understanding the use of Redis as a caching layer.
   - Utilizing Redis commands like `SET`, `GET`, `INCR`, and list commands like `RPUSH` and `LRANGE`.

2. **Decorator Pattern**:
   - Implementing decorators to enhance method functionality without modifying the original method.
   - Creating a `count_calls` decorator to track the number of times a method is called.
   - Implementing a `call_history` decorator to log the inputs and outputs of method calls.

3. **Web Page Fetching**:
   - Using the `requests` module to retrieve HTML content from a specified URL.
   - Implementing a caching mechanism to store the fetched HTML and count access times with expiration logic.

## Implementation

### Cache Class

- **Initialization**: 
  - Initializes a Redis client and flushes the database.
  
- **Store Method**: 
  - Stores data in Redis with a randomly generated key.

- **Get Method**: 
  - Retrieves data from Redis and allows conversion via a callable.

- **Method Call Tracking**:
  - Uses decorators to track how many times methods are called and log inputs and outputs.

### Web Fetching

- **get_page Function**: 
  - Fetches the HTML content of a given URL and caches it for 10 seconds.
  - Increments the access count for the URL.

## Usage

### Example

```python
from web import get_page

url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://example.com"
content = get_page(url)
print(content)  # Prints the HTML content

# Fetch the page again to check caching
cached_content = get_page(url)
print(cached_content)  # Should print the cached content
```
## Requirements
    Python 3.7+
    Redis Server
    redis and requests Python packages

## Installation
```
  pip install redis requests
```
## Conclusion
This project showcases the integration of Redis with Python to create an efficient caching system and method call tracking mechanism. It provides a foundation for building scalable applications that require data persistence and performance optimization.
```

### Instructions

- Feel free to modify any sections to better suit your project specifics or personal preferences.
- You can save this README as `README.md` in your project directory for easy reference. 
