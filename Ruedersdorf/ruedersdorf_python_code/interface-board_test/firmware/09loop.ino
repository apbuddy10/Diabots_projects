
EthernetLinkStatus linkStatus = Unknown;
void checkLinkStatus() {
  EthernetLinkStatus newStatus =  Ethernet.linkStatus();
  if (newStatus != linkStatus) {
    if (newStatus == LinkON) {
      Serial.println("LinkStatus: Connected");
    } else if (newStatus == LinkOFF) {
      Serial.println("LinkStatus: Disconnected");
    } else {
      Serial.println("LinkStatus: Unknown");
    }
    linkStatus = newStatus;
  }
}

void loop() {

  checkLinkStatus();
  ClientHandler::process();
  delay(10);
}
