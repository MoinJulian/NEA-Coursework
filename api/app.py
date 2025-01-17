from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello World!", "status": 200})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)