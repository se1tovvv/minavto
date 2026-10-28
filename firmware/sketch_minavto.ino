#include <WiFi.h>
#include <WebServer.h>

const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WebServer server(80);

const int vibroPin = 19; // Pin connected to the vibration motor

void startVibration() {
  digitalWrite(vibroPin, HIGH); // Turn on the vibration motor
  Serial.println("Vibration started");
  server.send(200, "text/plain", "Vibration started");
}

void stopVibration() {
  digitalWrite(vibroPin, LOW); // Turn off the vibration motor
  Serial.println("Vibration stopped");
  server.send(200, "text/plain", "Vibration stopped");
}

void setup() {
  Serial.begin(115200);
  pinMode(vibroPin, OUTPUT);
  digitalWrite(vibroPin, LOW); // Ensure the motor is off at start

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.print("Connected to WiFi. IP Address: ");
  Serial.println(WiFi.localIP());

  // Define server paths
  server.on("/start_vibration", startVibration);
  server.on("/stop_vibration", stopVibration);

  // Start the server
  server.begin();
}

void loop() {
  // Handle client requests
  server.handleClient();
}
