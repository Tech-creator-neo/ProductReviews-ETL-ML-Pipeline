import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# PAGE CONFIG
st.set_page_config(
    page_title="🛍️ Product Reviews Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GLOBAL STYLES
st.markdown(
    """
    <style>
      /* App background */
      .stApp {
        background: #F8FAFC;
      }

      /* Page title spacing */
      h1 {
        margin-bottom: 0.25rem;
      }

      /* Subtle caption */
      .caption {
        font-size: 0.95rem;
        color: #64748B;
        margin-top: -0.25rem;
        margin-bottom: 1.25rem;
      }

      /* Card container */
      .card {
        background: #FFFFFF;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 16px;
        padding: 18px 18px 10px 18px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.05);
        margin-bottom: 16px;
      }

      /* KPI card */
      .kpi {
        background: #FFFFFF;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.05);
      }
      .kpi-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
      }
      .kpi-title {
        font-size: 0.9rem;
        color: #64748B;
        font-weight: 600;
      }
      .kpi-icon {
        font-size: 1.1rem;
        opacity: 0.9;
      }
      .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
      }
      .kpi-sub {
        font-size: 0.85rem;
        color: #64748B;
        margin-top: 6px;
      }

      /* Insight callout */
      .insight {
        background: #EEF2FF;
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-left: 6px solid #6366F1;
        border-radius: 14px;
        padding: 14px 16px;
        color: #0F172A;
      }
      .insight strong {
        display: block;
        margin-bottom: 4px;
      }

      /* Sidebar polish */
      section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid rgba(15, 23, 42, 0.08);
      }
    </style>
    """,
    unsafe_allow_html=True
)

# HEADER
st.title("🛍️ Product Reviews Insights")
st.markdown(
    "<div class='caption'>Sentiment, ratings & sales overview powered by an ETL pipeline and a DistilBERT sentiment model</div>",
    unsafe_allow_html=True
)

# LOAD DATA
BASE_DIR = Path(__file__).resolve().parent
LOCAL_CSV = (BASE_DIR / "../data/processed/reviews_products_with_sentiment.csv").resolve()

@st.cache_data
def load_data() -> pd.DataFrame:
    if not LOCAL_CSV.exists():
        st.error(f"CSV not found at: {LOCAL_CSV.resolve()}")
        st.stop()
    return pd.read_csv(LOCAL_CSV)

df = load_data()
df_f = df.copy()

# SIDEBAR FILTERS
st.sidebar.markdown("## Filters")
st.sidebar.caption("Narrow the dataset to see how sentiment and confidence shift.")

sentiments = sorted(df_f["sentiment"].dropna().unique()) if "sentiment" in df_f else []
selected_sentiments = st.sidebar.multiselect(
    "Sentiment",
    sentiments,
    default=sentiments,
    help="Filter by model-predicted sentiment label."
)

cats = sorted(df_f["category"].dropna().unique()) if "category" in df_f else []
selected_cats = st.sidebar.multiselect(
    "Category",
    cats,
    default=cats,
    help="Filter products by category."
)

price_range = None
if "price" in df_f:
    min_price = float(df_f["price"].min())
    max_price = float(df_f["price"].max())
    price_range = st.sidebar.slider(
        "Price range",
        min_price,
        max_price,
        (min_price, max_price),
        help="Filter by product price."
    )

st.sidebar.divider()

# Apply filters
if selected_sentiments:
    df_f = df_f[df_f["sentiment"].isin(selected_sentiments)]

if selected_cats:
    df_f = df_f[df_f["category"].isin(selected_cats)]

if price_range is not None and "price" in df_f:
    lo, hi = price_range
    df_f = df_f[(df_f["price"] >= lo) & (df_f["price"] <= hi)]

if df_f.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# HELPERS
def polish_fig(fig, title=None):
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
        font=dict(size=13),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(15,23,42,0.08)", zeroline=False)
    return fig

# KPIS AND INSIGHT
reviews_n = len(df_f)
products_n = df_f["id"].nunique() if "id" in df_f else df_f.shape[0]
pos_pct = (df_f["sentiment"].eq("POSITIVE").mean() * 100) if "sentiment" in df_f else None
avg_conf = df_f["confidence"].mean() if "confidence" in df_f else None

overall_pos = (df["sentiment"].eq("POSITIVE").mean() * 100) if "sentiment" in df else None
pos_delta = (pos_pct - overall_pos) if (pos_pct is not None and overall_pos is not None) else None

k1, k2, k3, k4 = st.columns(4)

def kpi(col, icon, title, value, sub=None):
    col.markdown(
        f"""
        <div class="kpi">
          <div class="kpi-top">
            <div class="kpi-title">{title}</div>
            <div class="kpi-icon">{icon}</div>
          </div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub or "&nbsp;"}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

kpi(k1, "", "Reviews", f"{reviews_n:,}", "Filtered records")
kpi(k2, "", "Products", f"{products_n:,}", "Unique products")
kpi(k3, "", "Positivity", f"{pos_pct:.1f}%" if pos_pct is not None else "—",
    (f"{pos_delta:+.1f} pts vs overall" if pos_delta is not None else ""))
kpi(k4, "", "Average confidence", f"{avg_conf:.2f}" if avg_conf is not None else "—",
    "Model certainty")

# Insight callout
top_cat = None
if "category" in df_f:
    top_cat = df_f["category"].value_counts().idxmax()

insight_parts = []
if pos_pct is not None:
    insight_parts.append(f"Positivity is {pos_pct:.1f}% in the current slice.")
if avg_conf is not None:
    insight_parts.append(f"Average confidence is {avg_conf:.2f}.")
if top_cat is not None:
    insight_parts.append(f"The most represented category of product is: {top_cat}.")

st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="insight">
      <strong>💡 Quick insight</strong>
      {" ".join(insight_parts) if insight_parts else "Use filters to generate an insight for this slice."}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# VISUALS
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    fig1 = px.histogram(
        df_f,
        x="sentiment",
        color="sentiment",
        title="Sentiment Distribution",
        color_discrete_sequence=["#6366F1", "#EF4444"],  # indigo / red
    )
    fig1.update_layout(yaxis_title="Number of customer responses")
    st.plotly_chart(polish_fig(fig1, "Sentiment Distribution"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    if "confidence" in df_f and "sentiment" in df_f:
        avg_conf_df = df_f.groupby("sentiment", as_index=False)["confidence"].mean()
        fig2 = px.bar(
            avg_conf_df,
            x="sentiment",
            y="confidence",
            color="sentiment",
            title="Model Confidence by Sentiment",
            color_discrete_sequence=["#EF4444", "#6366F1"],
        )
        fig2.update_layout(yaxis_title="Average model confidence")
        st.plotly_chart(polish_fig(fig2, "Model Confidence by Sentiment"), use_container_width=True)
    else:
        st.info("Confidence/sentiment columns missing.")
    st.markdown("</div>", unsafe_allow_html=True)

if "category" in df_f and "sentiment" in df_f:
    sent_by_cat = df_f.groupby(["category", "sentiment"]).size().reset_index(name="count")
    fig3 = px.bar(
        sent_by_cat,
        x="category",
        y="count",
        color="sentiment",
        barmode="group",
        title="Customer Sentiment by Product Category",
        color_discrete_sequence=["#EF4444", "#6366F1"],
    )
    fig3.update_layout(
        yaxis_title="Number of customer responses",
        xaxis_title="Product category",
    )
    st.plotly_chart(polish_fig(fig3, "Customer Sentiment by Product Category"), use_container_width=True)
else:
    st.info("Category/sentiment columns missing.")
st.markdown("</div>", unsafe_allow_html=True)

# DATA PREVIEW
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Sample of Filtered Data")
st.caption("Showing the first 100 rows of the filtered dataset.")
st.dataframe(df_f.head(100), use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)
