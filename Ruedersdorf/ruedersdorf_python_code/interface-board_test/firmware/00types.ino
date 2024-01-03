
#pragma pack(push, 1)

const uint8_t MAX_REQUEST_ARG_LENGTH = 20;

typedef int16_t MouseWheelPosition;
typedef uint8_t MouseButtonArg;
struct MousePosition {
  int16_t x;
  int16_t y;
};
struct MouseDblClick {
  uint16_t delay;
  MouseButtonArg buttons;
};
struct MouseMoveClick {
  MousePosition position;
  MouseButtonArg buttons;
};
struct MouseMoveDblClick {
  MousePosition position;
  MouseDblClick dblArg;
};
struct MousePositionAbs {
  uint16_t x;
  uint16_t y;
};
struct MouseMoveAbsClick {
  MousePositionAbs position;
  MouseButtonArg buttons;
};
struct MouseMoveAbsDblClick {
  MousePositionAbs position;
  MouseDblClick dblArg;
};

typedef uint8_t KeyboardKey;
struct KeyboardSequence {
  uint8_t sequence[MAX_REQUEST_ARG_LENGTH];
};

union RequestArguments {
  uint8_t bytes[MAX_REQUEST_ARG_LENGTH];
  MouseButtonArg mouseButtonArg;
  MousePosition mousePosition;
  MouseWheelPosition mouseWheelPosition;
  MouseDblClick mouseDblClick;
  MouseMoveClick mouseMoveClick;
  MouseMoveDblClick mouseMoveDblClick;
  MousePositionAbs mousePositionAbs;
  MouseMoveAbsClick mouseMoveAbsClick;
  MouseMoveAbsDblClick mouseMoveAbsDblClick;
  KeyboardKey keyboardKey;
  KeyboardSequence keyboardSequence;
};

struct RequestData {
  uint8_t length;
  uint8_t commandClass;
  uint8_t commandNum;
  RequestArguments arguments;
};

const uint8_t MAX_REQUEST_LENGTH = MAX_REQUEST_ARG_LENGTH + 3;

union Request {
  uint8_t bytes[MAX_REQUEST_LENGTH];
  RequestData data;
  uint8_t length();
  uint8_t commandClass();
  uint8_t commandNum();
  RequestArguments arguments();
};

uint8_t Request::length() {
  return data.length;
}

uint8_t Request::commandClass() {
  return data.commandClass;
}

uint8_t Request::commandNum() {
  return data.commandNum;
}

RequestArguments Request::arguments() {
  return data.arguments;
}

struct BaseResponse {
  uint8_t length;
  uint8_t errorClass;
  uint8_t errorNum;
};


#pragma pack(pop)