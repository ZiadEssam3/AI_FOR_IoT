// Command receiver from Python to control LEDs
String cmd;

// Define LED pins
const int LED_PINS[] = {18, 2, 19, 4, 5};
const int NUM_LEDS = sizeof(LED_PINS) / sizeof(LED_PINS[0]);

void setup() {
  Serial.begin(115200);

  // Initialize LED pins
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }
}

// Function to set LED states using an array
void setLEDStates(const bool states[]) {
  for (int i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], states[i] ? HIGH : LOW);
  }
}

void loop() {
  if (Serial.available() > 0) {
    cmd = Serial.readStringUntil('\r');
    cmd.trim();  // Remove newline or extra whitespace

    if (cmd == "One") {
      bool states[] = {1, 0, 0, 0, 0};
      setLEDStates(states);
    } 
    else if (cmd == "Two") {
      bool states[] = {1, 1, 0, 0, 0};
      setLEDStates(states);
    } 
    else if (cmd == "Three") {
      bool states[] = {1, 1, 1, 0, 0};
      setLEDStates(states);
    } 
    else if (cmd == "Four") {
      bool states[] = {1, 1, 1, 1, 0};
      setLEDStates(states);
    } 
    else if (cmd == "Five") {
      bool states[] = {1, 1, 1, 1, 1};
      setLEDStates(states);
    } 
    else if (cmd == "Pinky") {
      bool states[] = {0, 0, 0, 1, 0};
      setLEDStates(states);
    } 
    else if (cmd == "Thumb") {
      bool states[] = {0, 0, 0, 0, 1};
      setLEDStates(states);
    } 
    else if (cmd == "Inside") {
      bool states[] = {0, 1, 1, 0, 0};
      setLEDStates(states);
    } 
    else if (cmd == "Outside") {
      bool states[] = {1, 0, 0, 1, 0};
      setLEDStates(states);
    } 
    else if (cmd == "UnKnown") {
      bool states[] = {0, 0, 0, 0, 0};
      setLEDStates(states);
    }
    
  }
}
