import os, sys
from cutesy_mvc.helpers.db import Where, Table
from cutesy_mvc.helpers import path, cutify
from cutesy_mvc.models.Customer import Customer 
from cutesy_mvc.models.Phone import Phone 

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
    p.save()
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

## SCHEMAS
### customer 
#### name/text* 
### phone 
#### IMEI/int*, customer_id/int 
### blog_post 
### comment 
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

# methods to test:
## isDirty
## isClean
## hydrated
## trashed
## withTrashed
## onlyTrashed
## allModels
## fresh
## refresh
## find
## setLastPulled
## save (update)
## limit
## orderBy
## condition
## conditions 
## get 
## chunk 
## chunkById
## delete
## forceDelete 
## destroy 
## restore 
## load (hasMany, belongsTo, belongsToMany, morphOne, morphMany, morphTo, morphToMany, morphedByMany)
## touchIfNeeded (as called by other methods)

# to be implemented:
