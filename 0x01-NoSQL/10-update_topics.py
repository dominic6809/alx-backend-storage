#!/usr/bin/env python3
""" module for update_topics """


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a school document.

    Args:
        mongo_collection: The pymongo collection object.
        name (str): The name of the school to update.
        topics (list): A list of topics to set.

    Returns:
        None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
