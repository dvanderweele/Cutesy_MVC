from .tests import _index

def main():
    suites = _index.suites
    passes = 0
    fails = 0
    for s in suites:
        s.run()
        print(s)
        passes += s.passes
        fails += s.fails
    print(f'###################\nSUMMARY OF ALL TEST SUITES\nTotal Passing Tests: {passes}\nTotal Failing Tests: {fails}\nPercent Passing: {(passes/(passes+fails)) * 100}%')

