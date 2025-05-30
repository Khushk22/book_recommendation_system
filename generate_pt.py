import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define the correct absolute path for book.csv
base_dir = "E:\\book-recommender-system-master\\book-recommender-system-master"
file_path = os.path.join(base_dir, "book.csv")

try:
    # Load dataset
    df_books = pd.read_csv(file_path)

    # Ensure necessary columns
    required_columns = {"Book-Title", "Category", "Image-URL-L"}
    if not required_columns.issubset(df_books.columns):
        raise ValueError(f"❌ Error: Dataset must contain columns: {required_columns}! Found: {df_books.columns.tolist()}")

    # Use only first 5000 books (modify as needed)
    df_books = df_books.head(5000)

    # Fill missing values
    df_books["Category"].fillna("Unknown", inplace=True)
    df_books["Book-Title"].fillna("Unknown", inplace=True)
    df_books["Image-URL-L"].fillna("https://via.placeholder.com/150", inplace=True)

    # Text feature extraction using TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df_books["Book-Title"])

    # Compute similarity
    similarity_scores = cosine_similarity(tfidf_matrix)

    # Convert to DataFrame and set index to Book-Title
    pt = pd.DataFrame(similarity_scores, index=df_books["Book-Title"], columns=df_books["Book-Title"])

    # Save `pt.pkl`
    pt_path = os.path.join(base_dir, "pt.pkl")
    with open(pt_path, "wb") as f:
        pickle.dump(pt, f)

    print(f"✅ Successfully generated and saved `pt.pkl` at {pt_path} as a Pandas DataFrame!")

except FileNotFoundError:
    print(f"❌ Error: The file '{file_path}' was not found! Please check the file path.")
except Exception as e:
    print(f"❌ Error: {e}")
