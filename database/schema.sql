-- PlayCount Royalty Database Schema
CREATE DATABASE IF NOT EXISTS playcount_royalty;
USE playcount_royalty;

-- Table for storing audio fingerprints
CREATE TABLE IF NOT EXISTS fingerprints (
    hash BINARY(10) NOT NULL,
    song_id MEDIUMINT UNSIGNED NOT NULL,
    offset INT UNSIGNED NOT NULL,
    INDEX(hash),
    UNIQUE(song_id, offset, hash)
);

-- Table for storing song information
CREATE TABLE IF NOT EXISTS songs (
    song_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    song_name VARCHAR(250) NOT NULL,
    fingerprinted TINYINT DEFAULT 0,
    file_sha1 BINARY(20),
    artist VARCHAR(250),
    album VARCHAR(250),
    genre VARCHAR(100),
    INDEX(song_name),
    INDEX(artist)
);

-- Table for logging plays
CREATE TABLE IF NOT EXISTS plays (
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

-- Table for registered devices
CREATE TABLE IF NOT EXISTS devices (
    device_id VARCHAR(100) PRIMARY KEY,
    device_name VARCHAR(255),
    location VARCHAR(255),
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen DATETIME,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert sample data
INSERT INTO songs (song_name, artist, album, genre) VALUES
('Sample Song 1', 'Artist A', 'Album X', 'Pop'),
('Sample Song 2', 'Artist B', 'Album Y', 'Rock'),
('Sample Song 3', 'Artist C', 'Album Z', 'Classical');

INSERT INTO devices (device_id, device_name, location) VALUES
('esp32_001', 'Main Radio Station', 'Kathmandu'),
('esp32_002', 'Concert Hall', 'Pokhara'),
('simulated_esp32_001', 'Test Device', 'Development');
