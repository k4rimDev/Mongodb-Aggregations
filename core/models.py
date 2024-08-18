import os
from pymongo import MongoClient


client = MongoClient(
    host=os.getenv('MONGO_DB_HOST', 'localhost'),
    port=27017,
    username=os.getenv('MONGO_DB_USERNAME'),
    password=os.getenv('MONGO_DB_PASSWORD'),
    authSource='admin'
)

db = client[os.getenv('MONGO_DB_NAME', 'mydatabase')]
collection = db['feedback']


class Feedback:
    @staticmethod
    def group_feedback_by_branch_service():
        pipeline = [
            {"$unwind": "$feedback_rate"},
            {
                "$group": {
                    "_id": {
                        "branch_name": "$branch.name",
                        "service_name": "$feedback_rate.service.name"
                    },
                    "rate_options": {"$push": "$feedback_rate.rate_option"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "branch_name": "$_id.branch_name",
                    "service_name": "$_id.service_name",
                    "rate_counts": {
                        "1": {"$size": {"$filter": {"input": "$rate_options", "as": "rate", "cond": {"$eq": ["$$rate", 1]}}}},
                        "2": {"$size": {"$filter": {"input": "$rate_options", "as": "rate", "cond": {"$eq": ["$$rate", 2]}}}},
                        "3": {"$size": {"$filter": {"input": "$rate_options", "as": "rate", "cond": {"$eq": ["$$rate", 3]}}}},
                        "4": {"$size": {"$filter": {"input": "$rate_options", "as": "rate", "cond": {"$eq": ["$$rate", 4]}}}},
                        "5": {"$size": {"$filter": {"input": "$rate_options", "as": "rate", "cond": {"$eq": ["$$rate", 5]}}}},
                    },
                    "total_count": {"$size": "$rate_options"},
                }
            },
            {
                "$addFields": {
                    "positive_score": {
                        "$sum": [
                            {"$multiply": ["$rate_counts.1", 10]},
                            {"$multiply": ["$rate_counts.2", 5]}
                        ]
                    },
                    "negative_score": {
                        "$sum": [
                            {"$multiply": ["$rate_counts.4", -5]},
                            {"$multiply": ["$rate_counts.5", -10]}
                        ]
                    },
                    "total_score": {
                        "$sum": [
                            {"$multiply": ["$rate_counts.1", 10]},
                            {"$multiply": ["$rate_counts.2", 5]},
                            {"$multiply": ["$rate_counts.4", -5]},
                            {"$multiply": ["$rate_counts.5", -10]}
                        ]
                    }
                }
            },
            {
                "$addFields": {
                    "calculated_value": {
                        "$cond": {
                            "if": {"$eq": ["$total_count", 0]},
                            "then": None,
                            "else": {
                                "$round": [
                                    {
                                        "$multiply": [
                                            100,
                                            {
                                                "$divide": ["$total_score", {"$multiply": ["$total_count", 10]}]
                                            }
                                        ]
                                    },
                                    3
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$sort": {"calculated_value": -1}
            },
            {
                "$project": {
                    "branch_name": 1,
                    "service_name": 1,
                    "rate_counts": 1,
                    "total_count": 1,
                    "positive_score": 1,
                    "negative_score": 1,
                    "total_score": 1,
                    "calculated_value": 1
                }
            }
        ]

        return list(collection.aggregate(pipeline))
