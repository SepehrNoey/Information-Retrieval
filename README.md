# Information Retrieval System

This project implements a basic Information Retrieval (IR) system on a dataset of 13,000 Persian news articles. The system supports preprocessing, indexing, and retrieval using a variety of Information Retrieval techniques.

## Features

### 1. Preprocessing
The preprocessing phase included several key steps:
- **Lemmatization**: Converted different tenses of verbs and variations of words into their root form.
- **Normalization**: Standardized the text by converting all characters to a uniform case and removing any special characters.
- **Tokenization**: Split the text into individual tokens (words/terms) for analysis.

### 2. Inverted Index
An **Inverted Index** was built over the dataset to allow for efficient document retrieval. Each token is mapped to the list of documents (news articles) where it appears.

### 3. Positional Index
The system also supports a **Positional Index**, where both the term and its position within the document are stored. This allows for more advanced query retrieval techniques such as phrase queries.

### 4. Positional Query Retrieval
Implemented **Positional Query Retrieval**, where the system can handle phrase queries and return documents where the exact phrase appears by checking word positions within documents.

### 5. TF-IDF & Cosine Similarity
For calculating the relevance of documents to a given query:
- **TF-IDF (Term Frequency-Inverse Document Frequency)** was used to weigh terms by their importance in both the document and the overall dataset.
- **Cosine Similarity** was implemented to measure the similarity between the query and each document.

### 6. Champions List
To optimize retrieval, **Champions Lists** were implemented. This technique calculates similarity scores for a limited set of the most relevant documents (top-K documents), improving retrieval speed.

## How It Works

1. **Preprocessing**: The input Persian news dataset is first preprocessed using the steps mentioned above.
2. **Indexing**: An inverted index and a positional index are created from the processed dataset.
3. **Query Retrieval**: The user inputs a query, which is then processed and matched against the indexes using TF-IDF and cosine similarity.
4. **Champion Lists**: The top-K relevant documents are retrieved from the Champions Lists to optimize query response time.
