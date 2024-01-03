
namespace ProcMouse {


  #pragma pack(push, 1)
  struct MouseReportRel {
    uint8_t buttons;
    int16_t x;
    int16_t y;
    int16_t wheel;
  };
  struct MouseReportAbs {
    uint16_t x;
    uint16_t y;
  };
  #pragma pack(pop)

  class MouseClass {
    uint8_t buttonState;
    void sendReportAbs(uint16_t x = 0, uint16_t y = 0);
    void sendReportRel(int16_t x = 0, int16_t y = 0, int16_t wheel = 0);
  public:
    MouseClass(void);
    void press(uint8_t buttons);
    void release(uint8_t buttons);
    void releaseAll();
    void click(uint8_t buttons);
    void moveRel(int16_t x, int16_t y);
    void moveAbs(uint16_t x, uint16_t y);
    void scrollRel(int16_t steps);
    void zero();
    void reset();
  };

  static const uint8_t reportDescriptorRel[56] = {
    0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
    0x09, 0x02,                    // USAGE (Mouse)
    0xa1, 0x01,                    // COLLECTION (Application)
    0x09, 0x01,                    //   USAGE (Pointer)
    0xa1, 0x00,                    //   COLLECTION (Physical)
    0x85, 0x01,                    //     REPORT_ID (1)
    0x05, 0x09,                    //     USAGE_PAGE (Button)
    0x19, 0x01,                    //     USAGE_MINIMUM (Button 1)
    0x29, 0x03,                    //     USAGE_MAXIMUM (Button 3)
    0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
    0x25, 0x01,                    //     LOGICAL_MAXIMUM (1)
    0x95, 0x03,                    //     REPORT_COUNT (3)
    0x75, 0x01,                    //     REPORT_SIZE (1)
    0x81, 0x02,                    //     INPUT (Data,Var,Abs)
    0x95, 0x01,                    //     REPORT_COUNT (1)
    0x75, 0x05,                    //     REPORT_SIZE (5)
    0x81, 0x03,                    //     INPUT (Cnst,Var,Abs)
    0x05, 0x01,                    //     USAGE_PAGE (Generic Desktop)
    0x09, 0x30,                    //     USAGE (X)
    0x09, 0x31,                    //     USAGE (Y)
    0x09, 0x38,                    //     USAGE (Wheel)
    0x16, 0x00, 0x80,              //     LOGICAL_MINIMUM (-32768)
    0x26, 0xff, 0x7f,              //     LOGICAL_MAXIMUM (32767)
    0x75, 0x10,                    //     REPORT_SIZE (16)
    0x95, 0x03,                    //     REPORT_COUNT (3)
    0x81, 0x06,                    //     INPUT (Data,Var,Rel)
    0xc0,                          //   END_COLLECTION
    0xc0                           // END_COLLECTION
  };

  static const uint8_t reportDescriptorAbs[40] = {
    0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
    0x09, 0x02,                    // USAGE (Mouse)
    0xa1, 0x01,                    // COLLECTION (Application)
    0x09, 0x01,                    //   USAGE (Pointer)
    0xa1, 0x00,                    //   COLLECTION (Physical)
    0x85, 0x03,                    //     REPORT_ID (3)
    0x05, 0x01,                    //     USAGE_PAGE (Generic Desktop)
    0x09, 0x30,                    //     USAGE (X)
    0x09, 0x31,                    //     USAGE (Y)
    0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
    0x27, 0xff, 0xff, 0x00, 0x00,  //     LOGICAL_MAXIMUM (65535)
    0x35, 0x01,                    //     PHYSICAL_MINIMUM (1)
    0x47, 0xff, 0xff, 0x00, 0x00,  //     PHYSICAL_MAXIMUM (65535)
    0x75, 0x10,                    //     REPORT_SIZE (16)
    0x95, 0x02,                    //     REPORT_COUNT (2)
    0x81, 0x02,                    //     INPUT (Data,Var,Abs)
    0xc0,                          //   END_COLLECTION
    0xc0                           // END_COLLECTION
  };


