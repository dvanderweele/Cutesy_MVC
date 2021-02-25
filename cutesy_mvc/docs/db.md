# Database Tools

Only SQLite is supported at this time. Not all database classes and methods are documented here simply because some of them only exist to power the migration system. 

## QueryBuilder

These tools are inspired heavily by the Laravel framework's query builder tools, albeit with far less functionality. 

### `Table` class 

Methods:
- 

### `Where` class

The key to understanding the `Where` class is the format of the conditions that you pass in. Unlike the framework that inspired this query builder, I did not want to spend a lot of time creating a long host of methods to enable complex combinations of nested conditions. At the same time, I did want to enable the most complex combinations of nested conditions. 

In the end, the compromise is a fully functional yet admittedly not so user-friendly format for defining where conditions. What this means really is that it takes more work than it otherwise might with other query builders to construct simpler where condition clauses, but once you learn enough to specify more complex where condition clauses you might find it less intimidating than alternative approaches (and I might be projecting a bit with the last part). The conditions list that you make can be nested arbitrarily deep as a recursive algorithm is used to parse the conditions into the logically appropriate string for the query.

After you pass the conditions into the `Where` constructor, there are two methods available to you on the resulting object:
- getConditionString
- getParams

Typically you won't need to call these methods yourself. They will usually be called internally by the Table object after you pass the Where object into the Table object's constructor. 

Let's move on to some examples.