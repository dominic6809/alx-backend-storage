#!/usr/bin/env python3
""" module for insertion """


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into a collection.

    Args:
        mongo_collection: The pymongo collection object.
        **kwargs: The fields to include in the new document.

    Returns:
        The new document's _id.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
