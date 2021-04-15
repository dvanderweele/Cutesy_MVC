"""
Defines two classes for creating and running suites of tests.
"""
import sys

class Test:
    """
    Define and run a test case.

    Parameters
    ----------
    name : str
           The name of the test case, for use in output.
    callback
           Must be a callback function that performs testing logic and returns a boolean indicating whether the test was successful (True) or not (False).

    Attributes
    ----------
    name : str
           The name of the test case.
    cb
           The user-provided callback for the test case.
    passes : bool
           Indicates whether the `cb` function returned True
    fails : bool
           Indicates whether the `cb` function returned False
    """
    def __init__(self, name, callback):
        self.name = name
        self.cb = callback
        self.passes = False
        self.fails = False

    def __str__(self):
        return f'---------------\nTest "{self.name}":\nRan - {self.ran()}\nPassed - {self.passes}\nFailed - {self.fails}'

    def ran(self):
        """
        Indicates whether the test case was ran yet by looking at the `self.passes` and `self.fails` booleans.
        Returns
        -------
        bool
        """
        if not self.passes and not self.fails:
            return False
        else:
            return True

    def run(self):
        """
        Run the user-provided test function and record whether it passes or not.
        """
        passed = False
        try:
            passed = self.cb()
        except:
            print(f'---------------\nTest "{self.name}" encountered an error:\nType: {sys.exc_info()[0]}\nValue: {sys.exc_info()[1]}\nTraceback: {sys.exc_info()[2]}')
        finally:
            if passed:
                self.passes = True
            else:
                self.fails = True


class Suite:
    """
    A class data structure for holding and running multiple `Test`s.

    Parameters
    ----------
    name : str
          The name of the test suite.
    tests : iterable of `Test` objects
    """
    def __init__(self, name, tests):
        self.__tests = tests
        self.passes = 0
        self.fails = 0
        self.name = name

    def run(self):
        """
        Run all the tests.
        """
        for test in self.__tests:
            test.run()
            if test.passes:
                self.passes += 1
            else:
                self.fails += 1
            print(test)

    def __str__(self):
        """
        Print the ratio of tests that passed and failed.
        """
        return f'---------------\nTEST SUITE "{self.name}"\nTests Passing: {self.passes}\nTests Failing: {self.fails}\nPercent Passing: {(self.passes / (self.passes + self.fails)) * 100}%\n==============='
