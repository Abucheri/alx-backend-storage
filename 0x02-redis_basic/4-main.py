#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache
cache_0 = __import__('exercise').replay

cache = Cache()

cache.store("foo")
cache.store("bar")
cache.store(42)

cache_0(cache.store)
