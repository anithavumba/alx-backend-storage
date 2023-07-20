#!/usr/bin/env python3
import requests
import time

# Dictionary to keep track of the count of URL accesses
url_count = {}

# Dictionary to store the cached content and timestamps
cache = {}

# Decorator for tracking URL accesses
def track_url_access(func):
    def wrapper(url):
        # Check if the URL has been accessed before
        if url in url_count:
            url_count[url] += 1
        else:
            url_count[url] = 1
        return func(url)
    return wrapper

# Decorator for caching URL content with a 10-second expiration time
def cache_url_content(func):
    def wrapper(url):
        # Check if the URL content is already cached
        if 'content:{url}' in cache and 'timestamp:{url}' in cache:
            timestamp = cache['timestamp:{url}']
            current_time = int(time.time())
            # If the cached content is still valid (within 10 seconds), return it
            if current_time - timestamp < 10:
                return cache['content:{url}']
        
        # If the URL content is not cached or expired, fetch it
        response = func(url)
        
        # Cache the fetched content and its timestamp
        cache['content:{url}'] = response
        cache['timestamp:{url}'] = int(time.time())
        
        return response
    return wrapper

@track_url_access
@cache_url_content
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
