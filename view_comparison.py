import re
from itertools import combinations

import openai
import numpy as np

# Set your OpenAI API key
client = openai.OpenAI(
    api_key=""
)

percentage_regex = re.compile(r"\d*(?:\.\d)?(?:%)?")


def compare_political_views(article1: str, article2: str):
    return sum(compare_political_views_once(article1, article2) for i in range(5)) / 5


def compare_political_views_once(article1: str, article2: str) -> float:
    # Define the prompt for ChatGPT
    prompt = (
        "You are a political expert and a news reviewer.\n"
        "You are given two news articles on the same specific event. Your task is to compare the political views "
        "of the authors of each article and provide a percentage score indicating how different their political "
        "views are. Use nuance and judgement as the articles are likely to be mostly similar as they reference the same event. "
        "The score should be a value between 0% and 100%, using the following criteria:\n"
        "100% - The views of the authors are completely identical\n"
        "80% - The views of the authors are mostly similar\n"
        "60% - The views of the authors are somewhat similar\n"
        "40% - The views of the authors are somewhat different\n"
        "20% - The views of the authors are very different\n"
        "0% - The views of the authors are completely opposite\n\n"
        "Article 1:\n" + article1 + "\n\n"
        "Article 2:\n" + article2 + "\n\n"
        "Judge the similarity based on the political perspective ONLY! The articles are guaranteed to focus on the same event and be based on the same context - those should ABSOLUTELY NOT be a factor in your score. "
        "You MUST provide a percentage score, and nothing else."
    )

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )

    # Extract the response content
    response_text = response.choices[0].message.content.strip()

    try:
        # Extract and return the percentage score from the response
        score = float(percentage_regex.search(response_text).group().strip('%'))
        return score
    except ValueError:
        raise ValueError("Invalid response format from ChatGPT.")


def create_adjacency_matrix(articles: list) -> np.ndarray:
    num_articles = len(articles)
    # Initialize a square matrix with zeros
    adjacency_matrix = np.zeros((num_articles, num_articles))

    # Compute the political difference for every pair of articles
    for i in range(num_articles):
        for j in range(i + 1, num_articles):
            score = compare_political_views(articles[i], articles[j])
            adjacency_matrix[i][j] = score
            adjacency_matrix[j][i] = score  # The matrix is symmetric

    return adjacency_matrix


def find_optimal_subset(adjacency_matrix: np.ndarray) -> list:
    num_articles = len(adjacency_matrix)

    # Ensure the first article (index 0) is included
    first_article_index = 0

    # Function to check if all pairs in the subset satisfy the condition
    def is_valid_subset(subset):
        for i, j in combinations(subset, 2):
            if adjacency_matrix[i][j] >= 40:
                return False
        return True

    # Store the best subset and its maximum difference score
    best_subset = []
    best_max_diff = float('inf')

    # Generate all possible subsets containing the first article
    for size in range(5, 0, -1):
        for subset in combinations(range(num_articles), size):
            if first_article_index in subset and is_valid_subset(subset):
                # Calculate the maximum difference score in this subset
                max_diff = max([adjacency_matrix[i][j] for i, j in combinations(subset, 2)] + [float('-inf')])
                if max_diff < best_max_diff:
                    best_max_diff = max_diff
                    best_subset = subset
        if best_subset != []:
            return list(best_subset)

    return [0]
