import requests
import csv
from dotenv import load_dotenv
import os

url_top_rated = "https://api.themoviedb.org/3/movie/top_rated"
url_movie_details = "https://api.themoviedb.org/3/movie/{movie_id}"
url_movie_credits = "https://api.themoviedb.org/3/movie/{movie_id}/credits"
url_movie_keywords = "https://api.themoviedb.org/3/movie/{movie_id}/keywords"
url_movie_reviews = "https://api.themoviedb.org/3/movie/{movie_id}/reviews"  

# Load environment variables
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
access_token = os.getenv("TMDB_ACCESS_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Fetch top-rated movies
def get_top_rated_movies(page):
    params = {
        "language": "en-US",
        "page": page
    }
    response = requests.get(url_top_rated, headers=headers, params=params)
    return response.json()

# Fetch movie details
def get_movie_details(movie_id):
    url = url_movie_details.format(movie_id=movie_id)
    response = requests.get(url, headers=headers)
    return response.json()

# Fetch movie credits
def get_movie_credits(movie_id):
    url = url_movie_credits.format(movie_id=movie_id)
    response = requests.get(url, headers=headers)
    return response.json()

# Fetch movie keywords
def get_movie_keywords(movie_id):
    url = url_movie_keywords.format(movie_id=movie_id)
    response = requests.get(url, headers=headers)
    return response.json()

# Fetch movie reviews
def get_movie_reviews(movie_id):
    url = url_movie_reviews.format(movie_id=movie_id)
    response = requests.get(url, headers=headers)
    return response.json()

total_pages = 10

movies_data = []

for page_number in range(1, total_pages + 1):
    top_rated_movies = get_top_rated_movies(page_number)["results"]
    
    for movie in top_rated_movies:
        details = get_movie_details(movie["id"])
        credits = get_movie_credits(movie["id"])
        keywords = get_movie_keywords(movie["id"])
        reviews = get_movie_reviews(movie["id"]) 
        
        # Extract director name
        director_name = next((crew["name"] for crew in credits.get("crew", []) if crew.get("job") == "Director"), "")
        
        # Extract review details
        review_contents = [review["content"] for review in reviews.get("results", [])]
        
        # Combine data
        movie_data = {
            "id": movie["id"],
            "original_title": movie["original_title"],
            "overview": movie["overview"],
            "popularity": movie["popularity"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "genres": [genre["name"] for genre in details.get("genres", [])],
            "cast": [cast["name"] for cast in credits.get("cast", [])],
            "director": director_name,
            "keywords": [keyword["name"] for keyword in keywords.get("keywords", [])],
            "reviews": review_contents  # Add reviews to the movie data
        }
        
        movies_data.append(movie_data)

csv_file_path = os.path.join("data", "movies_data.csv") 
fields = ["id", "original_title", "overview", "popularity", "release_date", "vote_average", "genres", "cast", "director", "keywords", "reviews"]

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    
    writer.writeheader()
    
    for movie in movies_data:
        writer.writerow({field: movie.get(field, "") for field in fields})

print(f"Movies data saved to {csv_file_path}")