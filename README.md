# 🛍️ ML & NLP Amazon Product Recommender

An intelligent product discovery application that goes beyond simple keyword matching. This tool uses **Machine Learning (TF-IDF & Cosine Similarity)** and **Natural Language Processing (Sentiment Analysis)** to find Amazon products that precisely match your detailed text requirements.

## 🚀 Features

-   **General Search**: Search by broad categories (e.g., Laptops, Headphones, Mouse).
-   **Contextual Matching**: Enter detailed textual requirements (e.g., "I need a powerful device for gaming with a dedicated GPU and fast processor").
-   **Dual NLP/ML Analysis**: 
    -   **TF-IDF & Cosine Similarity**: Matches your description against product titles and details.
    -   **Sentiment Analysis**: Evaluates product descriptions to favor positively framed items.
-   **Weighted Scoring Engine**:
    -   60% Textual Match Similarity
    -   25% Product Rating
    -   15% Positive Sentiment Polarity
-   **Sorting Options**: Sort by Match Score (ML logic), Rating (Highest First), or Number of Reviews (Most Popular).
-   **Live Data**: Connects to Amazon via RapidAPI (with a robust offline mock data fallback).

## 🛠️ Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **Machine Learning**: [Scikit-Learn](https://scikit-learn.org/) (TF-IDF, Cosine Similarity)
-   **NLP**: [TextBlob](https://textblob.readthedocs.io/) (Sentiment Analysis)
-   **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
-   **API Handling**: [Requests](https://requests.readthedocs.io/)

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Amazon_Recommender
    ```

2.  **Install dependencies**:
    ```bash
    pip install streamlit pandas scikit-learn textblob numpy requests
    ```

3.  **Download TextBlob corpora**:
    ```bash
    python -m textblob.download_corpora
    ```

## 🏃 Overrunning the App

To launch the Streamlit dashboard:
```bash
streamlit run app.py
```
Alternatively, you can use the provided batch script:
```bash
run.bat
```

## 🔑 RapidAPI Key (Optional)

Users can input their own RapidAPI key in the sidebar to fetch live data. If no key is provided, the application automatically falls back to a high-quality offline demonstration dataset.

---
*Built with ❤️ for intelligent shopping.*
