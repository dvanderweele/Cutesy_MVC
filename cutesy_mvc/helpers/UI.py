"""
Defines a class with five classmethods for maintaining a simple global application state dictionary, intended for use by the user-interface.
"""
from sys import intern

class State:
    """
    A simple class for maintaining global app state, requiring no instantiation.

    Attributes
    ----------
    store : dict
            A dictionary that is intended to be managed exclusively by way of the five available classmethods.
    """
    store = {}
    @classmethod
    def add(cls, key, value):
        """
        A class method for adding a new key-value pair to the `store` dictionary.

        Parameters
        ----------
        key : str
              Dictionary keys may ordinarily be of types other than strings, but in this case the key should be a string as it will be iterned to enhance lookup times.
        value
              The data value that you want stored in the `store` dictionary under the `key` key.
        """
        k = intern(key)
        cls.store[k] = value
    @classmethod
    def set(cls, key, value):
        """
        A class method for adding or mutating an existing key-value pair in the `store` dictionary.

        Parameters
        ----------
        key
              The key under which you wish to store the `value` in the `store` dictionary.
        value
              The data value that you want stored in the `store` dictionary under the `key` key. 
        """
        cls.store[key] = value
    @classmethod
    def pop(cls, key):
        """
        A class method to remove and return a key-value pair from the `store` without validation.

        Parameters
        ----------
        key
              The key of the value in the `store` dictionary that you want to remove and return.
        """
        return cls.store.pop(key)
    @classmethod
    def get(cls, key):
        """
        A class method to return the value stored in the `store` dictionary under the specified key, without validation.

        Parameters
        ----------
        key
              The key of the value you wish to have returned to you from the `store` dictionary.
        """
        return cls.store[key]
    @classmethod
    def has(cls, key):
        """
        A class method that will return a boolean indicating whether or not the given key is in use within the `store` dictionary.

        Parameters
        ----------
        key
              The key whose presence in the `store` dictionary you are querying.

        Returns
        -------
        boolean
              A boolean that indicates if the passed argument is in use as a key within the `store` dictionary (True) or not (False).
        """
        return key in cls.store.keys()

