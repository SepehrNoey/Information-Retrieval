# Information Retrieval System

This project implements a basic Information Retrieval (IR) system on a dataset of 13,000 Persian news articles. The system supports preprocessing, indexing, and retrieval using a variety of Information Retrieval techniques. The datasets used for creating indices and testing them can be found [here](https://drive.google.com/drive/folders/11yStVcviiOqXppQixSCNNVw3i8s8erm0?usp=sharing).

## Sample Queries (Written in Persian):
For each query, we print **only the first retrieved document ID** by three type of indices:
- `Normal Index` that uses TF-IDF and cosine similarity on the whole documents to search on.
- `Positional Index` that tries to find documents that has at least some of the terms placed consecutively, and if doesn't find any document with this property, it acts just like `Normal Index`.
- `Champion Lit Index` that searchs on documents that have at least 5 occurrence of the term given. As a result, it retrieves documents faster but it may not retrieve all the related documents.
 
|Given Query|Normal|Positional|Champion|Explanation|
|-----|----|----|----|----|
|"پرسپولیس تهران"|6715|6715|6339|`Normal Index` retrieved document with most frequency of the terms (term "تهران" occurred 6 times and term "پرسپولیس" occurred 3 times). As in no document, the terms were present consecutively, the `positional index` acted just like normal index. And `Champion index` just searchs on documents that have both terms repeated at least 5 times. As a result it retrieved another document.|



A snippet of document 6715 with the term "تهران" highlighted:

![6715](https://github.com/user-attachments/assets/e2e1ca77-baa4-4a7b-8ef6-24e16ac6d578)

#### Another Sample
|Given Query|Normal|Positional|Champion|Explanation|
|-----|----|----|----|----|
|محصولات کشاورزی منطقه|8851|12005|12005|`Normal Index` has retrieved the best matching document. However, the `Positional Index` has retrieved the document that has the exact terms consecutivey. `Champion List Index` has not processed the doc 8851 because this doc has only 2 occurrences of the term "محصولات", so retrieved another document.|

Document 8851:

![8851](https://github.com/user-attachments/assets/9b92673d-d705-4946-a7e0-67ef4ae5579c)
As shown in the the image, the whole terms are not present consecutively. However each terms have occurred several times which makes the score of doc 8851 higher than 12005.

A snippet of document 12005. The whole terms are present consecutively:

![12005](https://github.com/user-attachments/assets/b64bfbc4-d8ef-49f6-a2ad-5ef7fa792f5c)


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
