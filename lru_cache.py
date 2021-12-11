from collections import namedtuple, OrderedDict


def lru_cache(func, maxsize=128):
    """A LRU-cache wrapper.

    The LRU-cache stores function results for the most recent calls
    with a default maximum size of 128.

    Args:
        func (function): A function used to get wrapped in lru_cache.
        maxsize (int): The maximum size of the lru_cache (default to
            be 128).

    Returns:
        function: A function in which the func is called with arbitrary
            positional arguments, an LRU cache and the info of the cache
            is maintained, and a function attribute cache_info() implemented
            to return the info of the cache.

    """
    CacheInfo = namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])
    cache = OrderedDict()
    hits = 0
    misses = 0

    def inner(*args):
        """A function in which the func is called with arbitrary
            positional arguments, an LRU cache and the info of the cache
            is maintained, and a function attribute cache_info() implemented
            to return the info of the cache.

        Args:
            *args: An arbitrary number of arguments for the func.

        Returns:
            The result of func.

        """
        nonlocal hits
        nonlocal misses
        nonlocal cache
        for key in args:
            if key not in cache:
                misses += 1
                result = func(*args)
                add_to_cache(maxsize, cache, key, result)
            else:
                hits += 1
                result = cache[key]
                add_to_cache(maxsize, cache, key, result)
            return result

    def cache_info():
        """Gets the info of the cache.

        Returns:
            NamedTuple: The info of the cache, including
                hits, misses, maxsize and current size.

        """
        return CacheInfo(hits, misses, maxsize, len(cache))

    inner.cache_info = cache_info
    return inner


def add_to_cache(maxsize, cache, key, value):
    """Adds a key-value pair to an OrderedDict.

    Args:
        maxsize (int): The maximum size of the cache.
        cache (OrderedDict): An OrderedDict storing each input
            and its result of func.
        key: The key of a new entry.
        value: The value of a new entry.

    """
    cache[key] = value
    cache.move_to_end(key)
    if len(cache) > maxsize:
        cache.popitem(last=False)
