# Models 

## The `Model` class 

User-defined models should extend the `Model` class, which provides a lot of convenient functionality — most of which is built on top of the query builder. 

One of the most obvious factors in your successful usage of the model system is ensuring that your models and migrations correspond to one another coherently. For instance, if your model is expecting timestamp columns and you did not define any in your migration(s), you will run into problems.

It is important that the `Model` base class constructor runs. It is not required to define a constructor for user-defined models.

Finally, unlike some other frameworks, the table targeted by your model will not be inferred from the name of your model. You must specify the name of the table your model targets in the `table` class attribute within your user-defined model. 

### `connection`

This attribute is set by default in the `Model` base class to the currently configured database connection. You can override it and redefine it to another database connection in any individual user-defined model. Otherwise, don't bother defining the attribute in your user-defined model.

```python
from ..helpers.model import Model

class PurchaseHistoryItem(Model):
  connection = 'analysis.db'
  table = 'purchase_history_item'
```

### `softDeletes`

By default this is set to `False` in the `Model` parent class. If you set it to true in your derived model class, you must make sure the targeted table has a nullable column of the `Real` type called `deleted_at`. Enabling soft deletion functionality allows you to use a number of methods discussed below to include or exclude "trashed" records. When a model is soft deleted, instead of being removed from the database, a timestamp is stored in its `deleted_at` column. 

### `timestamps`

By default, this is set to `True` in the `Model` base class. You can turn it off by setting it to `False` in your derived class. When it is turned on, records will be timestamped when they are created and whenever they are updated via the Model system. 

### `isSameModel` and `isNotSameModel`

Pass in another model to either of these methods to determine if the models are the same model or not (comparing primary key, table, and database connection).

### `getOriginal`

Even if you have mutated your model since it was hydrated from or pushed to the database, this method will return its original attributes.

### `hydrated`

Tells you if all attributes that are not `nullable` have been filled.

### `trashed`

Returns a boolean indicating whether a model has been soft deleted or not.

### `withTrashed`

Chainable method for queries to indicate the result set of models should include soft deleted records.

### `onlyTrashed`

Chainable method for queries indicating the result set of models should only include soft deleted models.

### `allModels`

Get all models from a table. Can be used in conjunction with a `limit`. By default does not include soft deleted models.

### `fresh`

Hit the database again and re-hydrate model with fresh data.

### `refresh`

The same as the `fresh` method but all currently loaded relationships will be re-hydrated as well.

### `find`

Pass in an `id` of a model you want. By default does not consider soft deleted models. Returns `None` if none is found.

### `save`

To persist a new model, call this method after setting required attributes on a freshly instantiated model. Also call this method after altering a model's attributes to update the record in the database.

### `limit`

Chainable method that works like the query builder's `limit` method.

### `orderBy`

Pass in an attribute/column and optionally 'asc' (the default) or 'dsc' to sort result set of models accordingly.

### `condition`

Like the method of the same name on the query builder.

### `conditions`

Like the method of the same name on the query builder.

### `get`

Like the method of the same name on the query builder.

### `chunk`

Like the method of the same name on the query builder.

### `chunkById`

Like the method of the same name on the query builder.

### `delete`

If soft deletes are enabled, will soft delete the model. Otherwise, this method will really delete the model. 

### `forceDelete`

Even if soft deletes are enabled, this will really delete the model.

### `destroy`

Pass in an `id` to target for deletion. Exactly like `delete` except model is not loadedbefore record is deleted (or soft deleted) in database.

### `restore`

Remove soft deleted status from current model.

### Defining `relations` 

If you wish to define relations for a user-defined model, you will define them in a dictionary on the class attribute `relations` within your user-defined model. The keys of the dictionary will be names that you will use to refer to the relations when loading them. 

#### `_index.py`

A file called `_index.py` must be found in the `models` directory. In it, you must have a registry variable that defines a dictionary where the keys are strings you will use to refer to the classes stores as values. For example:

```python
# _index.py 
from .BlogPost import BlogPost
from .Comment import Comment 

registry = {
    'BlogPost': BlogPost,
    'Comment': Comment
}

```

In the above example, you are importing the user-defined model classes `BlogPost` and `Comment` from the `BlogPost.py` and `Comment.py` files respectively in the same directory. the keys you assign them to in the registry dictionary will be used in your relation definitions in your user-defined models. You must register all of your user-defined models here if they will be participating in a relationship.

#### `hasOne`

Look at the following example:

```python
from ..helpers.model import Model

class Apartment(Model):
  table = 'apartment'
  relations = {
    'tenant': {
      'type': 'hasOne',
      'model': 'Tenant'
    }
  }
```

It will be assumed that the table at the connection defined for the `Tenant` model (note that the `'Tenant'` string is the key for the `Tenant` model class in the`_index.py` registry we just discussed) will have a foreign key column named after the `Apartment` model's table name plus `_id` concatenated (i.e. `apartment_id`). If you name the foreign key column something else, define its name as follows:

