#include <WiFi.h>
#include <HTTPClient.h>
#include <driver/i2s.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server details
const char* serverURL = "http://YOUR_SERVER_IP:5000/upload";

// I2S microphone configuration
#define I2S_WS 15
#define I2S_SD 13
#define I2S_SCK 2
#define I2S_PORT I2S_NUM_0

// Audio recording settings
const int sampleRate = 44100;
const int recordDuration = 10; // seconds
const int bufferSize = sampleRate * recordDuration;
const int deviceId = 001; // Unique device ID

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  
  // Setup I2S
  setupI2S();
}

void loop() {
  Serial.println("Recording audio...");
  
  // Record audio
  int16_t* audioBuffer = recordAudio();
  
  // Send to server
  if (audioBuffer != NULL) {
    sendAudioToServer(audioBuffer, bufferSize);
    free(audioBuffer);
  } else {
    Serial.println("Audio recording failed");
  }
  
  // Wait before next recording (5 minutes)
  Serial.println("Waiting for next recording in 5 minutes...");
  delay(300000);
}

void setupI2S() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = sampleRate,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 1024,
  };
  
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_in_num = I2S_SD,
    .data_out_num = I2S_PIN_NO_CHANGE
  };
  
  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
}

int16_t* recordAudio() {
  int16_t* buffer = (int16_t*)malloc(bufferSize * sizeof(int16_t));
  if (buffer == NULL) {
    Serial.println("Failed to allocate memory for audio buffer");
    return NULL;
  }
  
  size_t bytesRead = 0;
  esp_err_t result = i2s_read(I2S_PORT, buffer, bufferSize * sizeof(int16_t), &bytesRead, portMAX_DELAY);
  
  if (result != ESP_OK) {
    Serial.printf("I2S read error: %d\n", result);
    free(buffer);
    return NULL;
  }
  
  Serial.printf("Recorded %d bytes of audio\n", bytesRead);
  return buffer;
}

void sendAudioToServer(int16_t* audioData, int dataSize) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected");
    return;
  }
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/octet-stream");
  http.addHeader("Device-ID", String(deviceId));
  
  // Convert audio data to byte array
  uint8_t* byteData = (uint8_t*)audioData;
  int byteSize = dataSize * sizeof(int16_t);
  
  Serial.println("Sending audio to server...");
  int httpResponseCode = http.POST(byteData, byteSize);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("Server response: ");
    Serial.println(response);
    
    // Parse JSON response
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, response);
    
    if (doc.containsKey("song_name")) {
      Serial.print("Recognized song: ");
      Serial.println(doc["song_name"].as<String>());
      Serial.print("Confidence: ");
      Serial.println(doc["confidence"].as<float>());
    }
  } else {
    Serial.printf("Error sending audio: %s\n", http.errorToString(httpResponseCode).c_str());
  }
  
  http.end();
}
