#!/usr/bin/env python3
import requests
import time
from datetime import datetime, timedelta
from functools import wraps

CACHE_EXPIRATION_SECONDS = 10
CACHE = {}

def caching_decorator(func):
    @wraps(func)
    def wrapper(url):
        now = datetime.now()
        cache_key = f"cache:{url}"
        
        # Check if the cached data is still valid
        if cache_key in CACHE and CACHE[cache_key]['expires'] > now:
            return CACHE[cache_key]['content']
        
        # If not cached or expired, fetch the page and update the cache
        response = func(url)
        CACHE[cache_key] = {
            'content': response,
            'expires': now + timedelta(seconds=CACHE_EXPIRATION_SECONDS)
        }
        return response
    return wrapper

@caching_decorator
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    print(get_page(url))
    time.sleep(5)  # Wait 5 seconds to allow cache to expire
    print(get_page(url))
