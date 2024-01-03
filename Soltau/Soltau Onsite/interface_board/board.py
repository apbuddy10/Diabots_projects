from . connection import connection
from . consts import commands
from . mouse import Mouse
from . keyboard import Keyboard
import struct


class Board:
  firmware_version = 2
  mouse: Mouse
  keyboard: Keyboard

  def __init__(self, ip: str, connection_timeout: float = 1.0):
    self._conn = connection(ip, connection_timeout)
    self.mouse = Mouse(self._conn)
    self.keyboard = Keyboard(self._conn)

  async def check_connection(self) -> None:
    result = await self._conn.request(commands.general.firmware_version, 2, 2)
    (version,) = struct.unpack("<H", result)
    if (version != Board.firmware_version):
      raise ValueError("Firmware version of board is not Supported")


def board_by_id(id: int) -> Board:
  return Board("192.168.0." + str(id))
