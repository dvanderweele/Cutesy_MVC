from ..helpers import config, db, migrate, timestamp 

class Model:
  connection = config.get(f'db.list.{config.get("db.current")}')
  softDeletes = False 
  timestamps = True 
  schema = migrate.schema(False, connection)
  includeTrashed = False
  exclusivelyTrashed= False
  
  def __init__(self):
    self.__originals = {}
    self.__lastPushed = {}
    self.__lastPulled = {}
    self.__includeTrashed = False
    self.__onlyTrashed = False 
    self.__distinct = False
    self.__limit = None 
    self.__ordering = []
    self.__conditions = None
    self.__record = {}
    for c in self.__class__.schema[self.__class__.table].keys():
      self.__record[c] = None

  def __getitem__(self, key):
    return self.__record[key]

  def __setitem__(self, key, newval):
    self.__record[key] = newval
    
  def setOriginals(self, cols):
    self.__originals = cols
    
  def getOriginal(self):
    return self.__originals 
    
  def isDirty(self, att = None):
    dirty = False
    if att != None:
      if att not in self.__lastPulled.keys() or self.__lastPulled[att] != self[att]:
        return True
    else:
      for k in self.__class__.schema[self.__class__.table].keys():
        if k in self.__lastPulled.keys() and self.__lastPulled[k] != self[k]:
          dirty = True
          break
        elif k not in self.__lastPulled.keys():
          dirty = True
          break 
      return dirty 
    
  def isClean(self, att = None):
    return not(self.isDirty(att))
    
  def hydrated(self):
    res = True 
    for k in self.__class__.schema[self.__class__.table].keys():
      if not(self.__class__.schema[self.__class__.table][k]['nullable']) and self.__record[k] == None:
        res = False
        break
    return res
    
  def trashed(self):
    if not(self.softDeletes) or 'deleted_at' not in self.schema[self.__class__.table].keys() or self['deleted_at'] == None:
      return False
    else:
      return True

  def withTrashed(self):
    self.__includeTrashed = True
    
  def onlyTrashed(self):
    self.__onlyTrashed = True
    return self
    
  def allModels(self):
    res = None
    if not self.__class__.softDeletes or self.__includeTrashed:
      res = db.Table(self.__class__.table).setConnection(self.__class__.connection).get()
    else:
      op = '<>' if self.__onlyTrashed else '='
      res = db.Table(self.__class__.table).setConnection(self.__class__.connection).condition('deleted_at', op, None)
    out = []
    for r in res:
      m = self.__class__()
      m.setOriginals(r)
      for c in r.keys():
        m[c] = r[c]
      out.append(m)
      del m 
    return out 
    
  def fresh(self):
    res = db.Table(self.__class__.table).setConnection(self.__class__.connection).find(self['id'])
    for c in res[0].keys():
      self[c] = res[0][c]

  def find(self, id):
    res = db.Table(self.__class__.table).setConnection(self.__class__.connection).find(id)
    if len(res) > 0:
      m = self.__class__()
      m.setOriginals(res[0])
      for c in res[0].keys():
        m[c] = res[0][c]
      m.setLastPulled(res[0])
      return m
    else:
      return None
  
  def setLastPulled(self,record):
    for k in record.keys():
      self.__lastPulled[k] = record[k]

  def save(self):
    if self['id'] != None:
      # update
      self['updated_at'] = timestamp.getNixTs()
      self.__lastPushed['updated_at'] = self['created_at']
      cols = []
      vals = []
      for k in self.__record.keys():
        self.__lastPushed[k] = self.__record[k]
        self.__lastPulled[k] = self.__record[k]
        cols.append(k)
        vals.append(self.__record[k])
      # update record 
      db.Table(self.__class__.table).setConnection(self.__class__.connection).condition('id','=',self['id']).update(cols,vals)
    else:
      # create
      self['created_at'] = timestamp.getNixTs()
      self.__lastPushed['created_at'] = self['created_at']
      # update lastPushed dict
      cols = []
      vals = []
      for k in self.__record.keys():
        self.__lastPushed[k] = self.__record[k]
        self.__lastPulled[k] = self.__record[k]
        cols.append(k)
        vals.append(self.__record[k])
      # push record 
      newid = db.Table(self.__class__.table).setConnection(self.__class__.connection).insertGetId(cols,[vals])
      self['id'] = newid 
      self.__lastPushed['id'] = newid
  
  def limit(self,l):
    self.__limit = l
    return self 
    
  def orderBy(self,col,d = 'asc'):
    self.__ordering.append((col,d))
    return self
    
  def condition(self, col, op, val):
    self.__conditions = db.Where([{'type':'single','condition':(col,op,val)}])
    return self
    
  def conditions(self, ws):
    self.__conditions = ws
    return self
    
  def distinct(self):
    self.__distinct = True
    return self
    
  def get(self):
    q = db.Table(self.__class__.table).setConnection(self.__class__.connection)
    if self.__distinct:
      q = q.distinct()
    if self.__conditions != None:
      q = q.conditions(self.__conditions)
    if self.__limit != None:
      q = q.limit(self.__limit)
    if len(self.__ordering) > 0:
      for o in self.__ordering:
        q = q.orderBy(o[0],o[1])
    raw = q.get()
    res = []
    for r in raw:
      m = self.__class__()
      m.setOriginals(r)
      for c in r.keys():
        m[c] = r[c]
      m.setLastPulled(r)
      res.append(m)
    return res

  def chunk(self, size, cb):
    statement = f'SELECT * FROM {self.__class__.table}'
    limit = size
    offset = 0
    params = []
    if self.__conditions != None:
      statement += ' '
      statement += self.__conditions.getConditionString()
      for p in self.__conditions.getParams():
        params.append(p)
    statement += ' LIMIT ?'
    params.append(limit)
    statement += ' OFFSET ?'
    params.append(offset)
    conn = db.Connection(True, self.__class__.connection)
    cur = conn.cursor
    res = cur.execute(statement, params).fetchall()
    del conn
    discontinue = False
    for rec in res:
      m = self.__class__()
      m.setOriginals(rec)
      for c in rec.keys():
        m[c] = rec[c]
      m.setLastPulled(rec)
      if not cb(m):
        discontinue = True
    while len(res) > 0 and not(discontinue):
      offset += size + 1
      statement = f'SELECT * FROM {self.__class__.table}'
      params = []
      if self.__conditions != None:
        statement += ' '
        statement += self.__conditions.getConditionString()
        for p in self.__conditions.getParams():
          params.append(p)
      statement += ' LIMIT ?'
      params.append(limit)
      statement += ' OFFSET ?'
      params.append(offset)
      conn = db.Connection(True, self.__class__.connection)
      cur = conn.cursor
      res = cur.execute(statement, params).fetchall()
      del conn
      for rec in res:
        m = self.__class__()
        m.setOriginals(rec)
        for c in rec.keys():
          m[c] = rec[c]
        m.setLastPulled(rec)
        if not cb(m):
          discontinue = True
          break
  
  def chunkById(self, size, cb):
    statement = f'SELECT * FROM {self.__class__.table}'
    limit = size
    last = 0
    self.condition('id', '>', last)
    params = []
    if self.__conditions != None:
      statement += ' '
      statement += self.__conditions.getConditionString()
      for p in self.__conditions.getParams():
        params.append(p)
    statement += ' ORDER BY id LIMIT ?'
    params.append(limit)
    conn = db.Connection(True, self.__class__.connection)
    cur = conn.cursor
    res = cur.execute(statement, params).fetchall()
    del conn
    discontinue = False
    for rec in res:
      last = rec['id']
      m = self.__class__()
      m.setOriginals(rec)
      for c in rec.keys():
        m[c] = rec[c]
      m.setLastPulled(rec)
      if not cb(m):
        discontinue = True
    while len(res) > 0 and not(discontinue):
      self.__conditions = None 
      self.condition('id', '>', last)
      statement = f'SELECT * FROM {self.__class__.table}'
      params = []
      if self.__conditions != None:
        statement += ' '
        statement += self.__conditions.getConditionString()
        for p in self.__conditions.getParams():
          params.append(p)
      statement += ' ORDER BY id LIMIT ?'
      params.append(limit)
      conn = db.Connection(True, self.__class__.connection)
      cur = conn.cursor
      res = cur.execute(statement, params).fetchall()
      del conn
      for rec in res:
        last = rec['id']
        m = self.__class__()
        m.setOriginals(rec)
        for c in rec.keys():
          m[c] = rec[c]
        m.setLastPulled(rec)
        if not cb(m):
          discontinue = True
          break
  
  def delete(self):
    if self.softDeletes:
      pass 
    else:
      q = db.Table(self.__class__.table).setConnection(self.__class__.connection)
      if self.__conditions!= None:
        q = q.conditions(self.__conditions)
      else:
        q = q.condition('id','=',self['id'])
      q.delete()
  
  def destroy(self, targetId):
    if self.softDeletes:
      pass
    else:
      db.Table(self.__class__.table).setConnection(self.__class__.connection).condition('id','=',targetId).delete()
  
  def hasOne(self, model, foreign):
    res = db.Table(model.__class__.table).setConnection(model.__class__.connection).condition(foreign,'=',self['id']).first()
    if len(res) < 1:
      return None 
    else:
      m = model.__class__()
      m.setOriginals(res[0])
      for c in res[0].keys():
        m[c] = res[0][c]
      m.setLastPulled(res[0])
      return m 
      
  def hasMany(self,model,foreign):
    res = db.Table(model.__class__.table).setConnection(model.__class__.connection).condition(foreign,'=',self['id']).get()
    if len(res) < 1:
      return [] 
    else:
      coll = []
      for rec in res:
        m = model.__class__()
        m.setOriginals(rec)
        for c in rec.keys():
          m[c] = rec[c]
        m.setLastPulled(rec)
        coll.append(m)
      return coll
    
  
  def belongsTo(self,model,foreign):
    res = db.Table(model.__class__.table).setConnection(model.__class__.connection).condition('id','=',self[foreign]).first()
    if len(res) < 1:
      return None 
    else:
      m = model.__class__()
      m.setOriginals(res[0])
      for c in res[0].keys():
        m[c] = res[0][c]
      m.setLastPulled(res[0])
      return m 
      
  def belongsToMany(self, model, intermediary, conn = config.get(f'db.list.{config.get("db.current")}')):
    joins = [k[model.__class__.table + '_id'] for k in db.Table(intermediary).setConnection(conn).condition(self.__class__.table+'_id','=',self['id']).get()]
    res = []
    for j in joins:
      rec = db.Table(model.__class__.table).setConnection(model.__class__.connection).condition('id','=',j).first()
      m = model.__class__()
      m.setOriginals(rec[0])
      for c in rec[0].keys():
        m[c] = rec[0][c]
      m.setLastPulled(rec[0])
      res.append(m)
    return res
    
    
  