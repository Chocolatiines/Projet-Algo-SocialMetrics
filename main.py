from flask import Flask, request, jsonify
import joblib
import re


app = Flask(__name__)

model_positive = joblib.load("model_positive.joblib")
model_negative = joblib.load("model_negative.joblib")
vectorizer = joblib.load("vectorizer.joblib")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "Data must be a list."}), 400

        clean_tweets = [clean_text(tweet) for tweet in data]
        vectorized_tweets = vectorizer.transform(clean_tweets)

        positive_predictions = model_positive.predict_proba(vectorized_tweets)
        negative_predictions = model_negative.predict_proba(vectorized_tweets)

        if positive_predictions.ndim == 2:
            positive_predictions = positive_predictions[:, 1]
        else:
            positive_predictions = positive_predictions

        if negative_predictions.ndim == 2:
            negative_predictions = negative_predictions[:, 1]
        else:
            negative_predictions = negative_predictions

        results = []
        for tweet, positive_score, negative_score in zip(data, positive_predictions, negative_predictions):
            sentiment_score = float(positive_score) - float(negative_score)
            results.append({"tweet": tweet, "sentiment_score": round(sentiment_score, 3)})

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)