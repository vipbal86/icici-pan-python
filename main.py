from flask import Flask, render_template, render_template_string, request, jsonify
from google.cloud import firestore

app = Flask(__name__)

# force correct project ID
db = firestore.Client(project="composite-jetty-464401-n9")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/fetch-account", methods=["POST"])
def fetch_account():
    print("🔥🔥🔥 API endpoint running with Firestore logic.")

    data = request.json
    print("👉 Received request data:", data)

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
        print("🔥 Attempting Firestore write...")
        doc_ref = db.collection("panRequests").document()
        doc_ref.set({
            "pan": pan,
            "result": dummy_result
        })
        print("✅ Firestore write successful.")

    except Exception as e:
        print("❌ Firestore error:", e)

    return jsonify(dummy_result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
