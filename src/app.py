from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
access_token = os.getenv("TMDB_ACCESS_TOKEN")
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Load preprocessed data
data = pd.read_csv("data/movie_data_with_sentiment.csv")

# Load TF-IDF vectorizer for recommendations
tfidf_content = TfidfVectorizer(max_features=5000)
content_tfidf_matrix = tfidf_content.fit_transform(data['content'])
cosine_sim = cosine_similarity(content_tfidf_matrix, content_tfidf_matrix)

# Sentiment Analyzer
sid = SentimentIntensityAnalyzer()

# TMDB API Calls
def fetch_tmdb_data(movie_title):
    """Fetch movie details, cast, and director from TMDB API."""
    search_url = f"https://api.themoviedb.org/3/search/movie"
    params = {"query": movie_title, "language": "en-US", "page": 1}
    response = requests.get(search_url, headers=headers, params=params).json()
    
    if "results" not in response or len(response["results"]) == 0:
        return None  # Movie not found
    
    movie_data = response["results"][0]  # Take the first result
    movie_id = movie_data["id"]
    
    # Fetch movie details
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    details = requests.get(details_url, headers=headers).json()

    # Fetch movie credits
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    credits = requests.get(credits_url, headers=headers).json()

    # Extract director and cast
    director = next((crew["name"] for crew in credits.get("crew", []) if crew["job"] == "Director"), "N/A")
    cast = [member["name"] for member in credits.get("cast", [])[:5]]  # Top 5 cast members
    
    # Prepare the data
    movie_details = {
        "tmdb_link": f"https://www.themoviedb.org/movie/{movie_id}",
        "release_date": details.get("release_date", "N/A"),
        "runtime": details.get("runtime", "N/A"),
        "language": details.get("original_language", "N/A").upper(),
        "cast": ", ".join(cast) if cast else "N/A",
        "director": director,
    }
    
    return movie_details

# Recommendation function
def get_recommendations(title, data, cosine_sim):
    title = title.lower()
    if title not in data['original_title'].str.lower().values:
        return None

    idx = data[data['original_title'].str.lower() == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_indices = [i[0] for i in sim_scores[1:11]]  # Top 10 recommendations
    recommendations = data.iloc[sim_indices][['original_title', 'overview', 'genres', 'sentiment', 'sentiment_score']]
    
    # Enrich recommendations with TMDB data
    enriched_recommendations = []
    for _, row in recommendations.iterrows():
        tmdb_data = fetch_tmdb_data(row['original_title'])
        enriched_recommendations.append({
            "title": row['original_title'],
            "overview": row['overview'].capitalize(),
            "genres": row['genres'],
            "sentiment": row['sentiment'],
            "sentiment_score": row['sentiment_score'],
            "tmdb_link": tmdb_data["tmdb_link"] if tmdb_data else "#",
            "cast": tmdb_data["cast"] if tmdb_data else "N/A",
            "director": tmdb_data["director"] if tmdb_data else "N/A",
            "release_date": tmdb_data["release_date"] if tmdb_data else "N/A",
            "runtime": f"{tmdb_data['runtime']} minutes" if tmdb_data and tmdb_data["runtime"] != "N/A" else "N/A",
            "language": tmdb_data["language"] if tmdb_data else "N/A",
        })
    
    return enriched_recommendations

# Home route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search-suggestions', methods=['GET'])
def search_suggestions():
    query = request.args.get('query', '').lower()
    matching_movies = data[data['original_title'].str.lower().str.contains(query)]
    return matching_movies['original_title'].head(10).to_json(orient='values')

# Results route
@app.route('/results', methods=['POST'])
def results():
    title = request.form['title']
    recommendations = get_recommendations(title, data, cosine_sim)

    if recommendations is None:
        return render_template('recommendations.html', error="Movie not found in dataset.", title=title)

    return render_template('recommendations.html', recommendations=recommendations, title=title)

if __name__ == '__main__':
    app.run(debug=True)