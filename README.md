📝 Project Overview
The process_review.py script is a dedicated tool for performing detailed sentiment analysis on e-commerce product review data from both Amazon and Flipkart. The core objective is to transform raw, unstructured customer feedback into quantified sentiment metrics and compelling visualizations. It is built using Python, leveraging TextBlob for sentiment scoring, and Matplotlib/WordCloud for generating graphic reports.

This analysis is crucial for quickly identifying popular products, understanding areas of customer delight (Positive sentiment), and pinpointing critical issues (Negative sentiment) across various product lines.

✨ Core Functionality
The script executes a multi-step analytical pipeline:

Data Ingestion and Sampling: It reads raw CSV files from specified directories (data/raw/amazon/ and data/raw/flipkart/) and optionally samples the data (e.g., 10,000 Amazon reviews and 5,000 Flipkart reviews) for faster processing and analysis.

Text Cleaning: Review text is rigorously cleaned. This involves standardizing the text by converting it to lowercase, removing all URLs, and stripping out special characters and excessive whitespace.

Sentiment Labeling: Using TextBlob's polarity score, each cleaned review is classified as Positive, Neutral, or Negative.

Product Summary Generation: The script groups reviews by product ID (or name) to calculate the total counts and percentages of Positive, Neutral, and Negative reviews for every unique product.

Ranking Reports: It generates specialized reports identifying the Top 5 Best products (highest positive percentage), Top 5 Worst products (highest negative percentage), and Top 5 Most Reviewed products for each platform.

⚙️ Setup and Execution
To run this analysis, you must first install the required Python libraries: pandas, numpy, matplotlib, textblob, and wordcloud.

The script requires a specific directory structure to locate the input files. All raw data must be placed inside the data/raw/ directory, separated by platform (amazon/Reviews.csv and flipkart/Dataset-SA.csv).

Once the environment is set up and the data is correctly positioned, simply execute the script from your terminal:

Bash

python process_review.py
The script will automatically create the output folders and generate the results.

📂 Understanding the Results
The final output is organized into two main locations:

1. Processed Data (data/processed/)
This directory holds the intermediate data products. You will find platform-specific CSV files (e.g., amazon_processed.csv) which contain the original reviews enriched with the new cleaned_review and sentiment columns. Additionally, comprehensive summary files (e.g., amazon_product_summary.csv) are created, detailing the complete sentiment breakdown for every single product analyzed.

2. Final Output Reports (output/)
This directory contains the primary deliverables of the analysis:

Ranking Tables: Separate CSV files are generated for each platform highlighting the top 5 products across the Best, Worst, and Most Reviewed categories. These provide quick, quantifiable insights into product performance.

Sentiment Bar Charts: A high-level visualization is created for each platform (e.g., amazon_sentiment_bar.png). These stacked bar charts illustrate the breakdown of positive and negative review counts for the top 10 most-reviewed products, allowing for easy comparison.

Product-Specific Word Clouds: For the top 5 most-reviewed products, two distinct word clouds are generated per product: one for the Positive reviews and one for the Negative reviews. These images provide an immediate visual grasp of the most frequently used words associated with either satisfaction or dissatisfaction for key products.
