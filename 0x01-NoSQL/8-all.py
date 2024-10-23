#!/usr/bin/env python3
""" module for lists all """


def list_all(mongo_collection):
    """Lists all documents in a collection.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of documents or an empty list if no documents are found.
    """
    if mongo_collection.count_documents({}) > 0:
        return list(mongo_collection.find())
    return []
