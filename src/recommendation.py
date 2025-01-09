import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
access_token = os.getenv("TMDB_ACCESS_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

url_movie_details = "https://api.themoviedb.org/3/movie/{movie_id}"
url_movie_search = "https://api.themoviedb.org/3/search/movie"

def search_movie_by_title(title):
    """
    Search for a movie by its title using the TMDB API.
    """
    params = {
        "query": title,
        "language": "en-US",
    }
    response = requests.get(url_movie_search, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]  # Return the first result
    return None

def get_movie_details(movie_id):
    """
    Fetch detailed information about a movie by its ID.
    """
    url = url_movie_details.format(movie_id=movie_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_movie_cast(movie_id):
    """
    Fetch the top 5 cast members for a movie.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        cast = response.json().get("cast", [])
        return ", ".join([member["name"] for member in cast[:5]])  # Top 5 cast
    return "N/A"

def fetch_movie_director(movie_id):
    """
    Fetch the director of a movie.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        crew = response.json().get("crew", [])
        director = next((member["name"] for member in crew if member["job"] == "Director"), "N/A")
        return director
    return "N/A"

def generate_recommendations(recommendations):
    """
    Generate recommendations with dynamically fetched details.
    """
    enriched_recommendations = []
    for title in recommendations:
        movie_data = search_movie_by_title(title)
        if movie_data:
            details = get_movie_details(movie_data["id"])
            if details:
                enriched_recommendations.append({
                    "title": details.get("title", "N/A"),
                    "genres": ", ".join([genre["name"] for genre in details.get("genres", [])]),
                    "overview": details.get("overview", "N/A").capitalize(),
                    "cast": fetch_movie_cast(movie_data["id"]),
                    "director": fetch_movie_director(movie_data["id"]),
                    "release_date": details.get("release_date", "N/A"),
                    "runtime": f"{details.get('runtime', 'N/A')} minutes",
                    "language": details.get("original_language", "N/A").upper(),
                    "tmdb_link": f"https://www.themoviedb.org/movie/{movie_data['id']}"
                })
            else:
                enriched_recommendations.append(generate_empty_data(title))
        else:
            enriched_recommendations.append(generate_empty_data(title))
    return enriched_recommendations

def generate_empty_data(title):
    """
    Generate empty data placeholders for movies not found.
    """
    return {
        "title": title,
        "genres": "N/A",
        "overview": "N/A",
        "cast": "N/A",
        "director": "N/A",
        "release_date": "N/A",
        "runtime": "N/A",
        "language": "N/A",
        "tmdb_link": "https://www.themoviedb.org/"
    }

# Example Recommendations
recommended_movies = ["The Godfather Part II", "Goodfellas"]

# Generate Recommendations
recommendations = generate_recommendations(recommended_movies)

# Display Results
for rec in recommendations:
    print(f"Title: {rec['title']} (Link: {rec['tmdb_link']})")
    print(f"Genres: {rec['genres']}")
    print(f"Overview: {rec['overview']}")
    print(f"Cast: {rec['cast']}")
    print(f"Director: {rec['director']}")
    print(f"Release Date: {rec['release_date']}")
    print(f"Runtime: {rec['runtime']}")
    print(f"Language: {rec['language']}")
    print()