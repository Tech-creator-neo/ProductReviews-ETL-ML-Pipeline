import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="🛍️ Product Reviews Insights", layout="wide")

st.title("🛍️ Product Reviews Insights: Sentiment, Ratings & Sales")
st.markdown(
    "<p style='font-size:18px; color:gray;'>Mini dashboard powered by ETL data pipeline and DistilBERT sentiment model</p>",
    unsafe_allow_html=True
)

# 1) LOAD DATA
BASE_DIR = Path(__file__).resolve().parent
LOCAL_CSV = (BASE_DIR / "../data/processed/reviews_products_with_sentiment.csv").resolve()

@st.cache_data
def load_data() -> pd.DataFrame:
    if not LOCAL_CSV.exists():
        st.error(f"CSV not found at: {LOCAL_CSV.resolve()}")
        st.stop()
    return pd.read_csv(LOCAL_CSV)

df = load_data()

st.divider()

#SIDEBAR FILTERS
df_f = df.copy()

st.sidebar.header("Filters")

# Sentiment filter
sentiments = sorted(df_f["sentiment"].dropna().unique()) if "sentiment" in df_f else []
selected_sentiments = st.sidebar.multiselect("Sentiment", sentiments, default=sentiments)

# Category filter
cats = sorted(df_f["category"].dropna().unique()) if "category" in df_f else []
selected_cats = st.sidebar.multiselect("Category", cats, default=cats)

# Price range filter
if "price" in df_f:
    min_price = float(df_f["price"].min())
    max_price = float(df_f["price"].max())
    price_range = st.sidebar.slider("Price range", min_price, max_price, (min_price, max_price))
else:
    price_range = None

#APPLY FILTERS
if selected_sentiments:
    df_f = df_f[df_f["sentiment"].isin(selected_sentiments)]

if selected_cats:
    df_f = df_f[df_f["category"].isin(selected_cats)]

if price_range is not None and "price" in df_f:
    lo, hi = price_range
    df_f = df_f[(df_f["price"] >= lo) & (df_f["price"] <= hi)]

# Optional: show message if nothing matches
if df_f.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# 2) KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Reviews", f"{len(df_f):,}")
c2.metric("Products", f"{df_f['id'].nunique() if 'id' in df_f else df_f.shape[0]:,}")
c3.metric(
    "Positivity %",
    f"{(df_f['sentiment'].eq('POSITIVE').mean() * 100):.1f}%"
    if "sentiment" in df_f else "—"
)
c4.metric(
    "Avg confidence",
    f"{df_f['confidence'].mean():.2f}"
    if "confidence" in df_f else "—"
)

st.divider()

# 3) VISUALIZATION

# Sentiment distribution
fig1 = px.histogram(
    df_f,
    x="sentiment",
    color="sentiment",
    color_discrete_sequence=["#636EFA", "#EF553B"],
    title="Sentiment Distribution"
)
fig1.update_layout(yaxis_title="Number of Customer Responses")
st.plotly_chart(fig1, use_container_width=True)

# Model confidence by sentiment
if "confidence" in df_f and "sentiment" in df_f:
    avg_conf = df_f.groupby("sentiment", as_index=False)["confidence"].mean()
    fig2 = px.bar(
        avg_conf,
        x="sentiment",
        y="confidence",
        color="sentiment",
        title="Model Confidence by Sentiment",
        color_discrete_sequence=["#EF553B", "#636EFA"]
    )
    fig2.update_layout(yaxis_title="Average Model Confidence")
    st.plotly_chart(fig2, use_container_width=True)

# Sentiment by category
if "category" in df_f and "sentiment" in df_f:
    sent_by_cat = df_f.groupby(["category", "sentiment"]).size().reset_index(name="count")
    fig3 = px.bar(
        sent_by_cat,
        x="category",
        y="count",
        color="sentiment",
        title="Customer Sentiment by Product Category",
        barmode="group",
        color_discrete_sequence=["#EF553B", "#636EFA"]
    )
    fig3.update_layout(
        yaxis_title="Number of Customer Responses",
        xaxis_title="Product Category"
    )
    st.plotly_chart(fig3, use_container_width=True)

# 4) DATA PREVIEW (FILTERED)
st.subheader("Sample of Filtered Data")
st.dataframe(df_f.head(100), use_container_width=True)
