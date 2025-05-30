import pandas as pd
import pickle
import os

# Define the correct path for your dataset
DATA_PATH = r"E:\book-recommender-system-master\book-recommender-system-master\book.csv"

# Load the book dataset
try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Book dataset loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: book.csv not found at {DATA_PATH}")
    exit()

# Ensure required columns exist
required_columns = ["Book-Title", "num_ratings", "avg_rating", "Image-URL-L"]
for col in required_columns:
    if col not in df.columns:
        print(f"❌ Error: Missing '{col}' in book.csv. Please check your dataset.")
        exit()

# Convert 'num_ratings' to integer and 'avg_rating' to float (handling missing values)
df["num_ratings"] = df["num_ratings"].fillna(0).astype(int)
df["avg_rating"] = df["avg_rating"].fillna(0.0).astype(float)

# Sort books by highest number of ratings and include images
# Replace missing or invalid image URLs with a placeholder
df["Image-URL-L"] = df["Image-URL-L"].fillna("https://via.placeholder.com/150")
df["Image-URL-L"] = df["Image-URL-L"].apply(lambda x: x if x.startswith("http") else "https://via.placeholder.com/150")

# Select top 50 books
popular_books = df.sort_values(by="num_ratings", ascending=False).head(50)


# Save to 'popular.pkl'
with open("popular.pkl", "wb") as f:
    pickle.dump(popular_books, f)

print("✅ popular.pkl has been generated successfully!")
