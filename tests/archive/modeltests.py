import os 
from cutesy_mvc.helpers.db import Where, Table
from cutesy_mvc.helpers import path, cutify
from cutesy_mvc.models.Customer import Customer
from cutesy_mvc.models.Phone import Phone
from cutesy_mvc.models.BlogPost import BlogPost
from cutesy_mvc.models.Comment import Comment
from cutesy_mvc.models.Student import Student 
from cutesy_mvc.models.Schedule import Schedule
from cutesy_mvc.models.Course import Course
from cutesy_mvc.models.User import User 
from cutesy_mvc.models.Image import Image 
from cutesy_mvc.models.Video import Video 
from cutesy_mvc.models.Hashtag import Hashtag 
from cutesy_mvc.models.Tag import Tag 
from cutesy_mvc.models.Tagable import Tagable 

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

print('belongsToMany Test')

s = Student().allModels()
for p in s:
	print(p)

cs = Course()
cs['title'] = 'discrete math'
cs.save()
eng = Course()
eng['title'] = 'composition'
eng.save()

for x in [a for a in Course().allModels()]:
	print(x)
	
s = Schedule()
s['student_id'] = 1 
s['course_id'] = 1 
s.save()
s = Schedule()
s['student_id'] = 1 
s['course_id'] = 2
s.save()
s = Schedule()
s['student_id'] = 3 
s['course_id'] = 1
s.save()

print('courses of student 1')
stud = Student().find(1)
stud.load('courses')
for c in stud['courses']:
	print(c)
	
print('students of course 1')
crs = Course().find(1)
crs.load('students')
for s in crs['students']:
	print(s)

print('morphone morphto tests')

print('blog_posts:')
posts = BlogPost().allModels()
for p in posts:
	print(p)
	
print('seeding users')
u = User()
u['name'] = "Jeffrey"
u.save()
u = User()
u['name'] = "Jackson"
u.save()

print('seeding images')
pic = Image()
pic['URL'] = 'https://arachni.dev/logo.gif'
pic['alt'] = 'ArachniDev LLC URL'
pic['imageable_type'] = 'User'
pic['imageable_id'] = 1 
pic.save()
pic = Image()
pic['URL'] = 'https://arachni.dev/post1.jpg'
pic['imageable_type'] = 'BlogPost'
pic['imageable_id'] = 2
pic.save()

print('images')
imgs = Image().allModels()
for i in imgs:
	print(i)
	i.load('imageable')
	print(i['imageable'])
	
print('images from relations')

b1 = BlogPost().find(2)
b1.load('image')
print(b1['image'])
us = User().find(1)
us.load('image')
print(us['image'])

print('morphMany morphTo tests')

v = Video()
v['title'] = 'complaint log 257'
v['url'] = 'https://y.tube/ddgg332da'
v['description'] = 'lorem loren loren yeah'
v.save()
v = Video()
v['title'] = 'a pirate song'
v['url'] = 'https://y.tube/kfkfidjsjsn'
v['description'] = 'hi ho hi ho hi ho'
v.save()

h = Hashtag()
h['tag'] = 'yolo'
h['hashtagable_type'] = 'Video'
h['hashtagable_id'] = 1
h.save()
h = Hashtag()
h['tag'] = 'ughh'
h['hashtagable_type'] ='Video'
h['hashtagable_id'] = 2 
h.save()
h = Hashtag()
h['tag'] = 'diy'
h['hashtagable_type'] = 'BlogPost'
h['hashtagable_id'] = 2 
h.save()

bp = BlogPost().find(2)
bp.load('hashtags')
print(bp['hashtags'][0])
vs = Video().allModels()
for v in vs:
	v.load('hashtags')
	for h in v['hashtags']:
		print(h)

tags = Hashtag().allModels()
for h in tags:
	h.load('hashtagable')
	print(h['hashtagable'])
	
print('morphToMany & morphedByMany')

b = BlogPost().find(2)
print(b)
c = BlogPost().find(3)
print(c)
v = Video().find(1)
w = Video().find(2)
print(v)
print(w)

t = Tag()
t['name'] = 'updates'
t.save()
tt = Tag()
tt['name'] = 'rantings'
tt.save()
ttt=Tag()
ttt['name'] = 'ravings'
ttt.save()

p = Tagable()
p['tag_id'] = 1 
p['tagable_id'] = 2 
p['tagable_type'] = 'BlogPost'
p.save()
p = Tagable()
p['tag_id'] = 2
p['tagable_id'] = 2 
p['tagable_type'] = 'BlogPost'
p.save()
p = Tagable()
p['tag_id'] = 3
p['tagable_id'] = 1
p['tagable_type'] = 'Video'
p.save()

b.load('tags')
for tag in b['tags']:
	print(tag)
	tag.load('tagables')
	for t in tag["tagables"]:
		print(f'Tagable {t}')
v.load('tags')
for tag in v['tags']:
	print(tag)
	tag.load('tagables')
	for t in tag["tagables"]:
		print(f'Tagable {t}')
	
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
#### student_id/int*, course_id/int*
### course 
#### title/text*, description/text
### user 
#### name/text* 
### image
#### URL/text*, alt/text, imageable_id/int, imageable_type/text 
### video 
#### title/text*, url/text*, description/text 
### hashtag 
#### tag/text*, hashtagable_type/text, hashtagable_id/int 
### tag 
#### name/text*
### tagable 
#### tag_id/int*, tagable_id/int*, tagable_type/text*

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
## touchIfNeeded