import os
from pymongo import MongoClient


MONGO_URI = os.getenv("MONGO_DB")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["HrManagement"]