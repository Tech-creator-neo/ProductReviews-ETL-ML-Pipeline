# tests/test_transform.py
import os
import pandas as pd
from scripts.extract import extract_data
from scripts.transform import transform_data

def test_transform_runs():
    df_reviews, products_df = extract_data()
    combined = transform_data(df_reviews, products_df)

    assert isinstance(combined, pd.DataFrame)
    assert len(combined) == len(df_reviews)            # left join keeps all reviews
    assert os.path.exists("data/processed/reviews_products.processed.csv")