```python
from ..helpers.model import Model

class Apartment(Model):
  table = 'apartment'
  relations = {
    'tenant': {
      'type': 'hasOne',
      'model': 'Tenant',
      'foreign': 'unit_number'
    }
  }
```
This type of relation allows you to define a `default` dictionary of key-value pairs to use in the event that result of the relationship query is `null`.

```python
from ..helpers.model import Model

class Apartment(Model):
  table = 'tenant'
  relations = {
    'tenant': {
      'type': 'hasOne',
      'model': 'Tenant',
      'default': {
        'id': 0,
        'name': 'Vacant (No Tenant)',
        'ssn': 0
      }
    }
  }
```

#### `hasMany`

Define this type of relation in exactly the same fashion as the `hasOne` relationship, except with the `hasMany` keyword.


```python
from ..helpers.model import Model

class User(Model):
  table = 'user'
  relations = {
    'apartment': {
      'type': 'hasOne',
      'model': 'Apartment',
    },
    'parkingSpace': {
      'type': 'hasMany',
      'model': 'ParkingSpace'
    }
  }
```

#### `belongsTo`

This type of relation is the inverse of both the `hasOne` and `hasMany` types. Note that if you define a 'foreign' attribute it refers to the foreign key column name in the table referenced by the model that the relation is defined on (i.e. in the following example, the `id_of_tenant` column in the `parking_space` table). Also, if you wish an update to or deletion of this child model to update the timestamp of the parent model, add a `touch` class attribute to the child model with a list containing the names of the relationships to which that rule applies. This "touching" will not occur if a database record is deleted without a corresponding model being hydrated.

```python
from ..helpers.model import Model 

class ParkingSpace(Model):
  table = 'parking_space'
  touch = ('tenant',)
  relations = {
    'tenant': {
      'type': 'belongsTo',
      'model': 'Tenant',
      'foreign': 'id_of_tenant'
    }
  }
```

Like the `hasOne` relationship, you can define a `default` dictionary of key-value pairs to use in lieu of a real database record when the relation turns up `null`.

```python
from ..helpers.model import Model 

class ParkingSpace(Model):
  table = 'parking_space'
  touch = ('tenant',)
  relations = {
    'tenant': {
      'type': 'belongsTo',
      'model': 'Tenant',
      'default': {
        'id': '0',
        'description': 'Guest Parking Space'
      }
    }
  }
```

#### `belongsToMany`

