# 🎬 Movie Recommendation System

Welcome to the **Movie Recommendation System**! This project leverages Machine Learning and TMDB API to provide personalized movie recommendations based on user preferences as well as provides a sentiment score for each recommended movie. 

---

## 🌟 Objective

The primary goal of this project is to create a movie recommendation engine that suggests movies to users based on their search queries and preferences.

---

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: TMDB (The Movie Database) API
- **Machine Learning**: TF-IDF Vectorization, Cosine Similarity
- **Natural Language Processing**: NLTK (Sentiment Analysis)
- **Data**: Scraped from TMDB using the API

---

## ⚙️ Features

1. **Movie Search Suggestions**: Autocomplete functionality when typing a movie name.
2. **Personalized Recommendations**: Get top movie recommendations based on your search.
3. **TMDB Integration**: View additional movie details like cast, director, runtime, etc.
4. **Sentiment Analysis**: Analyze the sentiment of movie reviews.

---

## Want to try it out?

### Prerequisites
Make sure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Follow these steps to set up the project on your local machine:
1. **Clone the Repository**:
```bash
git clone https://github.com/parth-16/movie-recommendation-system.git
cd Movie_Recommendation_System
```
2. **Set Up a Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```
3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```
4. Set Up Environment Variables
Create a .env file in the root directory with the following content:
```bash
TMDB_API_KEY=your_tmdb_api_key
TMDB_ACCESS_TOKEN=your_tmdb_access_token
```
  Replace your_tmdb_api_key and your_tmdb_access_token with your actual TMDB API credentials.

5. Run the Application
Start the Flask development server:
```bash
python app.py
```

6. Access the Application
Open your browser and navigate to the link

7. Using the Application
1. Enter a movie name in the search bar and click on "Find Recommendations" to see similar movies.
2. Suggestions will appear as you type, making it easier to select a movie.

## Notes
1. Ensure your .env file is correctly set up before running the application.
2. If using Docker or deploying to a cloud service, additional steps may be required.

## 🛠️ Future Enhancements
1. Add user authentication for personalized experiences.
2. Enhance the recommendation model using collaborative filtering.
3. Allow users to rate and review movies directly on the platform.

## 🤝 Contributing
Contributions are welcome! Feel free to submit issues and pull requests to improve the project.

## 📄 License
This project is licensed under the MIT License.

## 🌐 Contact
Developer: Parth Batavia

Email: bataviaparth16@gmail.com

LinkedIn: https://www.linkedin.com/in/parth-batavia-363baa1b4/

