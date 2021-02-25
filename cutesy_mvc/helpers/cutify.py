


from ..helpers import migrate

def handleCuteness(userInput):
  argParts = userInput.split(':')
  if argParts[0] == 'make':
    if argParts[1] == 'migration':
      migType = argParts[2]
      migTarget = argParts[3]
      migrate.generateMigrationFile(migType, migTarget)
  elif argParts[0] == 'migrate':
    migrate.migrate()
  elif argParts[0] == 'rollback-migrations':
    migrate.rollback()
  elif argParts[0] == 'db':
    if argParts[1] == 'refresh':
      migrate.refresh()
    elif argParts[1] == 'schema':
      migrate.schema()