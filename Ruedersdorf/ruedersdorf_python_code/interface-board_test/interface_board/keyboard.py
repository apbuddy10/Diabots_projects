
from . connection import connection
from . consts import commands
from typing import List, Type, Union
from struct import pack
from enum import IntEnum


class KeyCodes(IntEnum):
  # Available KeyCodes based on the US Keyboard
  RESERVED = 0x00
  ERROR_ROLL_OVER = 0X01
  POST_FAIL = 0X02
  ERROR_UNDEFINED = 0X03
  KEY_A = 0X04
  KEY_B = 0X05
  KEY_C = 0X06
  KEY_D = 0X07
  KEY_E = 0X08
  KEY_F = 0X09
  KEY_G = 0X0A
  KEY_H = 0X0B
  KEY_I = 0X0C
  KEY_J = 0X0D
  KEY_K = 0X0E
  KEY_L = 0X0F
  KEY_M = 0X10
  KEY_N = 0X11
  KEY_O = 0X12
  KEY_P = 0X13
  KEY_Q = 0X14
  KEY_R = 0X15
  KEY_S = 0X16
  KEY_T = 0X17
  KEY_U = 0X18
  KEY_V = 0X19
  KEY_W = 0X1A
  KEY_X = 0X1B
  KEY_Y = 0X1C
  KEY_Z = 0X1D
  KEY1 = 0X1E
  KEY2 = 0X1F
  KEY3 = 0X20
  KEY4 = 0X21
  KEY5 = 0X22
  KEY6 = 0X23
  KEY7 = 0X24
  KEY8 = 0X25
  KEY9 = 0X26
  KEY0 = 0X27
  KEY_ENTER = 0X28
  KEY_ESCAPE = 0X29
  KEY_BACKSPACE = 0X2A
  KEY_TAB = 0X2B
  KEY_SPACE = 0X2C
  KEY_MINUS = 0X2D
  KEY_EQUALS = 0X2E
  KEY_SQUARE_BRACKET_OPEN = 0X2F
  KEY_SQUARE_BRACKET_CLOSE = 0X30
  KEY_BACKSLASH = 0X31
  KEY_NON_US_HASH = 0X32
  KEY_SEMICOLON = 0X33
  KEY_QUOTATION_MARK = 0X34
  KEY_GRAVE_ACCENT = 0X35
  KEY_COMMA = 0X36
  KEY_DOT = 0X37
  KEY_SLASH = 0X38
  KEY_CAPS_LOCK = 0X39
  KEY_F1 = 0X3A
  KEY_F2 = 0X3B
  KEY_F3 = 0X3C
  KEY_F4 = 0X3D
  KEY_F5 = 0X3E
  KEY_F6 = 0X3F
  KEY_F7 = 0X40
  KEY_F8 = 0X41
  KEY_F9 = 0X42
  KEY_F10 = 0X43
  KEY_F11 = 0X44
  KEY_F12 = 0X45
  KEY_PRINT_SCREEN = 0X46
  KEY_SCROLL_LOCK = 0X47
  KEY_PAUSE = 0X48
  KEY_INSERT = 0X49
  KEY_HOME = 0X4A
  KEY_PAGE_UP = 0X4B
  KEY_DELETE = 0X4C
  KEY_END = 0X4D
  KEY_PAGE_DOWN = 0X4E
  KEY_RIGHT_ARROW = 0X4F
  KEY_LEFT_ARROW = 0X50
  KEY_DOWN_ARROW = 0X51
  KEY_UP_ARROW = 0X52
  KEY_NUM_LOCK = 0X53
  KEYPAD_DIVIDE = 0X54
  KEYPAD_MULTIPLY = 0X55
  KEYPAD_SUBTRACT = 0X56
  KEYPAD_ADD = 0X57
  KEYPAD_ENTER = 0X58
  KEYPAD1 = 0X59
  KEYPAD2 = 0X5A
  KEYPAD3 = 0X5B
  KEYPAD4 = 0X5C
  KEYPAD5 = 0X5D
  KEYPAD6 = 0X5E
  KEYPAD7 = 0X5F
  KEYPAD8 = 0X60
  KEYPAD9 = 0X61
  KEYPAD0 = 0X62
  KEYPAD_DOT = 0X63
  KEY_NON_US_BACKSLASH = 0X64
  KEY_APPLICATION = 0X65
  KEY_POWER = 0X66
  KEYPAD_EQUALS = 0X67
  KEY_F13 = 0X68
  KEY_F14 = 0X69
  KEY_F15 = 0X6A
  KEY_F16 = 0X6B
  KEY_F17 = 0X6C
  KEY_F18 = 0X6D
  KEY_F19 = 0X6E
  KEY_F20 = 0X6F
  KEY_F21 = 0X70
  KEY_F22 = 0X71
  KEY_F23 = 0X72
  KEY_F24 = 0X73
  KEY_EXECUTE = 0X74
  KEY_HELP = 0X75
  KEY_MENU = 0X76
  KEY_SELECT = 0X77
  KEY_LEFT_CONTROL = 0X78
  KEY_LEFT_SHIFT = 0X79
  KEY_LEFT_ALT = 0X7A
  KEY_LEFT_GUI = 0X7B
  KEY_RIGHT_CONTROL = 0X7C
  KEY_RIGHT_SHIFT = 0X7D
  KEY_RIGHT_ALT = 0X7E
  KEY_RIGHT_GUI = 0X7F


KeyDown: Type[KeyCodes] = IntEnum("KeyDown", {data.name: data.value + 0x80 for data in KeyCodes})


class Keyboard:
  PRESSED: int = 0x80
  KEY_CODES: Type[KeyCodes] = KeyCodes
  KEY_DOWN: Type[KeyCodes] = KeyDown
  KEY_UP: Type[KeyCodes] = KeyCodes
  _conn: connection

  def __init__(self, conn: connection) -> None:
    self._conn = conn

  # releases all the keys
  async def reset(self) -> None:
    await self._conn.request(commands.keyboard.reset, None, 0)

  # presses the key down specified with key
  async def down(self, key: KeyCodes) -> None:
    await self._conn.request(commands.keyboard.down, 2, 0, pack("<B", key))

  # presses the key up specified with key
  async def up(self, key: KeyCodes) -> None:
    await self._conn.request(commands.keyboard.up, 2, 0, pack("<B", key))

  # presses and release key specified with key
  async def press(self, key: KeyCodes) -> None:
    await self._conn.request(commands.keyboard.press, 2, 0, pack("<B", key))

  # presses a key based on the highest bit in the byte (>= 0x80 press the key)
  async def update(self, key: KeyCodes) -> None:
    await self._conn.request(commands.keyboard.update, 2, 0, pack("<B", key))

  # Sends multiple key updates like calling update multiple times
  async def sequence(self, keys: List[KeyCodes]) -> None:
    await self._conn.request(commands.keyboard.sequence, 2, 0, bytes(keys))
