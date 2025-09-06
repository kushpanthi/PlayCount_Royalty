from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
import os
import logging

logger = logging.getLogger(__name__)

def get_dejavu_config():
    return {
        "database": {
            "host": os.getenv('DB_HOST', 'localhost'),
            "user": os.getenv('DB_USER', 'root'),
            "password": os.getenv('DB_PASSWORD', 'password'),
            "database": os.getenv('DB_NAME', 'playcount_royalty'),
        },
        "database_type": "mysql",
        "fingerprint_limit": 20
    }

def setup_dejavu():
    try:
        config = get_dejavu_config()
        dejavu_instance = Dejavu(config)
        logger.info("Dejavu initialized successfully")
        return dejavu_instance
    except Exception as e:
        logger.error(f"Failed to initialize Dejavu: {e}")
        raise

def recognize_song(dejavu_instance, filepath):
    try:
        results = dejavu_instance.recognize(FileRecognizer, filepath)
        
        if results and 'results' in results and results['results']:
            # Get the best match
            best_match = max(results['results'], key=lambda x: x['confidence'])
            
            if best_match['confidence'] > 50:  # Confidence threshold
                return {
                    'song_name': best_match['song_name'],
                    'confidence': best_match['confidence'],
                    'offset': best_match['offset']
                }
            else:
                logger.info(f"Low confidence match: {best_match['song_name']} ({best_match['confidence']}%)")
        else:
            logger.info("No matches found for the audio sample")
            
    except Exception as e:
        logger.error(f"Error during song recognition: {e}")
    
    return None
