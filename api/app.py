from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "Health Check passed", "status": 200})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)