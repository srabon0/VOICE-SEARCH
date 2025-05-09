from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from product_search_ai import ProductSearchAI
import speech_recognition as sr
import os
from datetime import datetime
app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure template auto-reload during development
app.config['TEMPLATES_AUTO_RELOAD'] = True

ai = ProductSearchAI()

@app.route('/')


@app.route('/')
def home():
    """Render the main search page"""
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        query = data.get("query")
        if not query:
            return jsonify({"error": "Missing query"}), 400

        result = ai.process_query(query)

        return jsonify({
            "search_term": result.get("search_term", ""),
            "filters": result.get("filters", {}),
            "query_type": "voice" if data.get("is_voice") else "text"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "Empty audio file"}), 400

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            query = recognizer.recognize_google(audio)

            result = ai.process_query(query)

            return jsonify({
                "text": query,
                "search_term": result.get("search_term", ""),
                "filters": result.get("filters", {})
            })
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Speech service error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)