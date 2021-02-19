import sqlite3
from ..helpers import config, path 

# SQLite Data Types
# 0 - NULL
# 1 - INTEGER
# 2 - REAL 
# 3 - TEXT 
# 4 - BLOB
dataTypes = ('NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB')

class Connection:
  def __init__(self):
    self.__dbname = config.get('db.current')
    self.__path = path.appendFileToRootDir(config.get(f'db.list.{self.__dbname}'))
    self.__conn = sqlite3.connect(self.__path)
    self.cursor = self.__conn.cursor()
    self.cursor.execute('PRAGMA foreign_keys=ON')
  def __del__(self):
    self.__conn.commit() 
    self.__conn.close() 

class Query:
  def __init__(self, statementObj):
    self.__statement = statementObj
  def execute(self):
    self.__conn = Connection()
    if not self.__statement.getParamList():
      self.__conn.cursor.execute(self.__statement.getQueryString())
    else:
      self.__conn.cursor.execute(self.__statement.getQueryString(), self.__statement.getParamList())
    del self.__conn

class Queries:
  def __init__(self, statements):
    self.__statements = statements
  def execute(self):
    self.__conn = Connection()
    for q in self.__statements:
      self.__conn.cursor.execute(q.getQueryString(), q.getParamList())
    del self.__conn

class CreateTableStatement:
  def __init__(self, tableName, columns, composite = None, foreigns = None):
    # columns should be a tuple of tuples, with each inner tuple 
    # having length 2 and representing a column name and datatype string
    # if non-null composite is provided, it is a one dimensional tuple of column names
    # if non-null foreigns is provided, it is a list of dictionaries where name key is column name in this table and reference key is a tuple of length two w/ 1st val being table name and 2nd being column name
    self.__tableName = tableName

    self.__columns = columns
    self.__composite = composite
    self.__foreigns = foreigns
  def getQueryString(self):
    res = f'CREATE TABLE IF NOT EXISTS {self.__tableName} ('
    for i in range(0, len(self.__columns)):
      res += f'{self.__columns[i][0]} {self.__columns[i][1]}'
      if i != len(self.__columns) - 1:
        res += ', '
    if self.__composite != None:
      res += ', PRIMARY KEY('
      for i in range(0, len(self.__composite)):
        if i != 0:
          res += ', '
        res += self.__composite[i]
      res += ')'
    if self.__foreigns != None:
      res += ','
      for i in range(0, len(self.__foreigns)):
        if i != 0 and i < len(self.__foreigns) - 1:
          res += ','
        k1 = self.__foreigns[i]['name']
        tn = self.__foreigns[i]['reference'][0]
        k2 = self.__foreigns[i]['reference'][1]
        res += f' FOREIGN KEY({k1}) REFERENCES {tn}({k2})'
        if i != len(self.__foreigns) - 1:
          res += ', '
    res += ')'
    return res
  def getParamList(self):
    return False
    
class DropTableStatement:
  def __init__(self, tableName):
    self.__tableName = tableName
  def getQueryString(self):
    return f'DROP TABLE IF EXISTS {self.__tableName}'
  def getParamList(self):
    return False
    
class AlterTableStatement:
  def __init__(self, tablename, line, upOrDown):
    self.__line = line.split(":")
    self.__tableName = tablename if self.__line[0] == 'rntab' and upOrDown == 'up' else self.__line[1]
  def getQueryString(self):
    # no support for sqlite's add column function because then we would have to emulate drop column functionality, which isn't directly supported
    # only support for renaming a column or a table 
    res = f"ALTER TABLE {self.__tableName} RENAME "
    if self.__line[0] == "rntab":
      res += f"TO {self.__line[2]}"
    elif self.__line[0] == "rncol":
      res += f"COLUMN {self.__line[2]} TO {self.__line[3]}"
  def getParamList(self):
    return False
    
