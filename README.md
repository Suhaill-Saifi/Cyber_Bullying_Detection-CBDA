# Cyberbullying Detection (CBDA)

Minor Project for Semester 7, B.Tech (CSE)

Unlocking safer online environments with Machine Learning and NLP innovation. This project aims to detect instances of cyberbullying in real-time using advanced NLP techniques and machine learning algorithms.

## Team Members:
- **Suhail Saifi** (RA2111003030439)
- **Karan Rana** (RA2111003030446)
- **Mohd. Zufar Hasan Alvi** (RA2111003030435)
- **Sohail** (RA2111003030436)

**Supervised by:** CSE, SRMIST Ghaziabad

---

## Project Overview

Cyberbullying is a growing problem in the digital age, especially on platforms like Twitter. Our project leverages the power of modern NLP techniques and machine learning to analyze tweet data and classify harmful content (cyberbullying) from non-harmful content (non-cyberbullying).

This project incorporates:

- **Sentiment Analysis**
- **Word Embeddings** (Word2Vec, GloVe)
- **Feature Extraction** (TF-IDF)
- **Machine Learning Algorithms**: SVM, KNN, Logistic Regression

---

## Getting Started

To get started simply download this repository.

### Clone the Project
```bash
https://github.com/Suhaill-Saifi/Cyber_Bullying_Detection-CBDA.git
```

Switch into the source folder and create a virtual environment:
```bash
$ cd Cyber_Bullying_Detection-CBDA
$ python3 -m venv myenv
$ source myenv/bin/activate # For Windows: myenv\Scripts\activate
```

### Install Dependencies
Install all required dependencies:
```bash
pip install -r requirements.txt
```

---

## Running the Application

### Backend Server
To start the backend server, run:
```bash
python3 server.py
```

### Clients
1. **Command-Line Client**
   ```bash
   python3 client.py
   ```

2. **GUI Client**
   ```bash
   python3 client_gui.py
   ```

---

## Features

1. **Data Preprocessing:** Cleaning, tokenization, and lemmatization of tweets.
2. **Feature Extraction:** Representing textual data in numerical form using TF-IDF and Word Embeddings.
3. **Model Training:** Classifying tweets as cyberbullying or non-cyberbullying with high accuracy.

---

## Technology Stack

- **Programming Language:** Python 3.x
- **Frameworks and Libraries:**
  - `nltk`
  - `scikit-learn`
  - `numpy`
  - `pandas`
  - `tensorflow`
  - `keras`
- **Machine Learning Algorithms:**
  - SVM (Support Vector Machine)
  - KNN (K-Nearest Neighbors)
  - Logistic Regression
- **Natural Language Processing Techniques:**
  - Tokenization
  - Lemmatization
  - Sentiment Analysis
  - Word Embeddings (Word2Vec, GloVe)

---

## Dataset

The model is trained on publicly available datasets, including:
- **Cyberbullying Dataset from Kaggle**
- **HateEval Dataset from SemEval**

---

## Evaluation Metrics

- **Precision**
- **Recall**
- **F1-Score**
- **Accuracy**

---

## Screenshots
<img width="1083" alt="Screenshot 2024-07-03 at 6 42 19 PM" src="https://github.com/user-attachments/assets/f534d1d4-774e-4163-92f0-1dbdeeeb65dc" />

### Example Output
<img width="1287" alt="Screenshot 2024-09-18 at 12 13 12 PM" src="https://github.com/user-attachments/assets/19a6a965-5235-4e25-9bef-d6e00a6afcde" />
<img width="443" alt="Screenshot 2024-09-18 at 12 13 34 PM" src="https://github.com/user-attachments/assets/5d63291a-6e56-4949-891f-f31384d61d81" />
<img width="1286" alt="Screenshot 2024-09-18 at 12 13 53 PM" src="https://github.com/user-attachments/assets/1d7b4059-2b45-447a-8302-9cf8dc174176" />

### GUI Interface
<img width="417" alt="Screenshot 2024-09-18 at 12 11 11 PM" src="https://github.com/user-attachments/assets/e797b4fd-ff2f-4dfe-ab52-f1ddd345073b" />
<img width="978" alt="Screenshot 2024-09-18 at 12 12 41 PM" src="https://github.com/user-attachments/assets/32df4d1a-e42b-45bc-8b5e-aa0b61cc53bb" />

---

## Authors

- **Suhail Saifi:** Lead Developer, NLP Implementation
- **Karan Rana:** Machine Learning Model Development, Evaluation
- **Mohd. Zufar Hasan Alvi:** Data Preprocessing, Feature Extraction
- **Sohail:** Client and Server Communication

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## Contact Us
For more information or questions, feel free to contact us at:

- **Karan Rana:** kr2081@srmist.edu.in
- **Suhail Saifi:** ss2280@srmist.edu.in
- **Mohd. Zufar Hasan Alvi:** mh1356@srmist.edu.in
- **Sohail:** sz2324@srmist.edu.in

---

## Acknowledgements
We would like to thank SRMIST, Ghaziabad, and our professors for their support and guidance throughout this project.
