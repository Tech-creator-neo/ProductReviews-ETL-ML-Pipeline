from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data

def main():
    df_reviews, products_df = extract_data()
    combined_df = transform_data(df_reviews, products_df)
    load_data()  # publishes processed dataset
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
