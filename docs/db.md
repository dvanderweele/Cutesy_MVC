# Database Tools

Only SQLite is supported at this time. Not all database classes and methods are documented here simply because some of them only exist to power the migration system. 

## QueryBuilder

These tools are inspired heavily by the Laravel framework's query builder tools, albeit with far less functionality and let's be honest probably more glitches. But hey, any cool project is really about the friends we made along the way. 

### `Table` class 

Specify the name of the Table you are targeting with your query in the Table class constructor. The point is to then chain additional query methods after instantiation. Notice, there is no static method API like some other query builders.

```
Table('user').get()
```

#### insert

Parameters: 
1 - List of Columns 
2 - List of Records

Each record itself is a list of data to be inserted, having the order specified by the List of Columns in the first parameter. Even if you are inserting only one record, you must specify it in a list of records. 

```
from datetime import datetime

def getNixTs():
  return datetime.now().timestamp()

us = [
  ['Billy', 17, getNixTs()],
  ['Jodi', 15, getNixTs()],
  ['Cark', 19, getNixTs()]
]

for u in us:
  Table('user').insert(['name', 'age', 'created_at'], us)
```

#### get 

Used to terminate a `select` statement. May or may not come after various query constraints.

```
recs = Table('user').get() 
for r in recs:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')
# Name: Billy, Age: 17, 12345567788754, id: 1
# Name: Jodi, Age: 15, 12345567788755, id: 2
# Name: Cark, Age: 19, 12345567788756, id: 3
```

```
rec = Table('user').condition('age','>=',17).get()
for r in rec:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')
# Name: Billy, Age: 17, 12345567788754, id: 1
# Name: Cark, Age: 19, 12345567788756, id: 3
```

#### find 

This method expects the targeted table to have a primary key column named `id`. Pass in the id of the record you are looking for and it will be returned to you. No need to add additional conditions, and no need to chain an additional `get` call on the end.

```
rec = Table('user').find(3)
for r in rec:
  print(f'Name: {r["name"]}, Age: {r["age"]}, ts: {r["created_at"]}, id: {r["id"]}')
# Name: Cark, Age: 19, 12345567788756, id: 3
```

#### conditions 

This method cannot terminate a query. See `Where` section below for details on how to define single and compound `Where` objects. For this example, we will assume such an object is already defined and reference by the variable `w`.

```
results = Table('user').conditions(w).get()
```

#### first

An alternative to the `get` method for terminating a `select` query that you have built. The difference is that this method will limit the result set to one entry.

```
result = Table('user').first()
print(len(result))
# 1
print(f'id: {result[0]["id"]}, name: {result[0]["name"]}')
# e.g. id: 1, name: Billy
```

#### value 

Method takes one required parameter: the name of the column whose value you are interested in. Method is ussd to terminate a select query. Like the `first` method, result set will be limited to one entry. Instead of possessing all the columns' values like with a `get` query, only the specified column's value will be returned.

```
result = Table('user').value('name')
print(len(result))
# 1
print(f'name: {result[0]["name"]}')
# e.g. name: Billy

```

#### pluck 

Same as `value` method except that result set will not be limited to one entry. 

```
result = Table('user').pluck('name')
print(len(result))
# 3 
for r in result:
  print(f'name: {r["name"]}')
# e.g.
## name: Billy
## name: Jodi 
## name: Cark

```

#### orderBy

This method is used to add an ordering constraint to the query. Only the first parameter, the column to order results by, is required. The second parameter defaults to 'asc' to specify an ascending ordering. Anything other than 'asc' will result in a descending ordering. This method cannot terminate a query.

```
result1 = Table('user').condition('age','>=',17).orderBy('age').get()
for r in result1:
  print(f'name: {r["name"]}, age: {r["age"]}')
# name: Billy, age: 17
# name: Cark, age: 19
result2 = Table('user').condition('age','>=',17).orderBy('age','d').get()
for r in result2:
  print(f'name: {r["name"]}, age: {r["age"]}')
# name: Cark, age: 19
# name: Billy, age: 17

```

#### distinct 

Use this with a query where you are constraining the result set to a limited number of columns. In such a scenario, you may wish to ensure the result set does not include duplicate entries. This method cannot terminate a query.

```
result = Table('user').distinct().pluck('name')
```

#### columns 

Use this method to specify that you wish your query to target a certain selection of columns rather than just the default (i.e. *). The one required parameter is a list or tuple of column names. This method cannot terminate a query.

```
result = Table('user').columns(('name','age')).get()
for r in result:
  print(f'name: {r["name"]}, age: {r["age"]}')
# name: Billy, age: 17
# name: Jodi, age: 15
# name: Cark, age: 19
```

#### insertGetId

Almost the same as the `insert` method except you can/should only attempt to insert one record at a time, and it will return the id of the newly created record to you directly as a scalar value. This method does not work with `Table`'s `setConnection` method.

```
id = Table('user').insertGetId(('name','age'),('Tom',27))
print(id) # 4
```

#### average 

Used to terminate a select query. Can be, optionally, chained after conditions are added to query via another method. Required to pass a single column name, whose values you want averaged, into this method. Returns the scalar value directly.

#### condition 

Defining a single (i.e. not compound) `Where` condition for a query is easy. This method cannot terminate a query.

