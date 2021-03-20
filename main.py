import os 
from cutesy_mvc.helpers.db import Where, Table
from cutesy_mvc.helpers import path, cutify
from cutesy_mvc.models.Customer import Customer
from cutesy_mvc.models.Phone import Phone
from cutesy_mvc.models.BlogPost import BlogPost
from cutesy_mvc.models.Comment import Comment
from cutesy_mvc.models.Student import Student 
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
  
posts[2].delete()
print('soft deleted models')
dead = BlogPost().onlyTrashed().allModels()
for d in dead:
  print(d)
print('still undeleted models')
alive = BlogPost().allModels()
for a in alive:
  print(a)
alive[0].forceDelete()
print('force deleted a living model...')
left = BlogPost().withTrashed().allModels()
for l in left:
  print(l)
  if l.trashed():
    l.restore()

print('restored deleted model')
last = BlogPost().allModels()
for l in last:
  print(l)
  
more = BlogPost().allModels()
more[0]['title'] = 'haha fake title'
more[0].save()
print('more...')
for m in more:
	print(m)
print('left before and after')
for l in left:
	print('l before fresh')
	print(l)
	l.fresh()
	print('l after fresh')
	print(l)
	
BlogPost().destroy(3)

blags = BlogPost().withTrashed().allModels()
print('printing all after destroy id 3')
for b in blags:
  print(b)
  
ltest = BlogPost().limit(1).withTrashed().get()
print('test limit and get')
for l in ltest:
  print(l)

ft = BlogPost().find(3)
print(ft)
tt = BlogPost().withTrashed().find(3)
print(tt)

a1 = Student()
a1['name'] = 'Rocky'
a1['dob'] = '16 March 1946'
a1.save()

a2 = Student()
a2['name'] = 'Bullwinkle'
a2['dob'] = '17 April 1945'
a2.save()

a3 = Student()
a3['name'] = 'Yogi Bear'
a3['dob'] = '24 August 1947'
a3.save()

ss = Student().condition('name','<>','Rocky').orderBy('dob', 'd').get()

for d in ss:
	print(d)
	
rb = Where([
	{
		'type': 'single',
		'condition': ('name', '=', 'Rocky')
	},
	{
		'type': 'single',
		'operator': 'OR',
		'condition': ('name', '=', 'Bullwinkle')
	}
])

ast = Student().conditions(rb).get()
for a in ast:
	print(a)
Student().destroy(2)
rs = Student().withTrashed().allModels()
for r in rs: 
	print(r)

bs = BlogPost().onlyTrashed().get()
bs[0].restore()
bs = BlogPost().allModels()
for b in bs:
	print(b)
	
c = Comment()
c['body'] = 'All hail our lord lorem ipsum, dolor sit amet.'
c['blog_post_id'] = 2 
c.save()
c = Comment()
c['body'] = 'Praise be unto lorem ipsum, our lord, from now unto the very end of the age.'
c['blog_post_id'] = 2
c.save()

b = BlogPost().find(2)
b.load('comments')
for c in b['comments']:
	print(c)

btc = Comment().find(1)
btc.load('blogPost')
print(btc)
print(btc['blogPost'])

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
#### name/text*, dob/text*
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
## load (hasOne, hasMany, belongsTo) 
## save (create, update) 
## refresh 
## isSameModel, isNotSameModel 
## hydrated 
## allModels 
## delete (hard, soft) 
## withTrashed
## onlyTrashed 
## trashed 
## restore 
## fresh 
## destroy (soft, hard) 
## limit
## get
## find 
## orderBy
## condition 
## conditions
## chunk 
## chunkById

# methods to test:
## load (belongsToMany, morphOne, morphMany, morphTo, morphToMany, morphedByMany)
## touchIfNeeded