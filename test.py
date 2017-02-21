import re

import Wikipedia

SLIM_SLIM__JSON = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.json'
CALENDAR_REGEX = re.compile('^!(style[^|]+\|)?(?P<round>\d+)[^\w]*(?P<name>[^]]+)[^\w]*flagicon\|(?P<countryCode>.{3}).*\[\[(?P<circuit>[^]]+)\]\].*\[\[(?P<city>[^]]+)[^|]*[|\s]+(?P<day>\d+) (?P<month>\w+)')

ROUND_RE = re.compile('.*?(\d+)$')

content = Wikipedia.getContent('2016_Formula_One_season')

start = content.index('\n==Season calendar==')
end = content.index('\n==', start + 1)

calendarEntries = content[start:end].split('\n|-\n')

for entry in calendarEntries[2:-1]:
  lines = entry.split('\n')
  round = ROUND_RE.match(lines[0]).group(1)
  print 'Round: %s' % (round)
