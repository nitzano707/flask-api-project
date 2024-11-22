import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pyannote.audio import Pipeline

app = Flask(__name__)
CORS(app)  # מאפשר תמיכה ב-CORS לכל היישום

# טוקן של Hugging Face (מתוך משתנה סביבה)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# אתחול של מודל הדיאריזציה
try:
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=HUGGINGFACE_TOKEN)
except Exception as e:
    print(f"Error initializing pipeline: {e}")
    pipeline = None

@app.route('/')
def serve_html():
    return send_from_directory('', 'index.html')

@app.route('/diarize', methods=['POST'])
def diarize():
    if pipeline is None:
        return jsonify({"error": "Pipeline not initialized"}), 500

    # קבלת קובץ האודיו מהבקשה
    audio_data = request.files.get('audio')

    if not audio_data:
        return jsonify({"error": "No audio file provided"}), 400

    # שמירת הקובץ שנשלח
    audio_path = "uploaded_audio.wav"
    audio_data.save(audio_path)

    # הרצת דיאריזציה
    try:
        diarization = pipeline(audio_path)
        
        # עיבוד התוצאה לטקסט
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "speaker": speaker,
                "start": turn.start,
                "end": turn.end
            })

        return jsonify({"message": "Audio file processed successfully!", "segments": segments})
    except Exception as e:
        return jsonify({"error": f"Error processing audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
