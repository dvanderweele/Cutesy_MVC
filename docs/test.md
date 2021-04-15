There are two classes to help you write tests for your application.

## The `Test` Class

Two arguments are required to instantiate a `Test` object: a name for the test in the form of a string and a callback function.

The name will be used to differentiate the tests from one another in the console output, so be as specific or vague as you like. 

The callback function can do whatever you want, but it must return a boolean indicating if your test case passes (True) or fails (False). If you need to test if an error is thrown in a specific scenario, structure your test callback function with try/except/finally blocks so you can return `True` from your callback if it throws as you expect. 

Your test callbacks will be run in try blocks as well so if one of them throws an error that isn't caught in your callback, it will be caught and helpfully described in the console output before proceeding with the rest of the tests.

After instantiating a `Test`, run it with the `run` method. To see if a `Test` was already run, call its `ran` method. 

## The `Suite` Class

Instantiate with a name for the entire `Suite` and a list or iterable of `Test` objects. To run all of the `Test`s in the `Suite`, call the `run` method. After running them, you can `print` the `Suite` object to get an overview of how they performed.

## `_index.py` File and Running `Test`s with `cutify`

In the tests directory is a file called `_index.py`. Place references to all of your instantiated `Suite`s in an iterable named `suites`. The `cutify` command `cutify test` can be invoked to run all those test suites.
