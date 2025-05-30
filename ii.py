import pandas as pd

# Load dataset
df = pd.read_csv(r"E:\book-recommender-system-master\book-recommender-system-master\book.csv")


# Print first 10 image URLs
print(df["Image-URL-L"].head(10))
