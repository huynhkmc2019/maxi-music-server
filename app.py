
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

@app.route("/music/test.pcm")
def play_test_pcm():
    import subprocess
    import imageio_ffmpeg
    from flask import Response, stream_with_context

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    def generate_pcm():
        process = subprocess.Popen(
            [
                ffmpeg_path,
                "-hide_banner",
                "-loglevel", "error",
                "-i", "test.mp3",
                "-f", "s16le",
                "-acodec", "pcm_s16le",
                "-ac", "1",
                "-ar", "24000",
                "pipe:1"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        try:
            while True:
                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                yield chunk
        finally:
            if process.poll() is None:
                process.terminate()
            process.stdout.close()
            process.wait()

    return Response(
        stream_with_context(generate_pcm()),
        mimetype="application/octet-stream",
        headers={"Cache-Control": "no-store"}
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
