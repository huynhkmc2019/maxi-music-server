
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

@app.route("/music/test.mp3")
def play_test_music():
    from flask import send_file
    return send_file("test.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
