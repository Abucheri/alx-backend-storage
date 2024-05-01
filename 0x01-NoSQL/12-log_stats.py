#!/usr/bin/env python3
"""
Module for providing stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats():
    """
    Provides stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    # Total number of documents
    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    # Methods count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count of documents with method=GET and path=/status
    status_check = collection.count_documents({"method": "GET",
                                              "path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
