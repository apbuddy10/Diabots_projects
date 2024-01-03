// Ethernet Server
EthernetServer server(7658);

class ClientHandler {
  const static uint8_t NUM_CLIENTS;
  static ClientHandler clients[];

  enum Status {idle, readReq, processing, writeRes};

  EthernetClient ethClient;
  uint8_t index;
  Status status;
  uint8_t readIndex;
  Request req;
  Processor* proc;
  
  void printClient(const char str[] = "", bool newLine = true);
  void printClientError(const char str[] = "", bool newLine = true);
  void setErrorResponse(uint8_t errorClass, uint8_t errornum);
  bool isAvailable();
  void doIdle();
  void doReadReq();
  void doProcessing(uint8_t errorClass = 0, uint8_t errorNum = 0);
  void doWriteRes();
  void processClient();
  void processReadReq();
  void processProcessing();
  void processWriteRes();
  void writeData(const char* data, uint8_t len);
  void assignClient(EthernetClient client);
  static void write(const char* data, uint8_t len, uint8_t clientIndex);
  static int8_t findFreeClientHandler();
  static void acceptNewClient();
  static void checkNewClient();
  static Processor* getProcessor(Request req);
public:
  ClientHandler(uint8_t clientIndex);
  static void process();
  static void init();
};

ClientHandler::ClientHandler(uint8_t clientIndex) {
  index = clientIndex;
  status = idle;
  proc = NULL;
}

void ClientHandler::printClient(const char str[], bool newLine) {
  Serial.print("Client");
  Serial.print(index);
  Serial.print(": ");
  if (newLine) Serial.println(str);
  else Serial.print(str);
}

void ClientHandler::printClientError(const char str[], bool newLine) {
  printClient("", false);
  printError(str, newLine);
}

bool ClientHandler::isAvailable() {
  return status == idle;
}

void ClientHandler::assignClient(EthernetClient client) {
  if (status != idle) return printClientError("Assigned with wrong status");
  doReadReq();
  ethClient = client;
  printClient("Connected");
}

void ClientHandler::doIdle() {
  printClient("status = idle");
  if (proc != NULL) delete proc;
  status = idle;
}

void ClientHandler::doReadReq() {
  printClient("status = readReq");
  readIndex = 0;
  status = readReq;  
}

void ClientHandler::processReadReq() {
  if (!ethClient.connected()) {
    printClientError("Dissconected");
    return doProcessing(0, 2);
  }
  if (ethClient.available() == 0) return;

  const uint8_t byte = ethClient.read();
  req.bytes[readIndex] = byte;
  readIndex++;
  if (readIndex == 1 && req.length() > MAX_REQUEST_LENGTH) {
    printClientError("Request length too large");
    return doProcessing(0, 3);
  }
  if (req.length() != readIndex) return;
  printClient("Request: [", false);
  for (uint8_t i = 0; i < req.length(); i++) {
    uint8_t byte = req.bytes[i];
    if (byte < 16) Serial.print(0);
    Serial.print(byte, HEX);
    if (i+1 != req.length()) Serial.print(",");
  }
  Serial.println("]");
  doProcessing();
}

void ClientHandler::doProcessing(uint8_t errorClass, uint8_t errorNum) {
  printClient("status = processing");
  if ((errorClass == 0) && (errorNum == 0)) {
    printClient("executing command [", false);
    Serial.print(req.commandClass());
    Serial.print(",");
    Serial.print(req.commandNum());
    Serial.println("]");
    proc = getProcessor(req);
  } else {
    printClientError("Processing error [", false);
    Serial.print(errorClass);
    Serial.print(", ");
    Serial.print(errorNum);
    Serial.println("]");
    proc = new ErrorProcessor(errorClass, errorNum);
  }
  status = processing;
}

void ClientHandler::processProcessing() {
  if (proc->process()) doWriteRes();
}

void ClientHandler::writeData(const char data[], uint8_t len) {
  ethClient.write(data, len);
  printClient("Response: [", false);
  for (uint8_t i = 0; i < len; i++) {
    uint8_t byte = data[i];
    if (byte < 16) Serial.print(0);
    Serial.print(byte, HEX);
    if (i+1 != len) Serial.print(",");
  }
  Serial.println("]");
}

