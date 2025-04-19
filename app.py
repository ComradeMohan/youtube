from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    video_streams = []
    if request.method == "POST":
        url = request.form["url"]
        try:
            yt = YouTube(url)
            video_streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
            return render_template("index.html", streams=video_streams, url=url)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html", streams=video_streams)

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    itag = request.form["itag"]
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        filename = stream.download()
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
