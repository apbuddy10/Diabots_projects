void initSerial() {
  delay(300);
  // Open serial communications and wait for port to open
  Serial.begin(460800);
  while (!Serial) {}
}

void setup() {
  initSerial();

  Serial.println("+--------------------------------+");
  Serial.println("|      Initialization Start      |");
  Serial.println("+--------------------------------+");

  ProcMouse::init();
  ProcKeyboard::init();
  ProcGeneral::init();
  ClientHandler::init();

  Serial.println("+--------------------------------+");
  Serial.println("|      Initialization Done       |");
  Serial.println("+--------------------------------+");
}