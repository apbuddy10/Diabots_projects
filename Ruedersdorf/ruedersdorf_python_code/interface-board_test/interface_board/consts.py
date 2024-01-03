import typing


class classes:
  general = 0
  mouse = 1
  keyboard = 2


class CommandGeneral:
  firmware_version = 1


class CommandMouse:
  reset = 1
  press = 2
  release = 3
  moveRel = 4
  moveWheel = 5
  click = 6
  dblClick = 7
  moveAbs = 8
  moveAbsClick = 9
  moveAbsDblClick = 10
  movePercent = 11
  movePercentClick = 12
  movePercentDblClick = 13


class CommandKeyboard:
  reset = 1
  down = 2
  up = 3
  press = 4
  update = 5
  sequence = 6


class commands:
  general = CommandGeneral
  mouse = CommandMouse
  keyboard = CommandKeyboard


errors: dict[int, dict[int, typing.Union[str, BaseException, typing.Callable[[int, int, bytes], BaseException]]]] = {
  classes.general: {
    1: "Connection refused because of too many connections",
    2: "Disconnected while still processing",
    3: "Request length too large",
    4: "Unknown command",
  }
}


for class_str in dir(commands):
  if (class_str.startswith("__")):
    continue
  class_number = getattr(classes, class_str)
  class_dict = getattr(commands, class_str)
  for command in dir(class_dict):
    if (command.startswith("__")):
      continue
    setattr(class_dict, command, (class_number, getattr(class_dict, command)))
