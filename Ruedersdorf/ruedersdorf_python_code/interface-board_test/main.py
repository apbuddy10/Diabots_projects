from interface_board import Board, Mouse, board_by_id, Keyboard
import asyncio
import types


class OrthoMachine:
  board: Board
  def __init__(self,board:Board,arrPos):
    self.board = board
    self.arrPos = arrPos
    
  async def openDoor(self):
    try:
      await self.board.mouse.reset()
      await self.board.mouse.moveAbs(*self.arrPos[0])    # 1st button
      await self.board.mouse.click() 
      await asyncio.sleep(1)
      await self.board.mouse.moveAbs(*self.arrPos[6])    # Load Button
      await self.board.mouse.click() 
      await asyncio.sleep(7)
      return True
    except Exception as e:
      print(e)
      return False
    
  async def moveToPos(self,position):
    try: 
      await self.board.mouse.reset()
      await self.board.mouse.moveAbs(*self.arrPos[position - 1])    
      await self.board.mouse.click() 
      await asyncio.sleep(3)
      return True
    except Exception as e:
      print(e)
      return False

# async def main():
#   board = board_by_id(8)
#   arrPos = [[520,320],[580,220],[680, 220],[740, 320],[720, 430],[650, 500],[80,700]]
#   orthoMachine = OrthoMachine(board,arrPos)
#   await orthoMachine.board.check_connection()
#   await orthoMachine.openDoor()
#   await asyncio.sleep(10)
#   await orthoMachine.moveToPos(1)
#   await orthoMachine.moveToPos(2)
#   await orthoMachine.moveToPos(3)
#   await orthoMachine.moveToPos(4)
#   await orthoMachine.moveToPos(5)
#   await orthoMachine.moveToPos(6)
  


# asyncio.run(main())
