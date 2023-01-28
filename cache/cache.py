import streamlit as st
import pyarrow as pa
import pandas as pd
import pickle
import os
import datetime
from abc import ABC, abstractmethod
from cache.gcp_cache import GcpCache

store = None

class CacheEngineInterface(type):    
    @abstractmethod
    def set(key, value, ttl):
        pass
    
    @abstractmethod
    def get(key):
        pass
    
    @abstractmethod
    def exists(key):
        pass
    
    
def init():
    global store
    store = GcpCache()

def cache_df(key, func, ttl=3600, force_refresh=False):
    """
    Used to cache a dataframe result using pyarrow. Caching is controlled by the key and ttl.
    It will throw exception if the result of the function invocation is not a pandas dataframe object
    """
    context = pa.default_serialization_context()

    global store
    if store is None:
        init()

    res = store.get(key) if not force_refresh else None

    if res != None:
        return context.deserialize(res)
    else:
        with st.spinner(text="Key {} was not in cache".format(key)):
            res = func()
            if not isinstance(res, pd.DataFrame):
                raise Exception(
                    "Result is not a dataframe. You can only use cache_df with functions that return a pandas dataframe."
                )
            store.set(key, context.serialize(
                res).to_buffer().to_pybytes(), ttl)
            return res


def cache_string(key, func, ttl=3600):
    """
    Used to cache a string result. Caching is controlled by the key and ttl.
    It will throw exception if the result of the function invocation is not a string object
    """
    context = pa.default_serialization_context()

    global store
    if store is None:
        init()

    res = store.get(key)

    if res != None:
        return res
    else:
        with st.spinner(text="Key {} was not in cache".format(key)):
            res = func()

            if not isinstance(res, str):
                raise Exception(
                    "Result is not a string. You can only use cache_string with functions that return a string."
                )
            store.set(key, res, ttl)
            return res


def cache(key, func, ttl=3600, force_refresh=False):
    """
    Used to cache any object using pickle (so cached data will not be readable). Caching is controlled by the key and ttl.
    """
    global store
    if store is None:
        init()

    res_cached = store.exists(key) if not force_refresh else False

    if res_cached:
        return _get_pickled_key_from_cache(store, key)
    else:
        with st.spinner(text="Key {} was not in cache so loading the data".format(key)):
            res = func()
            pickled_res = pickle.dumps(res)
            store.set(key, pickled_res, ttl)

            # load it back from the cache to ensure it works
            return _get_pickled_key_from_cache(store, key)


def _get_pickled_key_from_cache(store, key):
    res_cached_pickled = store.get(key)
    if res_cached_pickled is None:
        raise Exception(
            "Key {} does not exist in cache and can not be unpickled".format(
                key)
        )
    res_cached = pickle.loads(res_cached_pickled)
    return res_cached
