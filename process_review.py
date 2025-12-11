"""
Enhanced Product-wise Sentiment Analysis
----------------------------------------
✔ Product-wise sentiment (Positive / Neutral / Negative)
✔ Top 5: Best, Worst, Most Reviewed
✔ Bar charts using product NAMES
✔ Word clouds WITH product name in image
✔ Summary CSVs
"""

import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud

# --------------------------------------------------------
# CONFIG
# --------------------------------------------------------
RAW_AMAZON = "data/raw/amazon/Reviews.csv"
RAW_FLIPKART = "data/raw/flipkart/Dataset-SA.csv"

PROCESSED_DIR = "data/processed"
OUTPUT_DIR = "output"

SAMPLE_AMAZON = 10000
SAMPLE_FLIPKART = 5000
TOP_N_PRODUCTS = 10
TOP_K_WORDCLOUDS = 5

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --------------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------------
def clean_text(s):
    if pd.isnull(s):
        return ""
    s = str(s).lower()
    s = re.sub(r"http\S+|www\S+|https\S+", " ", s)
    s = re.sub(r"[^a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# --------------------------------------------------------
# SENTIMENT LABEL
# --------------------------------------------------------
def sentiment_label(text):
    if not text or text.strip() == "":
        return "Neutral"
    score = TextBlob(text).sentiment.polarity
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    return "Neutral"


# --------------------------------------------------------
# SAFE COLUMN PICKER
# --------------------------------------------------------
def safe_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


# --------------------------------------------------------
# LOAD & SAMPLE
# --------------------------------------------------------
amazon_df = pd.read_csv(RAW_AMAZON, low_memory=False)
flipkart_df = pd.read_csv(RAW_FLIPKART, low_memory=False)

if SAMPLE_AMAZON:
    amazon_df = amazon_df.sample(n=min(SAMPLE_AMAZON, len(amazon_df)), random_state=42)
if SAMPLE_FLIPKART:
    flipkart_df = flipkart_df.sample(n=min(SAMPLE_FLIPKART, len(flipkart_df)), random_state=42)

amazon_text = safe_col(amazon_df, ["Text", "Review", "reviewText"])
amazon_pid = safe_col(amazon_df, ["ProductId", "ASIN"])

flip_text = safe_col(flipkart_df, ["Review", "review", "text"])
flip_pid = safe_col(flipkart_df, ["product_name", "title", "Product"])


# --------------------------------------------------------
# ADD CLEANED TEXT & SENTIMENT
# --------------------------------------------------------
amazon_df["cleaned_review"] = amazon_df[amazon_text].apply(clean_text)
flipkart_df["cleaned_review"] = flipkart_df[flip_text].apply(clean_text)

amazon_df["sentiment"] = amazon_df["cleaned_review"].apply(sentiment_label)
flipkart_df["sentiment"] = flipkart_df["cleaned_review"].apply(sentiment_label)

amazon_df.to_csv(f"{PROCESSED_DIR}/amazon_processed.csv", index=False)
flipkart_df.to_csv(f"{PROCESSED_DIR}/flipkart_processed.csv", index=False)


# --------------------------------------------------------
# PRODUCT-WISE SUMMARY
# --------------------------------------------------------
def product_summary(df, pid_col, platform):
    summary = df.groupby(pid_col)["sentiment"].value_counts().unstack(fill_value=0)
    for c in ["Positive", "Neutral", "Negative"]:
        if c not in summary.columns:
            summary[c] = 0

    summary["total_reviews"] = summary.sum(axis=1)
    summary["pct_positive"] = summary["Positive"] / summary["total_reviews"] * 100
    summary["pct_negative"] = summary["Negative"] / summary["total_reviews"] * 100

    summary = summary.reset_index().rename(columns={pid_col: "product_name"})
    summary = summary.sort_values("total_reviews", ascending=False)

    summary.to_csv(f"{PROCESSED_DIR}/{platform}_product_summary.csv", index=False)
    return summary


amazon_summary = product_summary(amazon_df, amazon_pid, "amazon")
flipkart_summary = product_summary(flipkart_df, flip_pid, "flipkart")


# --------------------------------------------------------
# CREATE RANKING TABLES
# --------------------------------------------------------
def ranking_tables(summary, platform):
    best = summary.sort_values("pct_positive", ascending=False).head(5)
    worst = summary.sort_values("pct_negative", ascending=False).head(5)
    most = summary.sort_values("total_reviews", ascending=False).head(5)

    best.to_csv(f"{OUTPUT_DIR}/{platform}_top5_best.csv", index=False)
    worst.to_csv(f"{OUTPUT_DIR}/{platform}_top5_worst.csv", index=False)
    most.to_csv(f"{OUTPUT_DIR}/{platform}_top5_most_reviewed.csv", index=False)


ranking_tables(amazon_summary, "amazon")
ranking_tables(flipkart_summary, "flipkart")


# --------------------------------------------------------
# BAR CHARTS (USING PRODUCT NAMES)
# --------------------------------------------------------
def plot_sentiment_bars(summary, platform, top_n=10):
    top = summary.head(top_n)

    plt.figure(figsize=(12, 6))
    plt.barh(top["product_name"], top["Positive"], label="Positive")
    plt.barh(top["product_name"], top["Negative"], left=top["Positive"], label="Negative")
    plt.title(f"{platform.upper()} — Sentiment Distribution (Top {top_n})")
    plt.xlabel("Counts")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{platform}_sentiment_bar.png")
    plt.close()


plot_sentiment_bars(amazon_summary, "amazon")
plot_sentiment_bars(flipkart_summary, "flipkart")


# --------------------------------------------------------
# WORD CLOUDS WITH PRODUCT NAME
# --------------------------------------------------------
def product_text(df, pid_col, pid_value, sentiment_type):
    mask = (df[pid_col] == pid_value) & (df["sentiment"] == sentiment_type)
    return " ".join(df.loc[mask, "cleaned_review"].astype(str))


def make_cloud(text, filename, title):
    if not text.strip():
        return

    wc = WordCloud(width=1000, height=500, background_color="white").generate(text)
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.title(title, fontsize=18)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def wordclouds(summary, df, pid_col, platform):
    top_products = summary["product_name"].head(TOP_K_WORDCLOUDS)

    for product in top_products:
        pos_text = product_text(df, pid_col, product, "Positive")
        neg_text = product_text(df, pid_col, product, "Negative")

        make_cloud(pos_text,
                   f"{OUTPUT_DIR}/{platform}_{product}_positive_wc.png",
                   f"{product} — Positive Reviews")

        make_cloud(neg_text,
                   f"{OUTPUT_DIR}/{platform}_{product}_negative_wc.png",
                   f"{product} — Negative Reviews")


wordclouds(amazon_summary, amazon_df, amazon_pid, "amazon")
wordclouds(flipkart_summary, flipkart_df, flip_pid, "flipkart")

print("All outputs created successfully.")
