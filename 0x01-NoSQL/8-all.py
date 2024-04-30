#!/usr/bin/env python3
"""
Module for listing all documents in a collection.
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        list: A list of documents in the collection.
    """
    return mongo_collection.find()