void ClientHandler::write(const char* data, uint8_t len, uint8_t clientIndex) {
  if (clientIndex >= ClientHandler::NUM_CLIENTS) return;
  clients[clientIndex].writeData(data, len);
}

void ClientHandler::doWriteRes() {
  printClient("status = writeRes");
  if (!ethClient.connected()) {
    printClientError("Could not send Response");
    ethClient.stop();
    return doIdle();
  }
  proc->writeResponse(&ClientHandler::write, index);
  status = writeRes;
}

void ClientHandler::processWriteRes() {
  if (!ethClient.connected()) return doIdle();
  if (ethClient.available() == 0) {
    if (ethClient.availableForWrite() >= 2048) ethClient.stop();
    return;
  }
  printClientError("Received too much data");
  ethClient.read();
}

void ClientHandler::processClient() {
  switch (status) {
    case idle:
      return;
    case readReq:
      return processReadReq();
    case processing:
      return processProcessing();
    case writeRes:
      return processWriteRes(); 
  }
}

int8_t ClientHandler::findFreeClientHandler() {
  for (int8_t i = 0; i < ClientHandler::NUM_CLIENTS; i++) {
    if (clients[i].isAvailable()) {
      return i;
    }
  }
  return -1;
}

void ClientHandler::acceptNewClient() {
  EthernetClient ethClient = server.accept();
  if (!ethClient) return;
  Serial.println("New Client Connected");
  int8_t clientIndex = ClientHandler::findFreeClientHandler();
  Serial.print("Available Client index: ");
  Serial.println(clientIndex);
  if (clientIndex == -1) {
    printError("No Clients available; Closing Connection");
    ethClient.write("\x03\x00\x01", 3);
    ethClient.stop();
    return;
  }
  ClientHandler::clients[clientIndex].assignClient(ethClient);
}

void ClientHandler::process() {
  ClientHandler::acceptNewClient();
  for (uint8_t i = 0; i<ClientHandler::NUM_CLIENTS; i++) {
    ClientHandler::clients[i].processClient();
  }
}

void ClientHandler::init() {
  Serial.println("Init Ethernet");
  uint8_t deviceId = getDeviceId();
  // Setup adresses
  byte mac[6] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, deviceId };
  IPAddress ip = {192, 168, 0, deviceId};
  IPAddress subnet = {255, 255, 255, 0};
  IPAddress gateway = {192, 168, 0, 1};
  IPAddress dns = {0, 0, 0, 0};

  pinMode(9, OUTPUT);
  digitalWrite(9, 1);
  delay(1);
  Serial.println("Resetting W5500 Chip");
  digitalWrite(9, 1);
  delay(1);
  digitalWrite(9, 1);
  delay(100);

  printMacAddress("Mac Address: ", mac);
  printIpAddress("IP  Address: ", ip);
  printIpAddress("SN  Address: ", subnet);
  printIpAddress("GW  Address: ", gateway);
  printIpAddress("DNS Address: ", dns);
  // Set Ethernet Chip Select to pin 10
  Ethernet.init(10); 
  // initialize the Ethernet device
  Ethernet.begin(mac, ip, dns, gateway, subnet);
  // Check that hardware is connected
  while (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet adapter (W5500) is not connected to Arduino");
    Ethernet.begin(mac, ip, dns, gateway, subnet);
    delay(100);    
  }
  // start listening for clients
  server.begin();
  delay(100);
}

Processor* ClientHandler::getProcessor(Request req) {
  uint8_t id = req.commandClass();
  if (id == 0) return ProcGeneral::getProcessor(req);
  if (id == 1) return ProcMouse::getProcessor(req);
  if (id == 2) return ProcKeyboard::getProcessor(req);
  return new ErrorProcessor(0, 4);
}

const uint8_t ClientHandler::NUM_CLIENTS = 6;
ClientHandler ClientHandler::clients[ClientHandler::NUM_CLIENTS] = {ClientHandler(0), ClientHandler(1), ClientHandler(2), ClientHandler(3), ClientHandler(4), ClientHandler(5)};




