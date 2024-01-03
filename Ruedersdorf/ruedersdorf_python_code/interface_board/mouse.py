
from . connection import connection
from . consts import commands
from enum import IntFlag
from typing import Type
from struct import pack


class Button(IntFlag):
  LEFT = 0b001
  MIDDLE = 0b010
  LEFT_Middle = 0b011
  RIGHT = 0b100
  LEFT_RIGHT = 0b101
  MIDDLE_RIGHT = 0b110
  ALL = 0b111


# X and Y coordinated depend on mouse sensitivity and acceleration
class Mouse:
  BUTTON: Type[Button] = Button
  _conn: connection

  def __init__(self, conn: connection) -> None:
    self._conn = conn

  # releases all the buttons and moves the mouse to the top left corner (on single monitor system)
  async def reset(self) -> None:
    await self._conn.request(commands.mouse.reset, 2, 0)

  # presses the Buttons specified with buttons
  async def press(self, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.press, 2, 0, pack("<B", buttons))

  # release the Buttons specified with buttons
  async def release(self, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.release, 2, 0, pack("<B", buttons))

  # move the courser relative from the current location
  async def moveRel(self, x: int, y: int) -> None:
    await self._conn.request(commands.mouse.moveRel, 2, 0, pack("<hh", x, y))

  # move the mouse wheel number of steps (negative values are scrolling down)
  async def moveWheel(self, wheel: int) -> None:
    await self._conn.request(commands.mouse.moveWheel, 2, 0, pack("<h", wheel))

  # perform an click at the current location
  async def click(self, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.click, 2, 0, pack("<B", buttons))

  # perform two consecutive clicks at the current location
  async def dblClick(self, delayMs: int = 100, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.dblClick, 2, 0, pack("<HB", delayMs, buttons))

  # move mouse in to the corner and then move this amount
  async def moveAbs(self, x: int, y: int) -> None:
    await self._conn.request(commands.mouse.moveAbs, 2, 0, pack("<hh", x, y))

  # perform an click at the specified location in pixel
  async def moveClick(self, x: int, y: int, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.moveAbsClick, 2, 0, pack("<hhB", x, y, buttons))

  # perform two consecutive clicks at the specified location in pixel
  async def moveDblClick(self, x: int, y: int, delayMs: int = 100, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.moveAbsDblClick, 2, 0, pack("<hhHB", x, y, delayMs, buttons))

  # Move to the specified Location in % (0.0 - 1.0) of the main screen
  async def movePercent(self, x: float, y: float) -> None:
    await self._conn.request(commands.mouse.movePercent, 2, 0, pack("<HH", int(x * 65535), int(y * 65535)))

  # perform an click at the specified location in %
  async def movePercentClick(self, x: float, y: float, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.movePercentClick, 2, 0, pack("<HHB", int(x * 65535), int(y * 65535), buttons))

  # perform two consecutive clicks at the specified location in %
  async def movePercentDblClick(self, x: float, y: float, delayMs: int = 100, buttons: Button = Button.LEFT) -> None:
    await self._conn.request(commands.mouse.movePercentDblClick, 2, 0, pack("<HHHB", int(x * 65535), int(y * 65535), delayMs, buttons))
