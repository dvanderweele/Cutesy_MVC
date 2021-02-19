from datetime import datetime
from framework.helpers import migrate
from framework.helpers.db import Where, Table

def getNixTs():
  return datetime.now().timestamp()
  
def nixTsToDateTime(ts):
  return datetime.fromtimestamp(ts)

def hyphenatedTsStr():
  parts = str(datetime.now().timestamp()).split('.')
  return f'{parts[0]}-{parts[1]}'
  
def floatTsFromHyphenFormat(tstring):
  parts = tstring.split('-')
  joined = f'{parts[0]}.{parts[1]}'
  return float(joined)
  
print(getNixTs())
print(nixTsToDateTime(getNixTs()))
print(hyphenatedTsStr())
print(floatTsFromHyphenFormat(hyphenatedTsStr()))
  
  
wh = [{
  'type': 'series',
  'series': [{
    'type': 'single',
    'condition': ('x', '=', '1')
  },{
    'type': 'single',
    'operator': 'AND',
    'condition': ('y', '=', '2')
  }]
},{
  'type': 'single',
  'operator': 'OR',
  'condition': ('z', '=', '3')
},{
  'type': 'series',
  'operator': 'AND',
  'series': [{
    'type': 'single',
    'condition': ('x', '=', '1')
  },{
    'type': 'single',
    'operator': 'AND',
    'condition': ('y', '=', '2')
  }]
}]

wo = Where(wh)
print(wo.getConditionString())

