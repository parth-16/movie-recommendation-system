import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

nltk.download('vader_lexicon')

data = pd.read_csv("data/cleaned_movie_data.csv")

sid = SentimentIntensityAnalyzer()

# Ensure all values in 'review' column are strings, filling NaNs with an empty string
data['reviews'] = data['reviews'].fillna('').astype(str)

# Categorize sentiment based on compound score
def get_sentiment_label(score):
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def convert_to_percentage(score):
    return int((score + 1) * 50)  

# Calculate sentiment scores for each review
data['sentiment_score_raw'] = data['reviews'].apply(lambda review: sid.polarity_scores(review)['compound'])
data['sentiment_score'] = data['sentiment_score_raw'].apply(convert_to_percentage)
data['sentiment'] = data['sentiment_score_raw'].apply(get_sentiment_label)

sentiment_csv_file_path = os.path.join("data", "movie_data_with_sentiment.csv")
data.to_csv(sentiment_csv_file_path, index=False)
print(f"Sentiment-analyzed data saved to {sentiment_csv_file_path}")

data['sentiment_score'] = data['sentiment_score'].apply(lambda x: f"{x}/100")
print(data[['original_title', 'reviews', 'sentiment', 'sentiment_score']].head())