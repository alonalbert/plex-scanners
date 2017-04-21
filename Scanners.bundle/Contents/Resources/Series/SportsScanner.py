import re
import os
import Media
import Stack
import Utils
import datetime
import VideoFiles

class RegexHandler(object):
  def handle(self, match, file):
    pass
  def getRegexs(self):
    return []


class UfcHandler(RegexHandler):
  PATTERN = 'ufc (?P<episode>\d+) ?(?P<title>.*)?'

  def getRegexs(self):
    return [
      'ufc',
    ]

  def handle(self, match, file):
    show = 'UFC'
    name, year = VideoFiles.CleanName(os.path.basename(file))
    m = re.match(self.PATTERN, name, re.IGNORECASE)
    if not m:
      return None
    episode = m.group('episode')
    title = m.group('title')
    if year is None and os.path.exists(file):
      year = getYearFromFile(file)

    return Media.Episode(show, year, episode, title, year)

class F1Handler(RegexHandler):
  WEEKEND_BUNDLE_RE = re.compile('^(.*).formula1.(?P<year>\d+).r(?P<round>\d+).(?P<name>.*).Gran.Prix.(?P<show>.*)', re.IGNORECASE)
  P1_RE = re.compile('(.*practice.(one|1))|p1', re.IGNORECASE)
  P2_RE = re.compile('(.*practice.(two|2))|p2', re.IGNORECASE)
  P3_RE = re.compile('(.*practice.(three|3))|p1', re.IGNORECASE)
  Q_RE = re.compile('quali', re.IGNORECASE)
  RACE_RE = re.compile('race', re.IGNORECASE)
  TED_RE = re.compile('ted.*qualifying.notebook', re.IGNORECASE)

  SCHEDULE = {
    '2017' : [
      'Australia',
      'China',
      'Bahrain',
      'Russia',
      'Spain',
      'Monaco',
      'Canada',
      'Azerbaijan',
      'Austria',
      'Great Britain',
      'Hungary',
      'Belgium',
      'Italy',
      'Singapore',
      'Malaysia',
      'Japan',
      'United States',
      'Mexico',
      'Brazil',
      'Abu Dhabi',
    ]
  }

  LOCATION_ALIASES = {
    'Australian': 'Australia',
    'Australia': 'Australia',
    'Chinese': 'China',
    'China': 'China',
    'Bahrain': 'Bahrain',
    'Russian': 'Russia',
    'Russia': 'Russia',
    'Spanish': 'Spain',
    'Spain': 'Spain',
    'Canadian': 'Canada',
    'Canada': 'Canada',
    'Azerbaijanian': 'Azerbaijan',
    'Azerbaijan': 'Azerbaijan',
    'Austrian': 'Austria',
    'Austria': 'Austria',
    'British': 'Great Britain',
    'Great.Britain': 'Great Britain',
    'Hungarian': 'Hungary',
    'Hungary': 'Hungary',
    'Belgium': 'Belgium',
    'Italian': 'Italy',
    'Italy': 'Italy',
    'Singapore': 'Singapore',
    'Malaysian': 'Malaysia',
    'Malaysia': 'Malaysia',
    'Japanese': 'Japan',
    'Japane': 'Japan',
    'American': 'United States',
    'United.States': 'United States',
    'Mexican': 'Mexico',
    'Mexico': 'Mexico',
    'Brazilian': 'Brazil',
    'Brazil': 'Brazil',
    'Abu Dahbi': 'Abu Dahbi',
  }

  def getRegexs(self):
    return [
      'Formula.?1.*',
    ]

  def handle(self, match, file):
    basename = os.path.splitext(file)[0]
    m = self.WEEKEND_BUNDLE_RE.match(basename)
    if m:
      year = m.group('year')
      round = int(m.group('round'))
      name = m.group('name') + ' Gran Prix'
      show = m.group('show').replace('.', ' ')
      show, part, title = self.getShowAndPart(show)
      location = self.SCHEDULE[year][round]
      show = '%s %02d %s' % (show, round, location)
      return Media.Episode(show, year, round * 100 + part, name + ' ' + title, year)
    else:
      for alias, location in self.LOCATION_ALIASES.iteritems():
        if not re.search(alias, file, re.IGNORECASE):
          continue
        yearMatch = re.search(r'[^\d](2\d\d\d)[^\d]', file, re.IGNORECASE)
        if yearMatch is None:
          year = getYearFromFile(file)
        else:
          year = int(yearMatch.group(1))
        round = self.SCHEDULE[str(year)].index(location) + 1
        name = location + ' Gran Prix'
        show, part, title = self.getShowAndPart(file)

        show = '%s %02d %s' % (show, round, location)
        return Media.Episode(show, year, round * 100 + part, name + ' ' + title, year)

  def getShowAndPart(self, show):
    lower = show.lower()
    if self.P1_RE.search(show):
      return 'F1', 11, 'Practice 1'
    elif self.P2_RE.search(show):
      return 'F1', 12, 'Practice 2'
    elif self.P3_RE.search(show):
      return 'F1', 13, 'Practice 3'
    elif self.Q_RE.search(show):
      if 'pre' in lower:
        return 'F1', 21, 'Pre Qualifying'
      elif 'post' in lower:
        return 'F1', 23, 'Post Qualifying'
      else:
        return 'F1', 22, 'Qualifying'
    elif self.RACE_RE.search(show):
      if 'pre' in lower:
        return 'F1', 31, 'Pre Race'
      elif 'post' in lower:
        return 'F1', 33, 'Post Race'
      else:
        return 'F1', 32, 'Race'
    elif 'f1 report' in lower:
      return 'F1 Extras', 1, 'The F1 Report'
    elif 'driver press' in lower:
      return 'F1 Extras', 2, 'Driver Press Conference'
    elif 'paddock' in lower:
      return 'F1 Extras', 3, 'Paddock Uncut'
    elif self.TED_RE.search(show):
      return 'F1 Extras', 4, "Ted's Qualifying Notebook"
    elif 'team principal' in lower:
      return 'F1 Extras', 5, 'Team Principal Press Conference'
    elif 'f1 show' in lower:
      return 'F1 Extras', 6, 'The F1 Show'
    else:
      if 'pre' in lower:
        return 'F1', 31, 'Pre Race'
      elif 'post' in lower:
        return 'F1', 33, 'Post Race'
      else:
        return 'F1', 32, 'Race'

    pass


REGEX_HANDLERS = [
  UfcHandler(),
  F1Handler(),
]

def handle(file):
  basename = os.path.basename(file)
  for handler in REGEX_HANDLERS:
    for regex in handler.getRegexs():
      match = re.search(regex, file, re.IGNORECASE)
      if match:
        return handler.handle(match, file)


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  # Scan for video files.
  VideoFiles.Scan(path, files, mediaList, subdirs)
  scanFiles(files, mediaList)


def scanFiles(files, mediaList):
  for file in files:
    show = handle(file)
    if show is not None:
      show.parts.append(file)
      mediaList.append(show)


def getYearFromFile(file) :
  time = os.stat(file).st_ctime
  #returns a datetime object
  dt = datetime.datetime.fromtimestamp(time)
  return dt.year
