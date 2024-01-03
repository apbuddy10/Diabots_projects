
namespace ProcGeneral {
  #pragma pack(push, 1)
  struct ResponseFirmwareVersion {
    uint8_t length;
    uint8_t errorClass;
    uint8_t errorNum;
    uint16_t version;
  };
  #pragma pack(pop)

  void printCommand(const char* str) {
    Serial.print("Executing ProcGeneral::");
    Serial.println(str);
  }
  
  class FirmwareVersion: public Processor { 
    ResponseFirmwareVersion res = {5, 0, 0, FIRMWARE_VERSION};
  public:
    FirmwareVersion(Request req) {
      printCommand("FirmwareVersion");
    }
    bool process() {
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  Processor* getProcessor(Request req) {
    uint8_t id = req.commandNum();
    if (id == 1) return new FirmwareVersion(req);
    return new ErrorProcessor(0, 4);
  }

  void init() { }
}