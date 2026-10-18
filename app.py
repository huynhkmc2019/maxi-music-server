
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "server": "Maxi Music Server",
        "status": "online",
        "message": "Maxi Robot Music Server is ready!"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/music/test")
def music_test():
    return jsonify({
        "status": "ready",
        "message": "Music API is working",
        "format": "mp3"
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
