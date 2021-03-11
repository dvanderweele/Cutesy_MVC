from cutesy_mvc.models.user import User
from cutesy_mvc.helpers.db import Where, Table

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

# methods tested

# methods to test:
## isDirty
## isClean
## hydrated
## isSameModel, isNotSameModel
## trashed
## withTrashed
## onlyTrashed
## allModels
## fresh
## refresh
## find
## setLastPulled
## save (create, update)
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
## load (hasOne, hasMany, belongsTo, belongsToMany, morphOne, morphMany, morphTo, morphToMany, morphedByMany)
## touchIfNeeded (as called by other methods)

# to be implemented:
## cutify tool for generating model boilerplate files
