from .helpers.cutify import handleCuteness
import sys

def run():
    if len(sys.argv) > 2:
        handleCuteness(sys.argv[2])
    else:
        pass

