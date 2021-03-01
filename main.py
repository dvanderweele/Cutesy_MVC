from cutesy_mvc.models.user import User
from cutesy_mvc.helpers.db import Where, Table

#res = User().allModels()
#for m in res:
  #print(f'id: {m["id"]}, name: {m["name"]}, clean: {"y" if m.isClean() else "n"}')

print('find test')
res = User().find(330)
if res != None:
  print(f'id: {res["id"]}, name: {res["name"]}')
else:
  print('no such user.')

#u = User()
#u['name'] = 'horatio'
#u['age'] = 29
#u.save()

f = User().find(331)
print(f'id {f["id"]}, name: {f["name"]}, age: {f["age"]} {"clean" if f.isClean() else "dirty"}')
f['age'] = 120
print(f.isClean())
print(f.isClean('age'))
print(f.isClean('name'))
print(f.getOriginal()['age'])
f.save()
print(f.isClean())
print(f.getOriginal()['age'])
f['name'] = "hardyharhar"
g = User().find(331)
g['name'] = 'bamboozled'
g.save()
print(f['name'])
f.fresh()
print(f['name'])
h = User()
print(h.hydrated())
i = h.find(331)
i['name'] = None
print(i.hydrated())
i['name'] = 'hhhortatio'
print(i.hydrated())

ums = User().limit(5).condition('id','<',250).orderBy('id', 'dsc').get()
print(len(ums))
for um in ums:
  print(f'id: {um["id"]}, name: {um["name"]}')
  
w = [{'type': 'series','series':[{'type':'single','condition':('name','=','Jodi')},{'type':'single','operator':'OR','condition':('age','<',20)}]}]

ums = User().limit(6).conditions(Where(w)).get()
print(len(ums))
for u in ums:
  print(u['id'], u['age'], u['name'])

ums = User().distinct().limit(6).conditions(Where(w)).get()
print(len(ums))
for u in ums:
  print(u['id'], u['age'], u['name'])


print("CHUNK TEST")

c = 0
t = 0

def mycb(m):
  global c
  global t
  c += 1
  t += 1
  if c == 10:
    print("end chunk")
    c = 0
  if t == 30:
    return False
  print(f'{m["id"]} {m["name"]}')
  return True

User().chunk(10,mycb)

print('CHUNKBYID TEST')

t = 0 
c = 0 

User().chunkById(10,mycb)

res = Table('user').distinct().pluck('name')
for r in res:
  print(f'{r["name"]}')

# Model Method Testing 

## tested
### find
### allModels - on no softDeletes model only
### save 
### isDirty
### isClean 
### setLastPulled
### getOriginal 
### fresh
### hydrated 
### limit
### orderBy
### condition
### conditions
### distinct
### get - order by, limit, condition , conditions
### chunk
### distinct
### chunkById

## untested
### onlyTrashed
### withTrashed
### trashed
### delete
### destroy 
### hasOne 
### hasMany 
### belongsTo
### belongsToMany