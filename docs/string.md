## The `StringBuilder` Class

You can use this feature in many different situations to efficiently construct strings. 

### Constructor

There are two optional parameters for the constructor: `sep` and `internString`. The default value for the former is an empty string, and the latter's is the boolean `True`.

These arguments determine what happens when you call the `build` method. The string value of the `sep` parameter will be used to join all the string segments the object is currently holding. A `True` value for `InternString` will cause the resulting string to be interned.

### The `setSep` Method

Pass in a new string value to replace the `sep` value that was set at instantiation.

### The `setInternString` Method

Pass in a boolean value to replace the `internString` value that was set at instantiation.

### The `clear` Method

Call to reset the currenr string to an empty string and the list of string parts to an empty list.

### The `append` Method

Pass in a string value to add to the list of string parts. The `build` method uses that list to build a new string.

### The `build` Method

You must call this method after appending strings, setting a new separator, or changing the `internString` setting — and at least once after instantiation (unless you want an empty string returned to you when you call `__str__`).

### The `__str__` and `__repr__` Methods

The first returns the most recently built string, and the second returns a string repesenting the current internal state of the `StringBuilder` object.

