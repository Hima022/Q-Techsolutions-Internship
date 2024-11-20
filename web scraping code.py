# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import json

# Pre-trained AI model setup (example: sentiment analysis)
def load_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=10000, output_dim=16, input_length=100),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Load the model
model = load_model()

# Pre-trained tokenizer setup
tokenizer = Tokenizer(num_words=10000)

# Predefined URLs for scraping
URLS = [
    "https://www.bbc.com/news",
    "https://www.amazon.com/s?k=smartphones",
    "https://dev.to/t/data",
    "https://www.cnbc.com/markets/"
]

# Scrape and analyze data
def scrape_and_analyze(url):
    try:
        # Scrape data
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Collect relevant text data
        if "bbc" in url or "cnbc" in url:  # News articles
            paragraphs = soup.find_all('p')
        elif "amazon" in url:  # E-commerce
            paragraphs = soup.find_all('span', class_='a-size-base review-text review-text-content')
        elif "dev.to" in url:  # Blogs
            paragraphs = soup.find_all('div', class_='crayons-article__body')
        else:
            paragraphs = soup.find_all('p')  # Fallback

        text_data = ' '.join([para.text for para in paragraphs])

        # Tokenize and pad sequences for sentiment analysis
        sequences = tokenizer.texts_to_sequences([text_data])
        padded_sequences = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')

        # Perform sentiment analysis
        prediction = model.predict(padded_sequences)
        sentiment = "Positive" if prediction[0] > 0.5 else "Negative"

        return {
            "url": url,
            "scraped_text": text_data[:500],  # Limiting the text for display
            "sentiment": sentiment,
            "confidence": float(prediction[0])
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

# Main function for scraping all predefined URLs
def scrape_all():
    results = []
    for url in URLS:
        result = scrape_and_analyze(url)
        results.append(result)
    return results

# Run the scraper and save results to a file
if __name__ == "__main__":
    data = scrape_all()
    # Save the analysis results to a JSON file
    with open("scraped_data_analysis.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Scraping and analysis complete. Results saved to 'scraped_data_analysis.json'.")
