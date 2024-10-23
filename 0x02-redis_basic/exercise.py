#!/usr/bin/env python3
"""
Cache class for storing data in Redis with a random key.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    params:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped function that increments the call count.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count in Redis.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the original method.
        """
        # Get the qualified name of the method
        key = method.__qualname__
        # Increment the call count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped function that logs inputs and outputs.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that appends input arguments and output to Redis.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method (ignored).

        Returns:
            The output of the original method.
        """
        # Create input and output keys
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input in Redis
        self._redis.rpush(input_key, str(args))

        # Call the original method
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(output_key, output)

        return output

    return wrapper


class Cache:
    """
    A Cache class to interact with Redis for storing data.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache class, creates a Redis client, 
        and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, int]]:
        """
        Retrieves data from Redis and applies an optional conversion function.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A callable to convert the data.

        Returns:
            Optional[Union[str, int]]: The retrieved data, converted by fn if provided.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data from Redis and converts it to a UTF-8 string.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[str]: The retrieved data as a string.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data from Redis and converts it to an integer.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[int]: The retrieved data as an integer.
        """
        return self.get(key, int)
