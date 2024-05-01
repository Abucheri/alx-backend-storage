#!/usr/bin/env python3
"""
Module for top students function.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        list: A list of dictionaries containing student details with
             averageScore.
    """
    pipeline = [
        {
            '$project': {
                'name': 1,
                'averageScore': {'$avg': '$topics.score'}
            }
        },
        {'$sort': {'averageScore': -1}}
    ]
    return list(mongo_collection.aggregate(pipeline))
