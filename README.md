![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
[![Streamlit App](https://img.shields.io/badge/demo-streamlit-orange)](https://appuctreviews-etl-ml-pipeline-c9xhmmsg4aibwtrgxhlksr.streamlit.app/)

# Retail ETL & ML Data Pipeline

This project implements an end-to-end ETL data pipeline for a retail analytics scenario. It combines product, sales, and customer review data into a curated, analysis-ready dataset that can be used to power dashboards and machine learning models.

Starting from a prototype in a Jupyter notebook, the logic is refactored into a production-like repository structure with separate modules for extraction, transformation, and loading (extract.py, transform.py, load.py) orchestrated by a single pipeline controller script (data_pipeline.py). The pipeline automates the flow of data from multiple sources, cleans and standardises it, merges everything into a single dataset, and then publishes the processed output to a version-controlled repository.

On top of this ETL backbone, the project includes an SST-2 sentiment analysis model to predict the sentiment of customer product reviews. The predicted sentiment is merged into the curated dataset, enabling richer analytics and powering a lightweight dashboard to explore how customer sentiment correlates with product price, category, and ratings.

You can try the live version of the Retail ETL and Sentiment Analysis App here: [Open App](https://appuctreviews-etl-ml-pipeline-c9xhmmsg4aibwtrgxhlksr.streamlit.app/)

### What this project demonstrates

- **Data engineering**. Building an automated ETL pipeline across multiple data sources (products, sales, reviews) with clear extract/transform/load stages.
- **ML & NLP**. Integrating an SST-2 sentiment model into the pipeline to enrich customer review data.
- **Production practices**. Modular Python package structure, configuration-driven pipeline, logging, and basic test coverage.
- **Analytics & dashboards**. Interactive Streamlit app for exploring sentiment vs. price, category, and ratings.

## Sentiment Model

- Base model: `distilbert` fine-tuned on SST-2
