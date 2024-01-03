
void printIpAddress(const char str[], IPAddress ip) {
  Serial.print(str);
  if (ip[0] < 100) Serial.print(" ");
  if (ip[0] < 10) Serial.print(" ");
  Serial.print(ip[0]);
  Serial.print(".");
  if (ip[1] < 100) Serial.print(" ");
  if (ip[1] < 10) Serial.print(" ");
  Serial.print(ip[1]);
  Serial.print(".");
  if (ip[2] < 100) Serial.print(" ");
  if (ip[2] < 10) Serial.print(" ");
  Serial.print(ip[2]);
  Serial.print(".");
  if (ip[3] < 100) Serial.print(" ");
  if (ip[3] < 10) Serial.print(" ");
Serial.println(ip[3]);
}

void printMacAddress(const char str[], byte mac[6]) {
  Serial.print(str);
  if (mac[0] < 16) Serial.print("0");
  Serial.print(mac[0], HEX);
  Serial.print(":");
  if (mac[1] < 16) Serial.print("0");
  Serial.print(mac[1], HEX);
  Serial.print(":");
  if (mac[2] < 16) Serial.print("0");
  Serial.print(mac[2], HEX);
  Serial.print(":");
  if (mac[3] < 16) Serial.print("0");
  Serial.print(mac[3], HEX);
  Serial.print(":");
  if (mac[4] < 16) Serial.print("0");
  Serial.print(mac[4], HEX);
  Serial.print(":");
  if (mac[5] < 16) Serial.print("0");
  Serial.println(mac[5], HEX);
}

void printError(const char str[] = "", bool newLine = true) {
  Serial.print("Error: ");
  if (newLine) Serial.println(str);
  else Serial.print(str);
}

// Read the device id from pins 22-29
uint8_t getDeviceId() {
  uint8_t value = 0;
  pinMode(22,  INPUT_PULLUP);
  pinMode(23,  INPUT_PULLUP);
  pinMode(24,  INPUT_PULLUP);
  pinMode(25,  INPUT_PULLUP);
  pinMode(26,  INPUT_PULLUP);
  pinMode(27,  INPUT_PULLUP);
  pinMode(28,  INPUT_PULLUP);
  pinMode(29,  INPUT_PULLUP);
  if (!digitalRead(22)) value += 1;
  if (!digitalRead(23)) value += 2;
  if (!digitalRead(24)) value += 4;
  if (!digitalRead(25)) value += 8;
  if (!digitalRead(26)) value += 16;
  if (!digitalRead(27)) value += 32;
  if (!digitalRead(28)) value += 64;
  if (!digitalRead(29)) value += 128;
  return value;
}

// Returns -1, 0, 1 depending on the value sign
template <typename T> int sign(T val) {
    return (T(0) < val) - (val < T(0));
}


struct Time {
  bool isStarted = false;
  unsigned long time = 0;
  void reset();
  void start();
  unsigned long elapsedMicro();
  unsigned long elapsedMs();
  bool haveElapsedMicro(unsigned long micro);
  bool haveElapsedMs(unsigned long ms);
};

void Time::reset() {
  this->isStarted = 0;
  this->time = 0;
}

void Time::start() {
  this->isStarted = true;
  this->time = micros();
}

unsigned long Time::elapsedMicro() {
  if (!this->isStarted) return 0;
  return micros() - this->time;
}

unsigned long Time::elapsedMs() {
  return this->elapsedMicro()/1000;
}

bool Time::haveElapsedMicro(unsigned long micro) {
  return this->elapsedMicro() >= micro;
}

bool Time::haveElapsedMs(unsigned long ms) {
  return this->elapsedMs() >= ms;
}







