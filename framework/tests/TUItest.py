from ..helpers import test
from ..helpers import TUI

def condition(userin):
  if userin == "1":
    return True
  else:
    return False

def tuiInputTest1():
  TUI.clear()
  userInput = TUI.Input(condition, int, "Enter one: ", "You didn't enter one. Try again.").get()
  if userInput == 1:
    return True
  else:
    return False

tuiTests = [
  ("TUI Input Test", tuiInputTest1)
]

def run():
  if test.Suite("TUI Tests", tuiTests):
    print("All Tests Passing :-)")
  else:
    print("Oof, some tests failing :-(")