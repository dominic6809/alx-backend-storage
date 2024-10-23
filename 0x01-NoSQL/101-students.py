#!/usr/bin/env python3
""" module for data retrieval """


def top_students(mongo_collection):
    """Returns all students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of students with their average scores included,
        sorted by average score in descending order.
    """
    students = mongo_collection.find()
    result = []

    for student in students:
        total_score = 0
        topics = student.get('topics', [])
        count = len(topics)

        for topic in topics:
            total_score += topic.get('score', 0)

        average_score = total_score / count if count > 0 else 0
        student['averageScore'] = average_score
        result.append(student)

    return sorted(result, key=lambda x: x['averageScore'], reverse=True)
