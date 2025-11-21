"""
Integration test for scripts/extract.py that uses real inputs:
- Reads the actual JSONL at data/raw/product_reviews_sales.jsonl
- Calls the real FakeStore API (https://fakestoreapi.com/products)

This test intentionally avoids mocks and synthetic data.
"""

import pytest
import pandas as pd
from scripts.extract import extract_data

from scripts.extract import extract_data


def test_extract_runs():
    """Check that extract_data() runs successfully without throwing errors."""
    extract_data()