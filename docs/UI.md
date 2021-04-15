# The `State` Class

This class does not require instantiation and can be used via its five `@classmethod`'s as a global application state store. The store itself is really just a python dictionary.

## The `set` Method

Both parameters are required, the first being the key and the second being the value.

## The 'add' Method

This is the same as the `set` method except it should be used whenever you want to insert a new top-level record in the store with a new string as its key. The key string will be interned for faster lookups in the future.

## The `pop` Method

A single key argument is required. The value in the store that the key refers will be removed from the store and returned to you.

## The `get` Method

Exactly like the `pop` method except the value is not removed from the store.

## The `has` Method

This method takes a key argument and will return a boolean value indicating whether the key is in use within the store dictionary. 
