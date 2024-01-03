import asyncio
import struct
import typing
from .consts import errors


def get_error(error_class: int, error: int, arguments: bytes) -> None:
  class_dict = errors.get(error_class)
  if (class_dict == None):
    raise LookupError("Undefined Error: " + str(error_class) + ":" + str(error))
  error_str = class_dict.get(error)
  if (error_str == None):
    raise LookupError("Undefined Error: " + str(error_class) + ":" + str(error))
  if (type(error_str) is str):
    raise BaseException(error_str)
  if (isinstance(error_str, BaseException)):
    raise error_str
  if (callable(error_str)):
    raise error_str(error_class, error, arguments)
  raise TypeError("Wrong Type in Error Dict: " + str(error_class) + ":" + str(error))


async def write(writer: asyncio.StreamWriter, command_class: int, command: int, arguments: bytes) -> None:
  length = 3 + len(arguments)
  header = struct.pack("<BBB", length, command_class, command)
  data = header + arguments
  writer.write(data)
  await writer.drain()


async def read(reader: asyncio.StreamReader, result_length: typing.Union[int, None]) -> bytes:
  data = await reader.read()
  if (len(data) < 3):
    raise EOFError("Received not enough data")
  length, error_class, error = typing.cast(tuple[int, int, int], struct.unpack("<BBB", data[:3]))
  arguments = data[3:]
  if (len(data) != length):
    raise EOFError("Received length doesn't match packet length")
  if (error_class != 0 or error != 0):
    raise get_error(error_class, error, arguments)
  if (result_length != None and len(arguments) != result_length):
    raise EOFError("Received length doesn't match expected length of " + str(result_length))
  return arguments


class connection:
  _ip: str
  _timeout: float

  def __init__(self, ip: str, timeout: float):
    self._ip = ip
    self._timeout = timeout

  async def request(self, command: tuple[int, int], timeout: typing.Union[float, None], result_length: typing.Union[int, None] = None, arguments: bytes = bytes([])) -> bytes:
    writer = None
    try:
      async with asyncio.timeout(self._timeout):
        reader, writer = await asyncio.open_connection(self._ip, 7658)
    except TimeoutError:
      if (writer != None):
        writer.close()
      raise TimeoutError("Board doesn't respond")
    try:
      async with asyncio.timeout(timeout):
        await write(writer, command[0], command[1], arguments)
        ret = await read(reader, result_length)
        writer.close()
        await writer.wait_closed()
        return ret
    except TimeoutError:
      if (writer != None):
        writer.close()
      raise TimeoutError("Task did not finish within timeout")
