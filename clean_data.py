from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


URI = "HIDDEN"

def main():
    # Replace with your MongoDB Atlas connection string and Admin API key
    client = MongoClient(URI, server_api=ServerApi('1'))

    # Create a database and collection
    db = client["quest_db"]
    collection = db["restaurants_GOOGLE"]

    # Find all documents with the same place_id
    pipeline = [
        {
            "$group": {
                "_id": "$place_id",
                "count": {"$sum": 1},
                "docs": {"$push": "$$CURRENT"}
            }
        },
        {"$match": {"count": {"$gt": 1}}}
    ]

    result = collection.aggregate(pipeline)

    # Remove duplicate documents
    i = 0
    for doc in result:
        place_id = doc["_id"]
        duplicate_docs = doc["docs"][1:]  # Keep the first document
        for duplicate_doc in duplicate_docs:
            i = i + 1
            collection.delete_one({"_id": duplicate_doc["_id"]})

    print(str(i) + " total documents removed.")
    print("Duplicate documents removed.")

if __name__ == "__main__":
    main()