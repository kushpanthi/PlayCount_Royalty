# PlayCount Royalty

IoT-based audio recognition system for music play tracking and royalty management.

## System Overview

PlayCount Royalty is a distributed system consisting of ESP32 IoT devices that capture audio samples and a Flask-based backend server that processes these samples for song recognition. The system identifies copyrighted music plays and logs them to a centralized database and Google Sheets for royalty tracking.



## Components

- **ESP32 Devices**: Capture 10-second audio clips and transmit via HTTP
- **Flask Backend**: REST API for audio processing and recognition
- **Dejavu**: Audio fingerprinting and recognition engine
- **MySQL**: Persistent storage for fingerprints and play logs
- **Google Sheets API**: Secondary logging and reporting interface

## Prerequisites

- Python 3.9+
- MySQL 8.0+
- Arduino IDE (for ESP32 firmware)
- Docker 20.10+ (optional, for containerized deployment)

## Quick Start

### 1. Database Setup

```bash
mysql -u root -p < database/schema.sql

## Components

git clone https://github.com/yourusername/PlayCount-Royalty.git
cd PlayCount-Royalty/backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp ../.env.example .env

# Edit .env with your settings

```bash
python app.py

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=playcount_royalty

# Google Sheets API
GSHEETS_CREDS=credentials.json
GSHEETS_ID=your_google_sheet_id

# Application Settings
SECRET_KEY=your_secret_key_here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

{
  "status": "success",
  "song_name": "Recognized Song Name",
  "confidence": 95.5,
  "device_id": "esp32_001",
  "timestamp": "2024-01-15T10:30:00.000Z"
}

{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}

# Database Schema

CREATE TABLE songs (
    song_id MEDIUMINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    song_name VARCHAR(250) NOT NULL,
    fingerprinted TINYINT DEFAULT 0,
    file_sha1 BINARY(20),
    artist VARCHAR(250),
    album VARCHAR(250),
    genre VARCHAR(100),
    INDEX(song_name),
    INDEX(artist)
);

CREATE TABLE plays (
    play_id INT AUTO_INCREMENT PRIMARY KEY,
    song_name VARCHAR(255) NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    confidence FLOAT NOT NULL,
    recognized_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX(device_id),
    INDEX(timestamp),
    INDEX(song_name)
);

CREATE TABLE devices (
    device_id VARCHAR(100) PRIMARY KEY,
    device_name VARCHAR(255),
    location VARCHAR(255),
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen DATETIME,
    is_active BOOLEAN DEFAULT TRUE
);

```bash
docker-compose -f docker/docker-compose.yml up --build
docker-compose -f docker/docker-compose.yml up -d
docker-compose -f docker/docker-compose.yml logs -f
