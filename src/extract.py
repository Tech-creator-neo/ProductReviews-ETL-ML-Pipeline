import mongomock
import json
import pandas as pd
import requests


def extract_data():
    # 1. Setup mock MongoDB (in-memory)
    client = mongomock.MongoClient()
    db = client.my_mock_database
    review_collection = db.reviews

    # 2. Read local JSONL data
    jsonl_path = "data/raw/product_reviews_sales.jsonl"
    with open(jsonl_path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    # 3. Insert into mock collection
    review_collection.insert_many(data)

    # 4. Create DataFrame from mock collection
    df_reviews = pd.DataFrame(review_collection.find({}))
    if "_id" in df_reviews.columns:
        df_reviews = df_reviews.drop(columns=["_id"])

    # 5. Fetch API data
    api_url = "https://fakestoreapi.com/products"
    response = requests.get(api_url)
    products_df = pd.DataFrame(response.json())

    return df_reviews, products_df





