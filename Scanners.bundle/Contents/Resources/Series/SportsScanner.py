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


class UfcFightNightHandler(RegexHandler):
  PATTERN = 'ufc fight night (?P<episode>\d+)'

  def getRegexs(self):
    return [
      'ufc.fight.night',
    ]

  def handle(self, match, file):
    show = 'UFC Fight Night'
    name, year = VideoFiles.CleanName(os.path.basename(file))
    m = re.match(self.PATTERN, name, re.IGNORECASE)
    if not m:
      return None
    episode = int(m.group('episode')) * 10
    title = ''
    if 'early' in name.lower():
      episode += 1
      title = 'Early Prelims'
    elif 'prelim' in name.lower():
      episode += 2
      title = 'Prelims'
    else:
      episode += 3
      title = 'Main Event'

    if year is None and os.path.exists(file):
      year = getYearFromFile(file)

    return Media.Episode(show, year, episode, title, year)

class UfcOnFoxHandler(RegexHandler):
  PATTERN = 'ufc on fox (?P<episode>\d+)'

  def getRegexs(self):
    return [
      'ufc.on.fox',
    ]

  def handle(self, match, file):
    show = 'UFC On Fox'
    name, year = VideoFiles.CleanName(os.path.basename(file))
    m = re.match(self.PATTERN, name, re.IGNORECASE)
    if not m:
      return None
    episode = int(m.group('episode')) * 10
    title = ''
    if 'early' in name.lower():
      episode += 1
      title = 'Early Prelims'
    elif 'prelim' in name.lower():
      episode += 2
      title = 'Prelims'
    else:
      episode += 3
      title = 'Main Event'

    if year is None and os.path.exists(file):
      year = getYearFromFile(file)

    return Media.Episode(show, year, episode, title, year)

class UfcGenericHandler(RegexHandler):

  def __init__(self, title):
    self.show_name = title

  PATTERN = '%s (?P<episode>\d+)'

  def getRegexs(self):
    return [
      self.show_name.replace(' ', '.'),
    ]

  def handle(self, match, file):
    show = self.show_name
    name, year = VideoFiles.CleanName(os.path.basename(file))
    m = re.match(self.PATTERN % self.show_name, name, re.IGNORECASE)
    if not m:
      return None
    episode = int(m.group('episode')) * 10
    title = ''
    if 'early' in name.lower():
      episode += 1
      title = 'Early Prelims'
    elif 'prelim' in name.lower():
      episode += 2
      title = 'Prelims'
    else:
      episode += 3
      title = 'Main Event'

    if year is None and os.path.exists(file):
      year = getYearFromFile(file)

    return Media.Episode(show, year, episode, title, year)

class WsopHandler(RegexHandler):
  PATTERN = 'world.series.of.poker.s?(?P<year>\d{4}).(?P<title>.*)'

  def getRegexs(self):
    return [
      'world.series.of.poker',
    ]

  def handle(self, match, file):
    show = 'WSOP'
    basename = os.path.basename(file)
    m = re.match(self.PATTERN, basename, re.IGNORECASE)
    if not m:
      return None
    year = int(m.group('year'))
    title = VideoFiles.CleanName(m.group('title'))[0]
    titleLower = title.lower()
    if 'preview' in titleLower:
      episode = 0
    elif "one drop" in titleLower:
      m = re.match('.*part ?(?P<day>\d+)', title, re.IGNORECASE)
      if not m:
        return None
      day = int(m.group('day'))
      episode = day * 10
    elif "main event" in titleLower:
      m = re.match('.*day ?(?P<day>\d+)(?P<part>[a-z]?)', title, re.IGNORECASE)
      if not m:
        return None
      day = int(m.group('day'))
      part = m.group('part')
      if "final table" in titleLower:
        episode = 200 + day * 10
      else:
        episode = 100 + day * 10
        if part != "":
          episode += ord(part[0]) - ord('a') + 1
        else:
          m = re.match(".*part.(?P<part>\d+)", title,re.IGNORECASE)
          if m:
            part = m.group('part')
            episode += int(part)

    else:
      return None

    return Media.Episode(show, year, episode, title, year)

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
    title = m.group('title')
    lower = title.lower()
    episode = int(m.group('episode')) * 10
    if "weigh" in lower:
      episode += 1
    elif "prelim" in lower:
      episode += 2
    else:
      if title == "":
        title = "Fight"
      episode += 3

    if year is None and os.path.exists(file):
      year = getYearFromFile(file)

    return Media.Episode(show, year, episode, title, year)

class BellatorHandler(RegexHandler):
  PATTERN = 'Bellator (?P<episode>\d+)'

  def getRegexs(self):
    return [
      'bellator',
    ]

  def handle(self, match, file):
    show = 'Bellator'
    name, year = VideoFiles.CleanName(os.path.basename(file))
    m = re.match(self.PATTERN, name, re.IGNORECASE)
    if not m:
      return None
    episode = int(m.group('episode'))
    title = 'Bellator %d' % episode

    if year is None and os.path.exists(file):
      year = getYearFromFile(file)

    return Media.Episode(show, year, episode, title, year)

