import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime

def cluster_and_find_target_articles(target_article, articles, dates, num_clusters=5):
    # Ensure articles and dates are in the same length
    if len(articles) != len(dates):
        raise ValueError("Length of articles and dates must be the same")

    # Create a DataFrame for convenience
    df = pd.DataFrame({
        'article': articles,
        'date': pd.to_datetime(dates)
    })

    # Preprocess the text data
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['article'])

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    df['cluster'] = kmeans.fit_predict(X)

    # Vectorize the target article
    target_vector = vectorizer.transform([target_article])

    # Predict the cluster of the target article
    target_cluster = kmeans.predict(target_vector)[0]

    # Filter articles in the same cluster as the target article
    target_articles = df[df['cluster'] == target_cluster]

    # Return articles from the same cluster sorted by date
    target_articles_sorted = target_articles.sort_values(by='date', ascending=False)

    return target_articles_sorted['article'].tolist()

# Example usage
target_article = "Machine learning models require careful tuning and validation."
articles = [
    "Understanding deep learning and its applications.",
    "Basics of machine learning and data preparation.",
    "Advanced techniques in machine learning.",
    "The importance of validation in model training.",
    "How deep learning is revolutionizing artificial intelligence."
]
dates = [
    "2024-07-20",
    "2024-07-18",
    "2024-07-15",
    "2024-07-10",
    "2024-07-25"
]

result = cluster_and_find_target_articles(target_article, articles, dates)
print(result)
