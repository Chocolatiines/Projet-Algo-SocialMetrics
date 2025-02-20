from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "Data must be a list."}), 400

        results = [{"tweet": tweet, "sentiment_score": 1} for tweet in data]

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)