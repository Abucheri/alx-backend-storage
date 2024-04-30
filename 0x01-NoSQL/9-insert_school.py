#!/usr/bin/env python3
"""
Module for inserting a new document in a collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection: pymongo collection object.
        **kwargs: Keyword arguments representing the attributes
                  of the document.
    Returns:
        new_id: The _id of the newly inserted document.
    """
    new_id = mongo_collection.insert_one(kwargs).inserted_id
    return new_id
