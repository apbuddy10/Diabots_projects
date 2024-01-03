from interface_board import Board, Mouse, board_by_id, Keyboard
import asyncio
import types

async def test_mouse(board: Board):
  arrPos = [[520,320],[580,220],[680, 220],[740, 320],[720, 430],[650, 500],[80,700]]
  # await board.mouse.moveAbs(520,320)   # 1st button
  # await board.mouse.moveAbs(580,220)   #  2nd button
  # await board.mouse.moveAbs(680, 220)   #  3rd button
  # await board.mouse.moveAbs(740, 320)   # 4th button
  # await board.mouse.moveAbs(720, 430)   # 5th button
  # await board.mouse.moveAbs(650, 500)   # 6th button
  # await board.mouse.moveAbs(80,700)   # Load button

  # Open the door 
  await board.mouse.reset()
  await board.mouse.moveAbs(*arrPos[0])    # 1st button
  await board.mouse.click() 
  await asyncio.sleep(1)
  await board.mouse.moveAbs(*arrPos[1])    # Load Button

  # Move to positions from 1 to 6 
  # positionNum = 1
  # await board.mouse.reset()
  # await board.mouse.moveAbs(*arrPos[positionNum - 1])    
  # await board.mouse.click() 

  # for location in arrPos:
  #   await board.mouse.reset()
  #   await board.mouse.moveRel(location[0], location[1])  
  #   await board.mouse.press(Mouse.BUTTON.LEFT)
  #   await board.mouse.release(Mouse.BUTTON.LEFT)
  #   await asyncio.sleep(5)
  


  # await board.mouse.moveWheel(-1)
  # await board.mouse.click()
  # await board.mouse.moveAbs(100, 10)
  # await board.mouse.dblClick()
  # await board.mouse.moveClick(100, 100)
  # await board.mouse.moveDblClick(100, 100)
  # await board.mouse.movePercent(0.5, 0.5)
  # await board.mouse.movePercentClick(0.5, 0.5)
  # await board.mouse.movePercentDblClick(0.5, 0.5)

async def test_keyboard(board: Board):
  await asyncio.sleep(1)
 
  await board.keyboard.reset()
  # await board.keyboard.press(4)
  # await board.keyboard.update(Keyboard.KEY_DOWN.KEY_B)
  # await board.keyboard.update(Keyboard.KEY_UP.KEY_B)
  # Open door
  await board.keyboard.down(Keyboard.KEY_CODES.KEY_F1)
  await board.keyboard.up(Keyboard.KEY_CODES.KEY_F1)
  await asyncio.sleep(6)
  await board.keyboard.down(Keyboard.KEY_CODES.KEY_ESCAPE)
  await board.keyboard.up(Keyboard.KEY_CODES.KEY_ESCAPE)
  await asyncio.sleep(1)
  await board.keyboard.down(Keyboard.KEY_CODES.KEY_ENTER)
  await board.keyboard.up(Keyboard.KEY_CODES.KEY_ENTER)
  
  # close door
  await asyncio.sleep(8)
  await board.keyboard.down(Keyboard.KEY_CODES.KEY_ENTER)
  await board.keyboard.up(Keyboard.KEY_CODES.KEY_ENTER)
  await asyncio.sleep(1)
  await board.keyboard.down(Keyboard.KEY_CODES.KEY_ESCAPE)
  await board.keyboard.up(Keyboard.KEY_CODES.KEY_ESCAPE)
  await asyncio.sleep(1)
  await board.keyboard.down(Keyboard.KEY_CODES.KEY_ENTER)
  await board.keyboard.up(Keyboard.KEY_CODES.KEY_ENTER)

  # await board.keyboard.sequence([Keyboard.KEY_DOWN.KEY_LEFT_CONTROL, Keyboard.KEY_DOWN.KEY_S, Keyboard.KEY_UP.KEY_S, Keyboard.KEY_UP.KEY_LEFT_CONTROL])


async def main():
  board = board_by_id(8)
  await board.check_connection()
  await test_mouse(board)
  # await test_keyboard(board)

asyncio.run(main())
