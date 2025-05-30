from flask import Flask, render_template, request
import pickle
import os
import pandas as pd

app = Flask(__name__)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load necessary files safely
try:
    with open(os.path.join(current_dir, 'popular.pkl'), 'rb') as f:
        popular_df = pickle.load(f)

    with open(os.path.join(current_dir, 'books.pkl'), 'rb') as f:
        books = pickle.load(f)

    df_books = pd.read_csv(os.path.join(current_dir, "book.csv"))

    # Ensure 'Category' column exists
    if "Category" not in df_books.columns:
        raise KeyError("❌ Error: 'Category' column not found in book.csv")

    categories = df_books['Category'].dropna().unique().tolist()

except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    exit()
except Exception as e:
    print(f"❌ Error loading files: {e}")
    exit()

# Debug: Inspect popular_df
print("Debug: Columns in popular_df before merge:", popular_df.columns.tolist())
print("Debug: First 5 rows of popular_df before merge:")
print(popular_df.head())

# Debug: Inspect books
print("Debug: Columns in books:", books.columns.tolist())
print("Debug: First 5 rows of books:")
print(books.head())
print("Debug: Number of rows in books:", len(books))

# Drop Image-URL-L and Book-Author from popular_df if they exist to avoid conflicts
if 'Image-URL-L' in popular_df.columns:
    popular_df = popular_df.drop(columns=['Image-URL-L'])
if 'Book-Author' in popular_df.columns:
    popular_df = popular_df.drop(columns=['Book-Author'])

# Clean Book-Title columns to ensure consistent matching
popular_df['Book-Title'] = popular_df['Book-Title'].str.strip().str.lower().str.replace(r'[^a-z0-9\s]', '', regex=True)
books['Book-Title'] = books['Book-Title'].str.strip().str.lower().str.replace(r'[^a-z0-9\s]', '', regex=True)

# Perform the merge
if "Book-Title" in popular_df.columns and "Image-URL-L" in books.columns and "Book-Author" in books.columns:
    popular_df = popular_df.merge(books[['Book-Title', 'Book-Author', 'Image-URL-L']], on="Book-Title", how="left")
    popular_df = popular_df.drop_duplicates(subset=["Book-Title"])
    popular_df = popular_df.head(50)  # Limit to top 50 books

    # Debug: Inspect popular_df after merge
    print("Debug: Columns in popular_df after merge:", popular_df.columns.tolist())
    print("Debug: First 5 rows of popular_df after merge:")
    print(popular_df.head())
else:
    print("❌ Error: Missing 'Image-URL-L' or 'Book-Author' in books.pkl or incorrect column names.")
    exit()

# Check if Image-URL-L and Book-Author exist before accessing
if 'Image-URL-L' in popular_df.columns and 'Book-Author' in popular_df.columns:
    print("Debug: First 5 Image-URL-L values after merge:")
    print(popular_df['Image-URL-L'].head())
    print("Debug: Number of NaN Image-URL-L values:", popular_df['Image-URL-L'].isna().sum())
    print("Debug: First 5 Book-Author values after merge:")
    print(popular_df['Book-Author'].head())
    print("Debug: Number of NaN Book-Author values:", popular_df['Book-Author'].isna().sum())
else:
    print("❌ Error: 'Image-URL-L' or 'Book-Author' column is missing in popular_df after merge.")
    print("Debug: Available columns in popular_df:", popular_df.columns.tolist())
    exit()

# Ensure Image-URL-L and Book-Author are not NaN; fill with placeholders if needed
popular_df['Image-URL-L'] = popular_df['Image-URL-L'].fillna("https://via.placeholder.com/150")
popular_df['Image-URL-L'] = popular_df['Image-URL-L'].apply(lambda x: x if (isinstance(x, str) and x.startswith("http")) else "https://via.placeholder.com/150")
popular_df['Book-Author'] = popular_df['Book-Author'].fillna("Unknown Author")

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    """Main page displaying top 50 books (5 per row)."""
    per_page = 10  # Number of books per page
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(popular_df) + per_page - 1) // per_page
    paginated_books = popular_df[start:end]
    return render_template('index.html', books=paginated_books.to_dict(orient="records"), page=page, total_pages=total_pages, search_query='')


@app.route('/recommend')
def recommend():
    """Page to select a Category and get recommendations."""
    return render_template('recommend.html', categories=categories)

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    """Recommend books based on selected Category."""
    selected_category = request.form.get("Category", "").strip()

    if not selected_category:
        return render_template('recommend.html', categories=categories, error="❌ Please select a Category.")

    # Get books from the selected Category
    category_books = df_books[df_books['Category'] == selected_category]

    if category_books.empty:
        return render_template('recommend.html', categories=categories, error=f"❌ No books found in Category '{selected_category}'.")

    # Get the top 10 books from the selected Category
    recommended_books = category_books.head(10)

    return render_template('recommend.html', 
                           categories=categories, 
                           selected_category=selected_category,
                           recommendations=list(zip(recommended_books["Book-Title"], 
                                                    recommended_books["Book-Author"].fillna("Unknown Author"), 
                                                    recommended_books["Image-URL-L"].fillna("https://via.placeholder.com/150"))))

@app.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)