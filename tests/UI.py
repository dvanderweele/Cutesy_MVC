from ..cutesy_mvc import helpers

Test = helpers.test.Test
Suite = helpers.test.Suite
State = helpers.UI.State

def t1c():
    cle = 'abc!'
    State.add(cle, 42)
    passes = True
    if State.get(cle) != 42:
        passes = False
    if cle is not 'abc!':
        passes = False
    return True
t1 = Test('State.add,get', t1c)
def t2c():
    State.set('abc', 43)
    passes = True
    if State.get('abc') != 43 or \
            State.get('abc!') != 42:
        passes = False
    State.set('abc!', 44)
    if State.get('abc!') != 44:
        passes = False
    return passes
t2 = Test('State.set,get', t2c)
def t3c():
    a = State.pop('abc!')
    passes = True
    if a != 44 or 'abc!' in State.store.keys():
        passes = False
    if State.has('abc!'):
        passes = False
    return passes
t3 = Test('State.pop,has', t3c)
tests = [t1, t2, t3]

uiSuite = Suite("UI.State", tests)
