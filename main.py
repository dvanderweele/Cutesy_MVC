import os, sys
from cutesy_mvc.helpers.db import Where, Table
from cutesy_mvc.helpers import path, cutify
from cutesy_mvc.models.Customer import Customer
from cutesy_mvc.models.Phone import Phone
from cutesy_mvc.models.BlogPost import BlogPost
from cutesy_mvc.models.Comment import Comment
from cutesy_mvc.models.Hashtag import Hashtag 

# migration section

olddb = path.appendFileToRootDir('default.db')
if os.path.exists(olddb):
  os.remove(olddb)

cutify.handleCuteness('migrate')

# seeding section 

custs = []
for i in range(0,4):
  c = Customer()
  c['name'] = f'Person_{i}'
  c.save()
  c.load('phone')
  custs.append(c)
for c in custs:
  print()
  print(c)
  print(c['phone'])
  p = Phone()
  p['IMEI'] = 42 + c['id']
  p['customer_id'] = c['id']
  print(f'hydrated: {p.hydrated()}')
  p.save()
  print(f'hydrated: {p.hydrated()}')
  p['IMEI'] += c['id']
  p.save()
  print(p.isSameModel(c['phone']))
  c.load('phone')
  print(c)
  print(c['phone'])
  p['IMEI'] += 1000
  p.save()
  print(p.isSameModel(c['phone']))
  c.refresh()
  print(p.isSameModel(c['phone']))
  print(c['phone'])
  
print()
cc = Customer()
cc['name'] = "Freddyy"
cc.save()
clone = Customer().condition('name','=','Freddyy').get()[0]

print(clone.isSameModel(cc))

cs = Customer().allModels()
print(len(cs))
cs[len(cs) - 1].delete()
cz = Customer().allModels()
print(len(cz))

b1 = BlogPost()
b1['title'] = 'Whole Lotta Love'
b1['body'] = 'Lorem ipsum dolor sit amet.'
b1.save()
b2 = BlogPost()
b2['title'] = 'Dazed and Confused'
b2['body'] = 'Lorem ipsum dolor sit amet.'
b2.save()
b3 = BlogPost()
b3['title'] = 'In My Time of Dying'
b3['body'] = 'Lorem ipsum dolor sit amet.'
b3.save()

posts = BlogPost().allModels()
for p in posts:
  print(p)

## SCHEMAS
### customer 
#### name/text* 
### phone 
#### IMEI/int*, customer_id/int 
### blog_post
#### title/text*, body/text*, deleted_at/real
### comment 
#### body/text*, blog_post_id/int*
### student 
### schedule 
### course 
### user 
### image
### video 
### hashtag 
### tag 
### tagable 

# testing Model class 

# step 1:
## migrations required: 
### hasOne & belongsTo: customer, phone
### hasMany & belongsTo: blog_post, comments
### belongsToMany: student, schedule, course
### morphOne & morphTo: blog_posts, users, images
### morphMany & morphTo: blog_posts, videos, hashtags
### morphToMany & morphedByMany: blog_posts, videos, tags, tagables

# create model for each Table above 

# methods tested:
## load (hasOne)
## save (create, update)
## refresh
## isSameModel, isNotSameModel
## hydrated 
## allModels 
## delete (hard)

# methods to test:
## trashed
## withTrashed
## onlyTrashed
## fresh 
## find
## setLastPulled
## limit
## orderBy
## condition
## conditions 
## get 
## chunk 
## chunkById
## delete (soft)
## forceDelete 
## destroy 
## restore 
## load (hasMany, belongsTo, belongsToMany, morphOne, morphMany, morphTo, morphToMany, morphedByMany)
## touchIfNeeded (as called by other methods)

# to be implemented:
