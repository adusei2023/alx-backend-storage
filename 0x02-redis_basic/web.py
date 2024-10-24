#!/usr/bin/env python3
""" Expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Create a Redis connection with error handling
try:
    redis_client = redis.Redis()
except redis.exceptions.ConnectionError as e:
    print(f"Redis connection error: {e}")
    exit(1)


def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper function """
        try:
            # Increment access count
            redis_client.incr(f"count:{url}")
            
            # Check if the response is cached
            cached_response = redis_client.get(f"cached:{url}")
            if cached_response:
                return cached_response.decode('utf-8')

            # Fetch the page if not cached
            result = fn(url)
            
            # Cache the result with 10 seconds expiration
            redis_client.setex(f"cached:{url}", 10, result)
            return result

        except (requests.RequestException, redis.exceptions.RedisError) as e:
            print(f"Error occurred: {e}")
            return "An error occurred while processing the request."

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """ Fetches the HTML content of a URL """
    response = requests.get(url)
    return response.text


# Test the implementation
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    print(get_page(test_url))
    print(f"Access count: {redis_client.get(f'count:{test_url}').decode('utf-8')}")
