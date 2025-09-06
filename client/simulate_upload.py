import requests
import os
import time
from datetime import datetime

def simulate_esp32_upload():
    server_url = "http://localhost:5000/upload"
    audio_file = "sample_audio.wav"  # Replace with actual sample file
    
    if not os.path.exists(audio_file):
        print(f"Sample audio file '{audio_file}' not found.")
        print("Please create a sample WAV file or download one for testing.")
        return
    
    print("Simulating ESP32 audio upload...")
    
    with open(audio_file, 'rb') as f:
        files = {'audio': f}
        headers = {'Device-ID': 'simulated_esp32_001'}
        
        try:
            response = requests.post(server_url, files=files, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the server. Make sure the Flask server is running.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    simulate_esp32_upload()