```
results = Table('user').condition('age','>=',18).get()
```

#### limit 

This method cannot terminate a query. Must pass in an integral value indicating the max number of results you want in the result set.

#### update 

Two arguments are required. First is a list of columns to update. The second is a list of values for the update in the order specified in the first argument. Note that if you don't chain at least one condition before terminating a query with this method, you will end up updating every single record in the table that your query targets.

```
Table('user').condition('id','=',3).update(('name','age'),('Carky',20))
```

#### count

This method terminates a select query. Can use it with or without previpusly chained conditions. Optional argument is column to count; if none is provided, '*' is assumed. Returns a scalar value directly.

#### exists 

Utilizes `count` method to determine if at least one such record exists, returning an appropriate boolean.

#### doesntExist

Opposite of `exists`.

#### maximum 

Same as `count`, but returns largest value of specified column in result set.

#### minimum

Same as `maximum`, but... you get it.

#### delete

No arguments for this method. Warning: if you don't chain conditions bwfore calling this method, literally all records in the targeted table are going to be deleted.

#### vacuum 

The only method you can call via a `Table` object without specifying a table in the constructor. No, it probably doesn't belong here but it's okay. Calls SQLite's vacuum functionality. Doesn't support 'VACUUM INTO' because not all SQLite versions support it. To vacuum a different database file than the currently configured one, write your own vacuum method lol. This method does not work with `Table`'s `setConnection` method.

#### setConnection 

Pass in a connection string to use a different database connection than the one currently specified in configuration file. After calling this method, continue chaining methods to build your query. Not compatible with `vacuum` or `insertGetId`.

#### chunk

This works, I hope, similarly to Laravel's chunk method. First argument is an integral value indicating the max number of records to pull from the database at a time to feed one-by-one into the callback function provided as the second argument. Do not mutate the database in the callback function or anomalous behavior can occur. If you need that functionality, use `chunkById`. Under the hood this method uses limits and offsets to paginate 

#### chunkById

Very similar to `chunk` except you can mutate the database in your callback. As with `chunk`, you may use conditions with a query terminated by this method because it uses the `prependCondition` and `setCondition` methods of the `Where` object under the hood to dynamically make sure the smallest id of each chunk of results retrieved from the database is larger than the largest id of the previously retrieved chunk of results. Takes the same arguments as `chunk`.

### `Where` class

The key to understanding the `Where` class is the format of the conditions that you pass in. Unlike the framework that inspired this query builder, I did not want to spend a lot of time creating a long host of methods to enable complex combinations of nested conditions. At the same time, I did want to enable the most complex combinations of nested conditions. 

In the end, the compromise is a fully functional yet admittedly not so user-friendly format for defining where conditions. What this means really is that it takes more work than it otherwise might with other query builders to construct simpler where condition clauses, but once you learn enough to specify more complex where condition clauses you might find it less intimidating than alternative approaches (and I might be projecting a bit with the last part). The conditions list that you make can be nested arbitrarily deep as a recursive algorithm is used to parse the conditions into the logically appropriate string for the query.

After you pass the conditions into the `Where` constructor, there are four methods available to you on the resulting object:
- getConditionString
- getParams
- prependCondition
- setCondition
- parse

Typically you won't need to call these methods yourself. They will usually be called internally by the Table object after you pass the Where object into the Table object's `conditions` method.

A quick note, since so many times you really only need one query constraint/condition, I had mercy and made a simple method onthe `Table` class called `condition` (note the method name's singularity) where you can easily specify a single condition for the query via three parameters without fussing with instantiating a `Where` object yourself. The first parameter is the column name, the second is the operator, and the third is the value (e.g. 'id', '<', 5).

Let's move on to some examples for `Where` objects. 

This is how you would make the `Where` object for the single `condition` method example above:

```
c = [
  {
    'type': 'single',
    'condition': ('id', '<', 5)
  }
]

w = Where(c)

w.parse()

w.getConditionString()
# Output: 'WHERE (id < ?)'
w.getParams()
# Output: [5]
```

Note that if the third entry of the condition in a 'single' type dictionary is not a string and is an iterable sequence like a list or tuple, it is assumed you are going to be building the following type of condition:

```
c = [
  {
    'type':'single',
    'condition': ('userId', 'NOT IN', [2, 3, 7, 9])
  }
]

w = Where(c)

w.parse()

w.getConditionString()
# Output: 'WHERE (userId NOT IN (?, ?, ?, ?))'
w.getParams()
# Output: [2, 3, 7, 9]
```

A bit more complicated of an example. Note that the first entry within a list, no matter how nested (or not) that list is within the condition definition, is the only entry without an `operator` key.

```
c = [
  {
    'type': 'series',
    'series': [
      {
        'type': 'single',
        'condition': ('x', '=', 1)
      },{
        'type': 'single',
        'operator': 'AND',
        'condition': ('y', '=', 2)
      }
    ]
  },{
    'type': 'single',
    'operator': 'OR',
    'condition': ('z', '=', 3)
  }
]

w = Where(c)

w.parse()

w.getConditionString()
# Output: 'WHERE (((x = ?) AND (y = ?)) OR z = ?)'
w.getParams()
# Output: [1, 2, 3]
```