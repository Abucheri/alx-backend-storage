#!/usr/bin/env python3
"""
Module for retrieving schools by topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        list: A list of schools having the specified topic.
    """
    return list(mongo_collection.find({"topics": {"$in": [topic]}}))
