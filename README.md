# Customer_feedback_analysis
📝 Overview
This repository contains a Python script, process_review.py, designed to perform a comprehensive, product-wise sentiment analysis on e-commerce review datasets (specifically Amazon and Flipkart). The project aims to automatically process raw customer feedback, quantify sentiment, and generate clear, actionable reports and visualizations to identify product strengths and weaknesses.

The analysis is powered by TextBlob for sentiment scoring and Matplotlib/WordCloud for generating insightful graphics.

✨ Key Features
Dual Platform Analysis: Supports concurrent analysis of Amazon (Reviews.csv) and Flipkart (Dataset-SA.csv) data structures.

Robust Text Cleaning: Implements a cleaning function to normalize text (lowercase, removal of URLs, special characters).

Sentiment Classification: Labels each review as Positive, Neutral, or Negative based on TextBlob's polarity score.

Product Summaries: Creates detailed CSV files summarizing sentiment distribution for every analyzed product.

Top 5 Product Rankings: Automatically generates CSV reports for:

🏆 Best Products (Highest % Positive Sentiment)

❌ Worst Products (Highest % Negative Sentiment)

📈 Most Reviewed Products (Highest Volume)

Data Visualization: Generates stacked bar charts and product-specific word clouds (Positive and Negative reviews) to visualize results.

⚙️ Project Structure & Setup
1. Requirements
The script is written in Python and requires the following libraries.
pip install pandas numpy matplotlib textblob wordcloud.
Data Structure
The script is configured to look for raw data in the following directory structure. Please ensure your CSV files are named correctly and placed in the appropriate folders:
├── data/
│   ├── raw/
│   │   ├── amazon/
│   │   │   └── Reviews.csv
│   │   └── flipkart/
│   │       └── Dataset-SA.csv
├── process_review.py
└── README.md
3. Execution
Execute the analysis script from the root directory:

Bash

python process_review.py
The script will automatically create the data/processed/ and output/ directories if they do not exist.

📂 Outputs & Results
All final reports and visualizations are stored in the output/ directory, while intermediate summary files are placed in data/processed/.
A. Processed Data (Internal)
File Name,Description
<platform>_processed.csv,Raw data with added columns for cleaned_review and sentiment.
<platform>_product_summary.csv,"A master table showing Positive, Negative, Neutral counts, total reviews, and sentiment percentages for all products."
B. Final Reports (output/)
1. Ranking CSVs (Top 5)
These files provide the data for the best, worst, and most-reviewed products for each platform:

amazon_top5_best.csv

flipkart_top5_worst.csv

...and other ranking files.

2. Visualizations
Stacked Bar Charts: (<platform>_sentiment_bar.png)

Visual representation of the sentiment breakdown for the top 10 most-reviewed products.

Product-Specific Word Clouds: (<platform>_<product_id>_positive_wc.png / _negative_wc.png)

Generates word clouds for the top 5 most-reviewed products, separately for their Positive and Negative reviews, providing quick insights into common keywords.
🛠️ Configuration Details
The script includes a CONFIG section for easy modification of parameters:
Variable,Description,Default Value
SAMPLE_AMAZON,Max number of reviews to sample from Amazon.,10000
SAMPLE_FLIPKART,Max number of reviews to sample from Flipkart.,5000
TOP_N_PRODUCTS,Number of products to show in the bar chart.,10
TOP_K_WORDCLOUDS,Number of products for which to generate word clouds.,5
