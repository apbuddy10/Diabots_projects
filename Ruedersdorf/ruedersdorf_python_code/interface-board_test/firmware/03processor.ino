
class Processor {
public:
  virtual bool process() = 0;
  virtual void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) = 0;
};

class ErrorProcessor: public Processor {
  BaseResponse res = {3, 0, 0};
public:
  ErrorProcessor(uint8_t errorClass, uint8_t errorNum) {
    res.errorClass = errorClass;
    res.errorNum = errorNum;
  }
  bool process() {
    return true;
  }
  void writeResponse(void (*write)(const char* data, uint8_t len, uint8_t clientIndex), uint8_t clientIndex) {
    write((const char*)&res, res.length, clientIndex);
  }
};

