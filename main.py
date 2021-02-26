from datetime import datetime
from cutesy_mvc.helpers import migrate, path
from cutesy_mvc.helpers.db import Where, Table

def getNixTs():
  return datetime.now().timestamp()
  
def nixTsToDateTime(ts):
  return datetime.fromtimestamp(ts)

def hyphenatedTsStr():
  parts = str(datetime.now().timestamp()).split('.')
  return f'{parts[0]}-{parts[1]}'
  
def floatTsFromHyphenFormat(tstring):
  parts = tstring.split('-')
  joined = f'{parts[0]}.{parts[1]}'
  return float(joined)
  
print(getNixTs())
print(nixTsToDateTime(getNixTs()))
print(hyphenatedTsStr())
print(floatTsFromHyphenFormat(hyphenatedTsStr()))
  
  
wh = [{
  'type': 'series',
  'series': [{
    'type': 'single',
    'condition': ('x', '=', '1')
  },{
    'type': 'single',
    'operator': 'AND',
    'condition': ('y', '=', '2')
  }]
},{
  'type': 'single',
  'operator': 'OR',
  'condition': ('z', '=', '3')
},{
  'type': 'series',
  'operator': 'AND',
  'series': [{
    'type': 'single',
    'condition': ('x', '=', '1')
  },{
    'type': 'single',
    'operator': 'AND',
    'condition': ('y', '=', '2')
  }]
}]

wo = Where(wh)
print(wo.getConditionString())

# club seed
# name text *
# created_at real * 
# updated_at real

cs = [
  ['chess club', getNixTs()],
  ['fight club', getNixTs()],
  ['book club', getNixTs()]
]

for c in cs:
  Table('club').insert(['name', 'created_at'], [[c[0], c[1]]])
  
recs = Table('club').get()
for r in recs:
  print(f'Name: {r["name"]}, ts: {r["created_at"]}, id: {r["id"]}')

# user seed 
# name text * 
# age int *
# created_at real *
# updated_at real 
# clubId int 

us = [
  ['Billy', 15, getNixTs()],
  ['Jodi', 17, getNixTs()],
  ['Cark', 19, getNixTs()]
]

for u in us:
  Table('user').insert(['name', 'age', 'created_at'], [
    [u[0], u[1], u[2]]
  ])

recs = Table('user').get() 
for r in recs:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')

rec = Table('user').find(3)
for r in rec:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')

w = Where([{'type':'single','condition':['age','>=',17]}])

rec = Table('user').conditions(w).get()
for r in rec:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')

print('first test')

rec = Table('club').first()
for r in rec:
  print(f'Name: {r["name"]}, id: {r["id"]}')

print('first w/ condition test')

w = Where([{'type':'single','condition':['id','<',3]}])

rec = Table('club').conditions(w).first()
for r in rec:
  print(f'Name: {r["name"]}, id: {r["id"]}')

del w

print('value w/ condition test')

w = Where([{'type':'single','condition':['name','LIKE','%club']}])

rec = Table('club').conditions(w).value('name')
for r in rec:
  print(f'Name: {r["name"]}')

del w

print('pluck w/ condition test')

w = Where([{'type':'single','condition':['name','LIKE','%club']}])

rec = Table('club').conditions(w).pluck('name')
for r in rec:
  print(f'Name: {r["name"]}')

del w

del rec 

rec = Table('user').orderBy('name').get()
for r in rec:
  print(f'Name: {r["name"]}, id: {r["id"]}')
  
del rec
  
Table('user').insert(['name','age','created_at'],[
    ['Cark', 21, getNixTs()]
  ])
rec = Table('user').orderBy('name').get()
for r in rec:
  print(f'Name: {r["name"]}, id: {r["id"]}')

del rec 

rec = Table('user').distinct().columns(['name','age']).get()
for r in rec:
  print(f'Name: {r["name"]}, Age: {r["age"]}')
  
del rec 

rec = Table('user').insertGetId(['name','age','created_at'],[
    ['Cark', 31, getNixTs()]
  ])
 
rec = Table('user').average('age')
print(rec)
del rec 

recs = Table('user').condition('name','=','Cark').get() 
for r in recs:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')

del recs

recs = Table('user').get() 
for r in recs:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')
  
del recs 
Table('user').limit(2).orderBy('age').condition('name', '=','Cark').update(['name','age'],['Carkk',2])
recs = Table('user').get() 
for r in recs:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')
del recs 

rec = Table('user').condition('name','=','Carkk').count()
print(rec)
del rec 
print(Table('user').condition('name','=','Carkk').count('updated_at'))

print(Table('user').condition('name','=','Carkk').exists())
print(Table('user').condition('name','=','Carkkk').exists())
print(Table('user').condition('name','=','Carkk').doesntExist())
print(Table('user').condition('name','=','Carkkk').doesntExist())
print(Table('user').condition('name','<>','Carkk').maximum('age'))
print(Table('user').condition('name','<>','Carkk').minimum('age'))

Table('user').condition('name','=','Carkk').delete()
rec = Table('user').orderBy('name').get()
for r in rec:
  print(f'Name: {r["name"]}, id: {r["id"]}')
del rec 

Table('user').limit(2).orderBy('id').condition('name','=','Billy').delete()
rec = Table('user').orderBy('name').get()
for r in rec:
  print(f'Name: {r["name"]}, id: {r["id"]}')
del rec 

Table().vacuum()

count = 0

def mycb(rec):
  global count
  count += 1
  if count == 15:
    return False
  print(f'{rec["id"]} {rec["name"]}')
  return True

Table('user').condition('name','=','Jodi').chunk(5,mycb)

count = 0

Table('user').chunkById(5,mycb)

# test_score seed
# score real *
# userId int *
# created_at real *
# updated_at real

# tested db components:
# Where 
# Table:
## insert
## get 
## find 
## conditions 
## first
## value 
## pluck 
## order by
## distinct 
## columns 
## insertGetId
## average 
## condition 
## limit 
## update 
## count
## exists 
## doesntExist
## maximum 
## minimum
## delete
## vacuum 
## chunk
## chunkById