  MouseClass::MouseClass(void) {
    static HIDSubDescriptor nodeRel(reportDescriptorRel, sizeof(reportDescriptorRel));
    HID().AppendDescriptor(&nodeRel);
    static HIDSubDescriptor nodeAbs(reportDescriptorAbs, sizeof(reportDescriptorAbs));
    HID().AppendDescriptor(&nodeAbs);
  }

  void MouseClass::sendReportRel(int16_t x, int16_t y, int16_t wheel) {
    MouseReportRel report = {buttonState, x, y, wheel};
    HID().SendReport(1, &report, sizeof(report));
  }

  void MouseClass::sendReportAbs(uint16_t x, uint16_t y) {
    MouseReportAbs report = {x, y};
    HID().SendReport(3, &report, sizeof(report));
  }

  void MouseClass::press(uint8_t buttons)  {
    buttonState |= buttons;
    sendReportRel();
  }

  void MouseClass::release(uint8_t buttons) {
    buttonState &= ~buttons;
    sendReportRel();
  }

  void MouseClass::click(uint8_t buttons) {
    press(buttons);
    release(buttons);
  }

  void MouseClass::releaseAll() {
    release(0xFF);
  }

  void MouseClass::moveRel(int16_t x, int16_t y) {
    sendReportRel(x, y);
  }

  void MouseClass::moveAbs(uint16_t x, uint16_t y) {
    sendReportAbs(x, y);
  }

  void MouseClass::scrollRel(int16_t steps) {
    sendReportRel(0, 0, steps);
  }

  void MouseClass::zero() {
    moveAbs(0, 0);
  }

  void MouseClass::reset() {
    releaseAll();
    zero();
  }
  MouseClass Mouse;


  void printCommand(const char* str) {
    Serial.print("Executing ProcMouse::");
    Serial.println(str);
  }
  
