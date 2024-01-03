#!/usr/bin/env python

import asyncio
import json
import typing


# Error Type when a Malformed packet is Received
class Q400PacketError(Exception):
    def __init__(self, message="Malformed packet received"):
        super().__init__(message)


# Error type when the Connection to Vision Q.400 is lost
class Q400ConnectionError(Exception):
    def __init__(self, message="Connection Lost"):
        super().__init__(message)


# The Type of the Handler async Function
Handler = typing.Callable[[dict, str], typing.Awaitable[typing.Union[bool, None]]]


# Class for keeping the Connection to Q400 Upright and Parsing th Packages
class Q400Connection:
    # Constructor initializes attributes.
    def __init__(self, host: str = "127.0.0.1", port: int = 9094, version: int = 1, prettyJson: bool = False):
        self._host: str = host
        self._port: int = port
        self._version: int = version
        self._ending: bool = False
        self._prettyJson: bool = prettyJson
        self._writer: asyncio.StreamWriter = None
        self._task: asyncio.Task = asyncio.create_task(self._readerTask())
        self._future: asyncio.Future = asyncio.get_running_loop().create_future()
        self._handlers: typing.Set[Handler] = set()

    # The Task which continuously reads from the Connection
    async def _readerTask(self):
        reader: asyncio.StreamReader = None
        self._writer: asyncio.StreamWriter = None       
        while not self._ending:
            if not self._future.done():
                # Try to Connect to the Server, when no Connection is established
                try:
                    reader, self._writer = await asyncio.open_connection(self._host, self._port, limit=1000000000000)
                    self._writer.write(f"\x02{{\"version\":{self._version}}}\x03".encode("UTF-8"))
                    self._future.set_result(True)
                except Exception as error:
                    continue

            try:
                # Try to Read from the TCP Connection
                data: bytes = await reader.readuntil(b"\x03")
                data, s = self._parsePacket(data)
            except:
                if not self._writer.is_closing():
                    self._writer.close()
                if not self._future.done():
                    self._future.set_exception()
                self._future = asyncio.get_running_loop().create_future()
                if not self._writer.is_closing():
                    await self._writer.wait_closed()
                self._writer = None
                reader = None
                continue

            try:
                # Try to call the Handlers for this Data packet
                await self._processPacket(data, s)
            except Exception as error:
                continue

    # Decode the String to a Valid Dict Packet
    def _parsePacket(self, data: bytes) -> [dict, str]:
        try:
            s = data.decode("UTF-8")
            if s.startswith("\x02") and s.endswith("\x03"):
                s = s[1:-1]
                data = json.loads(s)
                if not isinstance(data, dict):
                    # raise Q400PacketError()
                    return None, None
                return data, s
            else:
                # raise Q400PacketError()
                return None, None
        except:
            return None, None

    # Call all handlers relevant to the given Packet
    async def _processPacket(self, data: dict, s: str):
        if data.pop("version", None) != self._version:
            raise Q400PacketError()
        for handler in self._handlers.copy():
            ret = await handler(data, s)
            if (ret is not None) and ret:
                self.removeHandler(handler)

    # Adds a Handler which is called for every Packet
    def addHandler(self, handler: Handler):
        self._handlers.add(handler)

    # Removes a Handler so it does not get calls anymore
    def removeHandler(self, handler: Handler):
        self._handlers.discard(handler)

    # Registers a Handler to receive the next Message and returns the Message when one is received
    async def getNextMessage(self) -> [dict, str]:
        fut = asyncio.get_running_loop().create_future()
        async def handler(data: dict, s: str):
            fut.set_result((data, s))
            return True
        self.addHandler(handler)
        return await fut

    # Terminate the Connection to Q400 Permanently. For a new Connection, create a new Class.
    async def end(self):
        self._ending = True
        if self._writer is not None:
            await self._writer.drain()
        if self.isConnected():
            self._writer.close()
            await self._writer.wait_closed()
        await self._task

    # Send a raw String to Q400 (without Packet Terminators)
    async def _sendStr(self, data: str, timeout=None):
        try:
            if self._ending:
                raise Q400ConnectionError(message="Connection is being Ended. Further transmission of data Allowed")
            await asyncio.wait_for(self._waitConnected(), timeout)
            b: bytes = data.encode("UTF-8")
            if b is not None:
                self._writer.write(b)
            await self._writer.drain()
        except Exception as error:
            print(error)

    # Send a Dict Packet to Q400
    async def send(self, data: dict, timeout: float = None):
        data = dict(data)
        data["version"] = self._version
        s = json.dumps(data, allow_nan=False, separators=(',', ':'), indent=2 if self._prettyJson else None)
        s = "\x02" + s + "\x03"
        await self._sendStr(s, timeout=timeout)

    async def sendAndWaitForResponse(self, data: dict, handler: typing.Callable[[dict, str], typing.Awaitable[typing.Any]], timeout: float = None):
        async def sendAndWaitHandler(d: dict, s: str):
            ret = await handler(d, s)
            if ret is not None:
                future.set_result(ret)
                return True
            return False
        future: asyncio.Future = asyncio.get_running_loop().create_future()
        self.addHandler(sendAndWaitHandler)
        await self.send(data, timeout)
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            pass
        except Exception as e: 
            pass
        finally:
            self.removeHandler(sendAndWaitHandler)

    # Wait for a Connection to Q400
    async def _waitConnected(self):
        while not self.isConnected():
            await self._future

    # Test if a Connection to Q400 is established
    def isConnected(self) -> bool:
        return (self._writer is not None) and (self._future.done())
