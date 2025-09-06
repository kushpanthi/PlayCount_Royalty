from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
from dejavu_setup import setup_dejavu, recognize_song
from google_sheets import log_to_google_sheet
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Dejavu
try:
    dejavu = setup_dejavu()
    logger.info("Dejavu audio fingerprinting system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Dejavu: {e}")
    dejavu = None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
        
    file = request.files['audio']
    device_id = request.headers.get('Device-ID') or request.form.get('device_id', 'unknown')
    
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
        
    try:
        # Save uploaded file
        filename = secure_filename(f"{device_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.wav")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"Saved uploaded file: {filepath}")
        
        # Recognize song
        if dejavu:
            song = recognize_song(dejavu, filepath)
            if song:
                # Log to Google Sheets
                log_to_google_sheet(
                    song_name=song['song_name'],
                    device_id=device_id,
                    confidence=song['confidence']
                )
                
                # Clean up file
                os.remove(filepath)
                
                return jsonify({
                    'status': 'success',
                    'song_name': song['song_name'],
                    'confidence': song['confidence'],
                    'device_id': device_id,
                    'timestamp': datetime.utcnow().isoformat()
                }), 200
            else:
                return jsonify({'status': 'no_match', 'message': 'No song recognized'}), 200
        else:
            return jsonify({'error': 'Audio recognition system not available'}), 503
            
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    logger.info(f"Starting server on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
