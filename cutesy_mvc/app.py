from .tests import TUItest, configtest
from .helpers import file, TUI, cutify, timestamp
import sys 

def run():
  if len(sys.argv) > 2: 
    # cutesy command line service handler
    if sys.argv[1] == 'cutify':
      cutify.handleCuteness(sys.argv[2])
  else: 
    # ordinary execution
    TUItest.run()
    configtest.run()
    contents = file.File().get('users.txt')
    print(contents)
    contents = file.File('backup').get('users.txt')
    print(contents)
    contents = "Gobbledygook\nGobbledygook\nGobbledygook"
    file.File('backup').put('users.txt', contents)
    file.File().appendContent('users.txt',"\nadsf\nddddddd\n")
    contents = file.File().getLines('users.txt')
    print(contents)
    print("console dimensions")
    print(TUI.getConsoleLines())
    print(TUI.getConsoleColumns())
    print('timestamp drama')
    print(timestamp.getNixTimestampAsInt())
    print(timestamp.getNixTimestampAsFloat())
    print(timestamp.getNixTimestampAsStrInt())
    