  class Reset : public Processor { 
    BaseResponse res = {3, 0, 0};
  public:
    Reset(Request req) {
      printCommand("Reset");
    }
    bool process() {
      Mouse.reset();
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Press : public Processor { 
    MouseButtonArg arg;
    BaseResponse res = {3, 0, 0};
  public:
    Press(Request req) {
      printCommand("Press");
      arg = req.arguments().mouseButtonArg;
    }
    bool process() {
      Mouse.press(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Release : public Processor { 
    MouseButtonArg arg;
    BaseResponse res = {3, 0, 0};
  public:
    Release(Request req) {
      printCommand("Release");
      arg = req.arguments().mouseButtonArg;
    }
    bool process() {
      Mouse.release(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class MoveRel : public Processor { 
    MousePosition arg;
    BaseResponse res = {3, 0, 0};
  public:
    MoveRel(Request req) {
      printCommand("MoveRel");
      arg = req.arguments().mousePosition;
    }
    bool process() {
      Mouse.moveRel(arg.x, arg.y);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class MoveWheel : public Processor { 
    MouseWheelPosition arg;
    BaseResponse res = {3, 0, 0};
  public:
    MoveWheel(Request req) {
      printCommand("MoveWheel");
      arg = req.arguments().mouseWheelPosition;
    }
    bool process() {
      Mouse.scrollRel(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class Click : public Processor { 
    MouseButtonArg arg;
    BaseResponse res = {3, 0, 0};
  public:
    Click(Request req) {
      printCommand("Click");
      arg = req.arguments().mouseButtonArg;
    }
    bool process() {
      Mouse.releaseAll();
      Mouse.click(arg);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class DblClick : public Processor { 
    MouseDblClick arg;
    Time time;
    BaseResponse res = {3, 0, 0};
  public:
    DblClick(Request req) {
      printCommand("DblClick");
      arg = req.arguments().mouseDblClick;
      time.reset();
    }
    bool process() {
      if (!time.isStarted) {
        Mouse.releaseAll();
        Mouse.click(arg.buttons);
        time.start();
        return false;
      }
      if (time.haveElapsedMs(arg.delay)) {
        Mouse.click(arg.buttons);
        return true;
      }
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class MoveAbs : public Processor { 
    MousePosition arg;
    BaseResponse res = {3, 0, 0};
  public:
    MoveAbs(Request req) {
      printCommand("MoveAbs");
      arg = req.arguments().mousePosition;
    }
    bool process() {
      Mouse.zero();
      Mouse.moveRel(arg.x, arg.y);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class MoveClick : public Processor { 
    MouseMoveClick arg;
    BaseResponse res = {3, 0, 0};
  public:
    MoveClick(Request req) {
      printCommand("MoveClick");
      arg = req.arguments().mouseMoveClick;
    }
    bool process() {
      Mouse.reset();
      Mouse.moveRel(arg.position.x, arg.position.y);
      Mouse.click(arg.buttons);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class MoveDblClick : public Processor { 
    MouseMoveDblClick arg;
    Time time;
    BaseResponse res = {3, 0, 0};
  public:
    MoveDblClick(Request req) {
      printCommand("MoveDblClick");
      arg = req.arguments().mouseMoveDblClick;
      time.reset();
    }
    bool process() {
      if (!time.isStarted) {
        Mouse.reset();
        Mouse.moveRel(arg.position.x, arg.position.y);
        Mouse.click(arg.dblArg.buttons);
        time.start();
        return false;
      }
      if (time.haveElapsedMs(arg.dblArg.delay)) {
        Mouse.click(arg.dblArg.buttons);
        return true;
      }
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class MovePercent : public Processor { 
    MousePositionAbs arg;
    BaseResponse res = {3, 0, 0};
  public:
    MovePercent(Request req) {
      printCommand("MovePercent");
      arg = req.arguments().mousePositionAbs;
    }
    bool process() {
      Mouse.moveAbs(arg.x, arg.y);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

    class MovePercentClick : public Processor { 
    MouseMoveAbsClick arg;
    BaseResponse res = {3, 0, 0};
  public:
    MovePercentClick(Request req) {
      printCommand("MovePercentClick");
      arg = req.arguments().mouseMoveAbsClick;
    }
    bool process() {
      Mouse.releaseAll();
      Mouse.moveAbs(arg.position.x, arg.position.y);
      Mouse.click(arg.buttons);
      return true;
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  class MovePercentDblClick : public Processor { 
    MouseMoveAbsDblClick arg;
    Time time;
    BaseResponse res = {3, 0, 0};
  public:
    MovePercentDblClick(Request req) {
      printCommand("MovePercentDblClick");
      arg = req.arguments().mouseMoveAbsDblClick;
      time.reset();
    }
    bool process() {
      if (!time.isStarted) {
        Mouse.releaseAll();
        Mouse.moveAbs(arg.position.x, arg.position.y);
        Mouse.click(arg.dblArg.buttons);
        time.start();
        return false;
      }
      if (time.haveElapsedMs(arg.dblArg.delay)) {
        Mouse.click(arg.dblArg.buttons);
        return true;
      }
    }
    void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
      write((const char*)&res, res.length, clientIndex);
    }
  };

  Processor* getProcessor(Request req) {
    uint8_t id = req.commandNum();
    if (id == 1) return new Reset(req);
    if (id == 2) return new Press(req);
    if (id == 3) return new Release(req);
    if (id == 4) return new MoveRel(req);
    if (id == 5) return new MoveWheel(req);
    if (id == 6) return new Click(req);
    if (id == 7) return new DblClick(req);
    if (id == 8) return new MoveAbs(req);
    if (id == 9) return new MoveClick(req);
    if (id == 10) return new MoveDblClick(req);
    if (id == 11) return new MovePercent(req);
    if (id == 12) return new MovePercent(req);
    if (id == 13) return new MovePercent(req);
    return new ErrorProcessor(0, 4);
  }

  void init() { }
}