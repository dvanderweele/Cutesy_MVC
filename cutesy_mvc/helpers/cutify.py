"""
Defines a single function for controlling framework components . 
"""
from ..helpers import migrate, path
from ..tests._index import suites

def handleCuteness(userInput):
  argParts = userInput.split(':')
  if argParts[0] == 'make':
    if argParts[1] == 'migration':
      migType = argParts[2]
      migTarget = argParts[3]
      migrate.generateMigrationFile(migType, migTarget)
    elif argParts[1] == 'model':
      fn = f'{argParts[2]}.py'
      p = path.appendDirToRootDir('models')
      p = path.appendFileToDir(p, fn)
      outfile = open(p, 'w')
      outfile.write(f'from ..helpers.model import Model\n\nclass {argParts[2]}(Model):\n    pass')
      outfile.close()
    elif argParts[1] == 'controller':
      fn = f'{argParts[2]}.py'
      p = path.appendDirToRootDir('controllers')
      p = path.appendFileToDir(p, fn)
      outfile = open(p, 'w')
      outfile.write(f'# {argParts[2]}.py\n\nfrom ..helpers.response import freshResponse\n\nclass {argParts[2]}:\n    pass')
      outfile.close()
  elif argParts[0] == 'migrate':
    migrate.migrate()
  elif argParts[0] == 'rollback-migrations':
    migrate.rollback()
  elif argParts[0] == 'db':
    if argParts[1] == 'refresh':
      migrate.refresh()
    elif argParts[1] == 'schema':
      migrate.schema()
  elif argParts[0] == 'test':
    passes = 0
    fails = 0
    for s in suites:
      s.run()
      print(s)
      passes += s.passes
      fails += s.fails
    print(f'###################\nSUMMARY OF ALL TEST SUITES\nTotal Passing Tests: {passes}\nTotal Failing Tests: {fails}\nPercent Passing: {(passes/(passes+fails)) * 100}%')
