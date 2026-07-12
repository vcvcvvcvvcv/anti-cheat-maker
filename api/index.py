from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "Spectre AI Online"
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    # AI logic will go here
    reply = (
        "Spectre AI specializes in Gorilla Tag copy "
        "security, anti-cheat architecture, Unity, "
        "PlayFab, and Photon."
    )

    return jsonify({
        "reply": reply
    })