This type is used in defining both sides of a many-to-many relationship. Also, like the `belongsTo` relationship type, you can define a `touch` attribute on the class to indicate you want the related model to have its timestamp updated when this model is updated. With this type of relationship, the timestamp touching rule can go one way or both ways (or neither at all of course if you don't define it in either model).

```python
from ..helpers.model import Model

class Student(Model):
  table = 'student'
  relations = {
    'Courses': {
      'type': 'belongsToMany',
      'model': 'Course',
      'pivot': 'Schedule'
    }
  }
```

```python
from..helpers.model import Model

class Course(Model):
  table = 'course'
  touch = ('students',)
  relations = {
    'students': {
      'type': 'belongsToMany',
      'model': 'Student',
      'pivot': 'Schedule'
    }
  }
```

In the `courses` relationship below, the `foreign` key is the column name in the pivot table (whose model in this case is `Schedule`) that contains `id`s of records in the `course` table. The `local` key refers to the column in the pivot table that contains `id`s of records in the `student` table.

```python
from ..helpers.model import Model

class Student(Model):
  table = 'student'
  relations = {
    'courses': {
      'type': 'belongsToMany',
      'model': 'Course',
      'foreign': 'id_of_course',
      'local': 'id_of_student',
      'pivot': 'Schedule'
    }
  }
```

```python
from ..helpers.model import Model 

class Course(Model):
  table = 'course'
  touch = ('students',)
  relations = {
    'students': {
      'type': 'belongsToMany',
      'model': 'Student',
      'foreign': 'id_of_student',
      'local': 'id_of_course',
      'pivot': 'Schedule'
    }
  }
```

Pivot tables will not be inferred. You must explicitly define their existence with a user-defined model that extends the `Model` class. There is no special `Pivot` class. You must explicitly define the pivot table name in that model. Customizing the connection is optional. Pivot tables should not use composite primary keys, but an incrementing primary key column named `id`. By default timestamps are turned on for pivot models just like all other models, so turn them off if you need to do so. 

In the event that you want to use timestamps for your pivot model, the `updated_at` timestamp in most cases won't ever be updated, even when a timestamp touch 'event' travels through the model. In order to directly access the pivot model, access it via the 'pivot' attribute on a model hydrated as a result of a relationship loading. From there you can update the timestamp as needed.

```python
from ..helpers.model import Model 

class Schedule(Model):
  table = 'schedule' 
  connection = 'pivots.db'
  timestamps = True
```

#### `morphOne` and `morphTo`

At this point I'm pretty transparently ripping off Laravel's naming conventions for polymorphic model relationships. However, they make a lot of sense, and this is just a learning project for me. 

A polymorphic one-to-one relationship is a lot like the normal one-to-one relationships defined by `hasOne` and `belongsTo` as discussed above. However, the model in the relationship that defines the `belongsTo` aspect of the relationship in this case may belong to two or more types of other models. This works because, in addition to the foreign key field, this model's table has another column that stores the type of model that foreign key belongs to in string format.

The `morphOne` part of the relationship is the polymorphic equivalent of `hasOne`. The `morphTo` relationship is defined on the tricky model that can belong to multiple types of other models.

In the case of a model defining one or more `morphTo` relations, you must also define a class member variable called `owners`. It should contain a relevant list of keys from the model `_index.py` registry that are found in the `able_type` column and whose values are the corresponding model classes.

```python
from ..helpers.model import Model

class Post(Model):
  table = 'post'
  relations = {
    'comment': {
      'type': 'morphOne',
      'model': 'Comment'
    }
  }
```
```python
from ..helpers.model import Model

class Video(Model):
  table = 'video'
  relations = {
    'comment': {
      'type': 'morphOne',
      'model': 'Comment'
    }
  }
```
```python
from ..helpers.model import Model

class Comment(Model):
  table = 'comment'
  touch = ('commentable',)
  owners = ('Post','Video')
  relations = {
    'commentable': {
      'type': 'morphTo'
    }
  }
```

In this case, the `comment` table will have a foreign key column named `commentable_id` and another column called `commentable_type`. The names of these columns are non-negotiable and derived from concatenating `able_id` and `able_type` onto the end of the table name. You don't need to name the relation `commentable`, but I like that convention. Note that like `belongsTo` relations, you can specify that you wish an update to this model to propagate an update to the timestamp of the related model. Also, like the ordinary `hasOne` and `belongsTo` 
relation types, you can define a `default` dictionary of key-value pairs, for both `morphTo` and `morphOne` relations, to return if the relationship query turns up `null`.

#### `morphMany` 

This is for defining one-to-many polymorphic relationships. Defining one-to-many polymorphic relationships works exactly like defining one-to-one relationships, but `morphMany` will take the place of `morphOne`.

#### `morphToMany` and `morphedByMany`

Many-to-many polymorphic relationships are for cool people only. Imagine that an application supports `Hashtag`s. There are many `Hashtag`s, and each one can also be associated with many `Post`s. Additionally, each `Post` can support multiple `Hashtag`s. The complicating factor for this application is that `Comment`s can also have multiple `Hashtag`s. 

For this you will need to define four models: `Post`, `Comment`, `Hashtag`, `Hashtagable`. 

```python
from ..helpers.model import Model

class Post(Model):
  table = 'post'
  relations = {
    'hashtags': {
      'type': 'morphedByMany',
      'model': 'Hashtag',
      'pivot': 'Hashtagable'
    }
  }
```

```python
from ..helpers.model import Model

class Comment(Model):
  table = 'comment'
  relations = {
    'hashtags': {
      'type': 'morphedByMany',
      'model': 'Hashtag',
      'pivot': 'Hashtagable'
    }
  }
```

```python
from ..helpers.model import model

class Hashtag(Model):
  table = 'hashtag'
  touch = ('hashtagables',)
  relations = {
    'hashtagables': {
      'type': 'morphToMany',
      'pivot': 'Hashtagable'
    }
  }
```

```python
from ..helpers import Model

class Hashtagable(Model):
  table = 'hashtagable'
  morphs = ('Comment','Post')
  relations = {
    'hashtag': {
      'type': 'poly',
      'model': 'Hashtag'
    }
  }
```

It will be assumed, no matter what you named your pivot class, that it contains an `id` column, a column named after the table plus `_id` concatenated (i.e. `hashtagable_id`), a column named after the table plus `_type` concatenated (i.e. `hashtagable_type`), and a column named after the table of the model defining the `morphToMany` relationship with `_id` concatenated (i.e. `hashtag_id`). 

Also note that the model playing the pivot role in a polymorphic many-to-many relationship (in this case `Hashtagable`) is expected to have a class member variable called `morphs` with a list containing all the `_index.py` registry keys found in its table's 'able_type' column.

Finally, note that in the example above, if you have a hydrated `Hashtag` model and you load the `hashtagables` relation, the list of hydrated models assigned to the `hashtagables` may contain models of both the `Post` and `Comment` types. This may be counterintuitive if you were expecting it to literally load a list of hydrated `Hashtagable` models. 

### Loading `relations`

#### `load`

After a model is hydrated, pass in the name of the one you want to the `load` function. Eager loading mechanisms are not suppported.