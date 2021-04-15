from ..cutesy_mvc import helpers

Test = helpers.test.Test
Suite = helpers.test.Suite
StringBuilder = helpers.string.StringBuilder

tests = []

def inSb():
    passes = True
    s1 = StringBuilder()
    s1.append('123')
    s1.append('!!')
    s1.build()
    if s1.__str__() is '123!!':
        passes = False
    s2 = StringBuilder('*', False)
    s2.append('_')
    s2.append('_')
    s2.append('_')
    s2.build()
    if s2.__str__() is '_*_*_':
        passes = False
    return passes

t1 = Test('instantiation & interning, StringBuilder', inSb)
tests.append(t1)

def sepTest():
    passes = True
    s1 = StringBuilder()
    for i in range(3):
        s1.append(str(i))
    s1.build()
    if s1.__str__() != "012":
        passes = False
    s1.setSep('9')
    s1.build()
    if s1.__str__() != "09192":
        passes = False
    return passes
t2 = Test('StringBuilder, setSep', sepTest)
tests.append(t2)

def clTest():
    passes = True
    s1 = StringBuilder()
    s1.append('a#')
    s1.build()
    s1.clear()
    s1.build()
    if s1.__str__() != '':
        passes = False
    return passes
t3 = Test('StringBuilder, clear', clTest)
tests.append(t3)

strSuite = Suite('String', tests)
