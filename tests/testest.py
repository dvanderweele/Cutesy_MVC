from ..linker import helpers

Test = helpers.test.Test
Suite = helpers.test.Suite

def y():
    throws = False
    try:
        2 / 0
    except:
        throws = True
    finally:
        return throws

t1 = Test('Zero Division', y)
t2 = Test('Proper Division', lambda x=1: True)

tsuite = Suite('Testest', [t1, t2])
