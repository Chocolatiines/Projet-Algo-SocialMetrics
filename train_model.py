import mysql.connector
import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from init_db import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

try:
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

    if connection.is_connected():
        print("Connected to MySQL")

        query = ("SELECT text, positive, negative FROM tweets")
        df = pd.read_sql(query, connection)

        def clean_text(text):
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            return text

        df['text_clean'] = df['text'].apply(clean_text)

        french_stopwords = [
            "le", "la", "les", "un", "une", "des", "du", "de", "dans", "et", "en", "au",
            "aux", "avec", "ce", "ces", "pour", "par", "sur", "pas", "plus", "où", "mais",
            "ou", "donc", "ni", "car", "ne", "que", "qui", "quoi", "quand", "à", "son",
            "sa", "ses", "ils", "elles", "nous", "vous", "est", "sont", "cette", "cet",
            "aussi", "être", "avoir", "faire", "comme", "tout", "bien", "mal", "on", "lui"
        ]

        vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)
        X = vectorizer.fit_transform(df['text_clean'])

        X_train, X_test, y_train_pos, y_test_pos, y_train_neg, y_test_neg = train_test_split(
            X, df['positive'], df['negative'], test_size=0.3, random_state=42
        )

        model_positive = LogisticRegression()
        model_positive.fit(X_train, y_train_pos)
        print("Positive model trained successfully.")
        print(classification_report(y_test_pos, model_positive.predict(X_test)))
        print(confusion_matrix(y_test_pos, model_positive.predict(X_test)))

        model_negative = LogisticRegression()
        model_negative.fit(X_train, y_train_neg)
        print("Negative model trained successfully.")
        print(classification_report(y_test_neg, model_negative.predict(X_test)))
        print(confusion_matrix(y_test_neg, model_negative.predict(X_test)))

        # Save the models
        joblib.dump(model_positive, "model_positive.joblib")
        joblib.dump(model_negative, "model_negative.joblib")
        joblib.dump(vectorizer, "vectorizer.joblib")

        print("Models saved successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")