class F1Handler(RegexHandler):
  WEEKEND_BUNDLE_RE = re.compile('^(.*).formula1.(?P<year>\d+).r(?P<round>\d+).(?P<name>.*).Gran.Prix.(?P<show>.*)', re.IGNORECASE)
  P1_RE = re.compile('(.*practice.(one|1))|p1', re.IGNORECASE)
  P2_RE = re.compile('(.*practice.(two|2)[-._ ])|p2', re.IGNORECASE)
  P3_RE = re.compile('(.*practice.(three|3))|p3|(3rd.practice)', re.IGNORECASE)
  Q_RE = re.compile('qual', re.IGNORECASE)
  RACE_RE = re.compile('race', re.IGNORECASE)
  TED_RE = re.compile('ted.*qualifying.notebook', re.IGNORECASE)
  IGNORE_RE = re.compile("([pr]addock.live)|(on.the.grid)")

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
    ],
    '2018' : [
      'Australia',
      'Bahrain',
      'China',
      'Azerbaijan',

      'Spain',
      'Monaco',
      'Canada',
      'France',

      'Austria',
      'Great Britain',
      'Germany',
      'Hungary',

      'Belgium',
      'Italy',
      'Singapore',
      'Russia',

      'Japan',
      'United States',
      'Mexico',
      'Brazil',

      'Abu Dhabi',
    ],
    '2019' : [
      'Australia',
      'Bahrain',
      'China',
      'Azerbaijan',

      'Spain',
      'Monaco',
      'Canada',
      'France',

      'Austria',
      'Great Britain',
      'Germany',
      'Hungary',

      'Belgium',
      'Italy',
      'Singapore',
      'Russia',

      'Japan',
      'United States',
      'Mexico',
      'Brazil',

      'Abu Dhabi',
    ],
    '2020' : [
      'Austrian',
      'Styrian',
      'Hungarian',

      'British',
      '70th Anniversary',
      'Spanish',

      'Belgian',
      'Italian',
      'Tuscan',

      'Russian',
      'Eifel',
      'Portuguese',

      'Emilia Romagna',
      'Turkish',
      'Bahrain',

      'Sakhir',
      'Abu Dhabi',
    ],
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
    'Monaco': 'Monaco',
    'French': 'France',
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
    'Belgian': 'Belgium',
    'Italian': 'Italy',
    'Italy': 'Italy',
    'Singapore': 'Singapore',
    'Malaysian': 'Malaysia',
    'Malaysia': 'Malaysia',
    'Japanese': 'Japan',
    'Japane': 'Japan',
    'American': 'United States',
    'America': 'United States',
    'USA': 'United States',
    'United.States': 'United States',
    'Mexican': 'Mexico',
    'Mexico': 'Mexico',
    'Brazilian': 'Brazil',
    'Brazil': 'Brazil',
    'Abu.Dhabi': 'Abu Dhabi',
    'German': 'Germany',
  }

  def getRegexs(self):
    return [
      'Formula.?1.*',
      'Formula.One.*',
      'F1.*',
    ]

  def handle(self, match, file):
    basename = os.path.splitext(file)[0]
    if self.IGNORE_RE.match(basename, re.IGNORECASE):
      return None
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

        if str(year) not in self.SCHEDULE:
          return None

        round = self.SCHEDULE[str(year)].index(location) + 1
        name = location + ' Gran Prix'
        show, part, title = self.getShowAndPart(basename.replace('P2P', ''))

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
    elif self.Q_RE.search(show) and not self.TED_RE.search(show):
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
    elif 'inside.line' in lower:
      return 'F1 Extras', 1, 'Inside Line'
    elif 'f1.report' in lower:
      return 'F1 Extras', 2, 'The F1 Report'
    elif re.search('driver(s)?.press', lower):
      return 'F1 Extras', 3, 'Driver Press Conference'
    elif re.search('welcome.to.the.weekend', lower):
      return 'F1 Extras', 4, 'Welcome to the Weekend'
    elif 'paddock' in lower:
      return 'F1 Extras', 5, 'Paddock Uncut'
    elif self.TED_RE.search(show):
      return 'F1 Extras', 6, "Ted's Qualifying Notebook"
    elif re.search('team.principal', lower):
      return 'F1 Extras', 7, 'Team Principal Press Conference'
    elif re.search('f1.show', lower):
      return 'F1 Extras', 8, 'The F1 Show'
    elif re.search('story.so.far', lower):
      return 'F1 Extras', 9, 'Story So Far'
    else:
      if 'pre' in lower:
        return 'F1', 31, 'Pre Race'
      elif 'post' in lower:
        return 'F1', 33, 'Post Race'
      else:
        return 'F1', 32, 'Race'

    pass


REGEX_HANDLERS = [
  UfcGenericHandler('UFC on ESPN'),
  UfcFightNightHandler(),
  UfcOnFoxHandler(),
  UfcHandler(),
  F1Handler(),
  WsopHandler(),
  BellatorHandler(),
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
  # VideoFiles.Scan(path, files, mediaList, subdirs)
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
