import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import os

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

data = pd.read_csv("data/movies_data.csv")

# Drop any rows with missing values in critical columns
data.dropna(subset=['reviews', 'original_title', 'overview', 'genres', 'cast', 'keywords', 'director'], inplace=True)

# Check and drop duplicates 
data.drop_duplicates(subset=['reviews'], inplace=True)

# Text Cleaning Funcion
def clean_text(text):
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize the text
    words = nltk.word_tokenize(text)
    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]
    # Join words back to a single string
    cleaned_text = ' '.join(words)
    return cleaned_text

# Apply the text cleaning function to relevant text columns
for col in ['reviews', 'overview', 'genres', 'cast', 'keywords', 'director']:
    data[col] = data[col].astype(str).apply(clean_text)

# Combine text features to form a single 'content' column for recommendations
data['content'] = data['overview'] + ' ' + data['genres'] + ' ' + data['cast'] + ' ' + data['keywords'] + ' ' + data['director']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data['reviews'], data['original_title'], test_size=0.2, random_state=42)

# Vectorize the text data in 'review' and 'content' columns using TF-IDF
tfidf_review = TfidfVectorizer(max_features=5000)
X_train_tfidf_review = tfidf_review.fit_transform(X_train)
X_test_tfidf_review = tfidf_review.transform(X_test)

tfidf_content = TfidfVectorizer(max_features=5000)
X_content_tfidf = tfidf_content.fit_transform(data['content'])

print("Training review data shape:", X_train_tfidf_review.shape)
print("Test review data shape:", X_test_tfidf_review.shape)
print("Content data shape:", X_content_tfidf.shape)

# Save cleaned data to 'data' folder
cleaned_csv_file_path = os.path.join("data", "cleaned_movie_data.csv")
data.to_csv(cleaned_csv_file_path, index=False)
print(f"Cleaned data saved to {cleaned_csv_file_path}")