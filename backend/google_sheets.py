import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_google_sheets_client():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds_file = os.getenv('GSHEETS_CREDS', 'credentials.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Failed to authenticate with Google Sheets: {e}")
        raise

def log_to_google_sheet(song_name, device_id, confidence):
    try:
        client = get_google_sheets_client()
        spreadsheet_id = os.getenv('GSHEETS_ID')
        
        if not spreadsheet_id:
            logger.error("Google Sheets ID not configured")
            return False
            
        sheet = client.open_by_key(spreadsheet_id).sheet1
        
        # Append the data
        row = [
            song_name,
            device_id,
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            f"{confidence:.2f}%"
        ]
        
        sheet.append_row(row)
        logger.info(f"Logged to Google Sheets: {song_name} by device {device_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to log to Google Sheets: {e}")
        return False
