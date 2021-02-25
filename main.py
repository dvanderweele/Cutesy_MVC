from datetime import datetime
from cutesy_mvc.helpers import migrate
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

#for c in cs:
  #Table('club').insert(['name', 'created_at'], [[c[0], c[1]]])
  
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

#for u in us:
  #Table('user').insert(['name', 'age', 'created_at'], [
    #[u[0], u[1], u[2]]
  #])

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
  
#Table('user').insert(['name','age','created_at'],[
#    ['Cark', 21, getNixTs()]
#  ])
rec = Table('user').orderBy('name').get()
for r in rec:
  print(f'Name: {r["name"]}, id: {r["id"]}')

del rec 

rec = Table('user').distinct().columns(['name','age']).get()
for r in rec:
  print(f'Name: {r["name"]}, Age: {r["age"]}')
  
del rec 

#rec = Table('user').insertGetId(['name','age','created_at'],[
#    ['Cark', 31, getNixTs()]
#  ])

Table('user').conditions(Where([{'type':'single','condition':('age', '=','31')}])).increment('age', 2)

recs = Table('user').get() 
for r in recs:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')

Table('user').conditions(Where([{'type':'single','condition':('age', '=','33')}])).decrement('age', 2)

recs = Table('user').get() 
for r in recs:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')

del recs 
recs = Table('user').average('age')
print(recs)

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
## increment 
## decrement 
## average 

# Table To Test:
## condition
## update 
## count 
## exists 
## doesn't exist
## maximum 
## minimum
## delete
## vacuum 
## chunk (not implemented)
## chunkById (not implemented)