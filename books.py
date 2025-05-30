import os
import pandas as pd
import pickle

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load books dataset
books_file = os.path.join(current_dir, "book.csv")

# Check if the file exists
if not os.path.exists(books_file):
    print(f"❌ Error: The file '{books_file}' does not exist.")
    exit()

# Load the dataset
books_df = pd.read_csv(books_file, low_memory=False)

# Ensure 'Image-URL-L' is included
if "Image-URL-L" not in books_df.columns:
    print("❌ Error: 'Image-URL-L' column is missing in books_dataset.csv")
    exit()

# Select important columns (including images)
books_df = books_df[['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]

# Save as `books.pkl`
with open(os.path.join(current_dir, "books.pkl"), "wb") as f:
    pickle.dump(books_df, f)

print(f"✅ books.pkl created successfully with {len(books_df)} books!")