from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

# Endpoint to fetch available video and audio formats for a YouTube video
@app.route('/get_video_info', methods=['GET'])
def get_video_info():
    video_url = request.args.get('url')
    yt = YouTube(video_url)
    
    # Extracting video information
    title = yt.title
    thumbnail_url = yt.thumbnail_url
    video_formats = yt.streams.filter(progressive=True, file_extension='mp4').all()
    audio_formats = yt.streams.filter(only_audio=True).all()
    
    # Creating response dictionary
    response = {
        'title': title,
        'thumbnail_url': thumbnail_url,
        'video_formats': [format.resolution for format in video_formats],
        'audio_formats': [format.abr for format in audio_formats]  # Example: abr attribute for audio bitrate
    }
    
    return jsonify(response)

# Endpoint to get download link for selected format
@app.route('/get_download_link', methods=['GET'])
def get_download_link():
    video_url = request.args.get('url')
    selected_format = request.args.get('format')
    
    yt = YouTube(video_url)
    
    # Check if selected format belongs to video or audio
    if any(selected_format in format.resolution for format in yt.streams.filter(progressive=True, file_extension='mp4').all()):
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_format).first()
    else:
        stream = yt.streams.filter(only_audio=True, abr=selected_format).first()
    
    if stream:
        download_link = stream.url
    else:
        download_link = None
    
    response = {
        'download_link': download_link
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
