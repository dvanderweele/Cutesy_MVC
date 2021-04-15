"""
Simple tool for building strings efficiently.
"""
from sys import intern

class StringBuilder:
    """
    A class for efficiently building strings.

    Attributes
    ----------
    sep : str, optional
          Defaults to an empty string, if specified will be used as the linking string for joining all the individual strings.
    internString : bool, optional
          Defaults to `True`, if so the resulting string of every build operation will be interned.
    """
    def __init__(self, sep = '', internString = True):
        self.__parts = []
        self.__sep = sep
        self.internString = internString
        self.string = ''
    def build(self):
        """
        This method constructs the string based on previously appended strings and currently set `sep` string.
        """
        if self.internString:
            self.string = intern(self.__sep.join(self.__parts))
        else:
            self.string = self.__sep.join(self.__parts)
    def setSep(self, sep):
        """
        Reset the `sep` string used when joining string parts.

        Parameters
        ----------
        sep : str
              The new string value to use as the joining material when building the new string.
        """
        self.__sep = sep
    def setInternString(self, value):
        """
        Reset the boolean used to determine whether built strings are interned.

        Parameters
        ----------
        value : bool
              The new boolean used to decide whether to intern (True) or not (False) the string produced by `build` method.
        """
        self.internString = value
    def clear(self):
        """
        Reset the last string value produced by the build method to an empty string, and empty the list of strings previously appended to the builder.
        """
        self.string = ''
        self.__parts = []
    def append(self, string):
        """
        Add a new string to the end of the list of strings to build the new string out of.

        Parameters
        ----------
        string : str
              The new string value to add to the list of string componenents. 
        """
        self.__parts.append(string)
    def __str__(self):
        """
        Returns most recently built string.
        """
        return self.string
    def __repr__(self):
        """
        Returns the current state of the String Builder Object formatted as a string.
        """
        return f'StringBuilder Object:\nString Parts: {self.__parts}, Current String: {self.string}\nCurrent Separator: {self.__sep}\nIntern String: {self.internString}'
