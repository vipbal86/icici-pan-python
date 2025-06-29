from flask import Flask, request, jsonify, render_template
from google.cloud import firestore
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize Firestore client
db = firestore.Client()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/fetch-account", methods=["POST"])
def fetch_account():
    data = request.json
    pan = data.get("pan")

    dummy_result = {
        "message": "ICICI API call simulated",
        "pan": pan,
        "accounts": [
            {
                "acctId": "1234567890",
                "acctName": "WINSTON LOBO",
                "openDate": "05-12-2017"
            }
        ]
    }

    try:
        doc_ref = db.collection("panRequests").document()
        doc_ref.set({
            "pan": pan,
            "result": dummy_result
        })
        print("Saved to Firestore")
    except Exception as e:
        print("Firestore error:", e)

    return jsonify(dummy_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
