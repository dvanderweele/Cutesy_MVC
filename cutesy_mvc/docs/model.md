# Models 

## The `Model` class 

User-defined models should extend the `Model` class, which provides a lot of convenient functionality — most of which is built on top of the query builder. 

One of the most obvious factors in your successful usage of the model system is ensuring that your models and migrations correspond to one another coherently. For instance, if your model is expecting timestamp columns and you did not define any in your migration(s), you will run into problems.

It is important that the `Model` base class constructor runs. It is not required to define a constructor for user-defined models.

Finally, unlike some other frameworks, the table targeted by your model will not be inferred from the name of your model. You must specify the name of the table your model targets in the `table` class attribute within your user-defined model. 

### `connection`

This attribute is set by default in the `Model` base class to the currently configured database connection. You can override it and redefine it to another database connection in any individual user-defined model. Otherwise, don't bother defining the attribute in your user-defined model.

```
from ..helpers.model import Model

class PurchaseHistoryItem(Model):
  connection = 'analysis.db'
  table = 'purchase_history_item'
```

### `softDeletes`

By default this is set to `False` in the `Model` parent class. If you set it to true in your derived model class, you must make sure the targeted table has a nullable column of the `Real` type called `deleted_at`. Enabling soft deletion functionality allows you to use a number of methods discussed below to include or exclude "trashed" records. When a model is soft deleted, instead of being removed from the database, a timestamp is stored in its `deleted_at` column. 

### `timestamps`

By default, this is set to `True` in the `Model` base class. You can turn it off by setting it to `False` in your derived class. When it is turned on, records will be timestamped when they are created and whenever they are updated via the Model system. 

### `getOriginal`



### `isDirty`



### `isClean`



### `hydrated`



### `trashed`



### `withTrashed`



### `onlyTrashed`



### `allModels`



### `fresh`



### `find`



### `save`



### `limit`



### `orderBy`



### `condition`



### `conditions`



### `get`



### `chunk`



### `chunkById`



### `delete`



### `destroy`



### `hasOne`



### `hasMany`



### `belongsTo`



### `belongsToMany`