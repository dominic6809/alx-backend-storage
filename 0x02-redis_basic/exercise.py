#!/usr/bin/env python3
"""
Cache class for storing data in Redis with a random key.
"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped function that increments the call count.
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """
        Wrapper function that increments the call count in Redis.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the original method.
        """
        self._redis.incr(method.__qualname__)
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
    def wrapper(self: Any, *args) -> str:
        """
        Wrapper function that appends input arguments and output to Redis.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method (ignored).

        Returns:
            The output of the original method.
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output

    return wrapper

def replay(self, method: Callable) -> None:
        """
        Displays the history of calls of a particular function.

        Args:
            method (Callable): The method for which to replay the history.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)

        call_count = len(inputs)
        print(f"{method.__qualname__} was called {call_count} times:")
        
        for input_value, output_value in zip(inputs, outputs):
            print(f"{method.__qualname__}(*{input_value.decode('utf-8')}) -> {output_value.decode('utf-8')}")


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

     def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Retrieves data from Redis and applies an optional conversion function.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A callable to convert the data.

        Returns:
            Optional[Union[str, int]]: The retrieved data, converted by fn if provided.
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

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
