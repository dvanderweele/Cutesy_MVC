from ..helpers import test, config

def configTest1():
  if config.get('testy.mc.testerson') == 'yay':
    return True
  else:
    return False

configTests = [
  ("Config Test", configTest1)
]

def run():
  if test.Suite("Config Helper Tests",configTests):
    print("All Tests Passing :-)")
  else:
    print("Oof, some tests failing :-(")