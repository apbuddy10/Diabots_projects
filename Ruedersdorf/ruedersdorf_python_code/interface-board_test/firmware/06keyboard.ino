
namespace ProcKeyboard {

  const uint8_t KEY_STATUS = 0x80;

  // Low level key report: up to 6 keys and shift, ctrl etc at once
  struct KeyboardReport {
    uint8_t values[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  };

  class KeyboardClass {
    KeyboardReport report;
    void sendReport();
  public:
    KeyboardClass();
    void press(uint8_t key);
    void release(uint8_t key);
    void update(uint8_t key);
    void releaseAll();
  };

  static const uint8_t reportDescriptor[33] = {
    0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
    0x09, 0x06,                    // USAGE (Keyboard)
    0xa1, 0x01,                    // COLLECTION (Application)
    0x85, 0x02,                    //   REPORT_ID (2)
    0x05, 0x07,                    //   USAGE_PAGE (Keyboard)
    0x19, 0x00,                    //   USAGE_MINIMUM (Reserved (no event indicated))
    0x29, 0x77,                    //   USAGE_MAXIMUM (Keyboard Select)
    0x15, 0x00,                    //   LOGICAL_MINIMUM (0)
    0x25, 0x01,                    //   LOGICAL_MAXIMUM (1)
    0x75, 0x01,                    //   REPORT_SIZE (1)
    0x95, 0x78,                    //   REPORT_COUNT (120)
    0x81, 0x02,                    //   INPUT (Data,Var,Abs)
    0x19, 0xe0,                    //   USAGE_MINIMUM (Keyboard LeftControl)
    0x29, 0xe7,                    //   USAGE_MAXIMUM (Keyboard Right GUI)
    0x95, 0x08,                    //   REPORT_COUNT (8)
    0x81, 0x02,                    //   INPUT (Data,Var,Abs)
    0xc0                           // END_COLLECTION
  };

  KeyboardClass::KeyboardClass(void) {
    static HIDSubDescriptor node(reportDescriptor, sizeof(reportDescriptor));
    HID().AppendDescriptor(&node);
  }

  void KeyboardClass::sendReport() {
    HID().SendReport(2,&report,sizeof(KeyboardReport));
  }

  void KeyboardClass::press(uint8_t key) {
    update(key | KEY_STATUS);
  }

  void KeyboardClass::release(uint8_t key) {
    update(key & ~KEY_STATUS);
  }

  void KeyboardClass::update(uint8_t key) {
    bool value = (key & KEY_STATUS) == KEY_STATUS;
    key = key & ~KEY_STATUS;
    bitWrite(report.values[key/8], key%8, value);
    sendReport();
  }

  void KeyboardClass::releaseAll(void) {
    memset(&report, 0, sizeof(KeyboardReport));
    sendReport();
  }

  KeyboardClass Keyboard;



  #pragma pack(push, 1)

  #pragma pack(pop)
  
  void printCommand(const char* str) {
    Serial.print("Executing ProcKeyboard::");
    Serial.println(str);
  }

  
  class Reset : public Processor { 
    BaseResponse res = {3, 0, 0};
  public:
    Reset(Request req) {
      printCommand("Reset");
    }
    bool process() {
      Keyboard.releaseAll();
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Down : public Processor { 
    KeyboardKey arg;
    BaseResponse res = {3, 0, 0};
  public:
    Down(Request req) {
      printCommand("Down");
      arg = req.arguments().keyboardKey;
    }
    bool process() {
      Keyboard.press(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Up : public Processor { 
    KeyboardKey arg;
    BaseResponse res = {3, 0, 0};
  public:
    Up(Request req) {
      printCommand("Up");
      arg = req.arguments().keyboardKey;
    }
    bool process() {
      Keyboard.release(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Press : public Processor { 
    KeyboardKey arg;
    BaseResponse res = {3, 0, 0};
  public:
    Press(Request req) {
      printCommand("Press");
      arg = req.arguments().keyboardKey;
    }
    bool process() {
      Keyboard.press(arg);
      Keyboard.release(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Update : public Processor { 
    KeyboardKey arg;
    BaseResponse res = {3, 0, 0};
  public:
    Update(Request req) {
      printCommand("Update");
      arg = req.arguments().keyboardKey;
    }
    bool process() {
      Keyboard.update(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Sequence : public Processor { 
    KeyboardSequence arg;
    uint8_t length;
    BaseResponse res = {3, 0, 0};
  public:
    Sequence(Request req) {
      printCommand("Sequence");
      arg = req.arguments().keyboardSequence;
      length = req.length() - 3;
    }
    bool process() {
      for (uint8_t i = 0; i < length; i++) {
        Keyboard.update(arg.sequence[i]);
      }
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };


  Processor* getProcessor(Request req) {
    uint8_t id = req.commandNum();
    if (id == 1) return new Reset(req);
    if (id == 2) return new Down(req);
    if (id == 3) return new Up(req);
    if (id == 4) return new Press(req);
    if (id == 5) return new Update(req);
    if (id == 6) return new Sequence(req);
    return new ErrorProcessor(0, 4);
  }

  void init() { }
}