class Where: 
  def __init__(self, conditions):
    self.__conditions = conditions
    self.__params = []
    self.__string = 'WHERE '
  def getConditionString(self):
    res = self.__string
    for i in range(0, len(self.__conditions)):
      res += self.__processConditionRecord(self.__conditions[i], i)
    return res
  def getParams(self):
    return self.__params
  def __processConditionRecord(self, rec, idx):
    res = ''
    if rec['type'] == 'single':
      if idx != 0:
        res+= ' ? '
        self.__params.append(rec['operator'])
      res += '(?'
      self.__params.append(rec['condition'][0])
      res += ' ?'
      self.__params.append(rec['condition'][1])
      res += ' ?'
      self.__params.append(rec['condition'][2])
      res += ')'
    elif rec['type'] == 'series':
      if idx != 0:
        res+= ' ? '
        self.__params.append(rec['operator'])
      res += '('
      for i in range(len(rec['series'])):
        res += self.__processConditionRecord(rec['series'][i], i)
      res += ')'
    elif rec['type'] == 'not':
      if idx != 0:
        res+= ' ? '
        self.__params.append(rec['operator'])
      res += 'NOT('
      for i in range(len(rec['not'])):
        res += self.__processConditionRecord(rec['not'][i], i)
      res += ')'
    return res 

class Table:
  def __init__(self, tableName):
    self.__table = tableName
    self.__statement = ''
    self.__params = []
    self.__finalized = False
    self.__conditions = None
    self.__columns = []
    self.__type = None
    self.__ordering = []
    self.__limit = None
    self.__offset = None
    self.__distinct = False
  
  def __buildStatement(self):
    if self.__type == 'sel':
      self.__statement += 'SELECT '
      if self.__distinct:
        self.__statement += ' DISTINCT '
      for i in self.__columns:
        if i != 0:
          self.__statement += ', '
        self.__statement += '?'
        self.__params.append(self.__columns[i])
      self.__statement += ' FROM ?'
      self.__params.append(self.__table)
      if self.__conditions != None:
        self.__statement += ' '
        self.__statement += self.__conditions.getConditionString()
        for p in self.__conditions.getParams():
          self.__params.append(p)
      if len(self.__ordering) > 0:
        for o in self.__ordering:
          self.__statement +=  ' ORDER BY ?'
          self.__params.append(o[0])
          if o[1] != 'asc':
            self.__statement += ' ?'
            self.__params.append('DESC')
      if self.__limit != None:
        self.__statement += ' LIMIT ?'
        self.__params.append(self.__limit)
      if self.__offset != None:
        self.__statement += ' OFFSET ?'
        self.__params.append(self.__offset)
    self.__finalizeStatement()
  
  def __finalizeStatement(self):
    if self.__type != None:
      self.__finalized = True

  def __execute(self):
    res = []
    if self.__finalized:
      conn = Connection()
      res = conn.cursor.execute(self.__statement, self.__params).fetchall()
      del conn
      return res

  def find(self, id):
    self.__type = 'sel'
    self.__conditions.append(('id', '==', id))
    self.__columns.append('*')
    self.__limit = '1'
    self.__buildStatement()
    return self.__execute()

  def first(self):
    self.__type = 'sel'
    self.__limit = '1'
    if len(self.__columns) < 1:
      self.__columns.append('*')
    self.__buildStatement()
    return self.__execute()

  def value(self, col):
    self.__type = 'sel'
    self.__columns.append(col)
    self.__limit = '1'
  
  def pluck(self, col):
    self.__type = 'sel'
    self.__columns.append(col)
    self.__buildStatement() 
    return self.__execute() 
  
  def conditions(self, w):
    self.__conditions = w
    return self

  def get(self):
    if self.__type == None:
      self.__type = 'sel'
    if len(self.__columns) < 1:
      self.__columns.append('*')
    self.__buildStatement() 
    return self.__execute()

  def distinct(self):
    self.__distinct = True 
    return self
  
  def orderBy(self, col, dr = 'asc'):
    self.__ordering.append((col, dr))
    return self 
    
  def chunk(self, size, cb):
    batch = 0
    if self.__type == None:
      self.__type = 'sel'
    if len(self.__columns) < 1:
      self.__columns.append('*')
    self.__limit = size
    self.__offset = 0
    self.__buildStatement() 
    res = self.__execute()