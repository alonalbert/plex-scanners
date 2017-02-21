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
  PATTERN = 'ufc (?P<episode>\d+) (?P<title>.*)'

  def getRegexs(self):
    return [
      '^ufc',
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

  def getRegexs(self):
    return [
      'Formula1.*',
    ]

  def handle(self, match, file):
    basename = os.path.splitext(file)[0]
    m = self.WEEKEND_BUNDLE_RE.match(basename)
    if m:
      year = m.group('year')
      round = m.group('round')
      name = m.group('name') + ' Gran Prix'
      show = m.group('show').replace('.', ' ')
      if show.startswith('Ted') and show.endswith('Notebook'):
        show = "Ted's Qualifying Notebook"
      if not show.startswith('F1'):
        show = 'F1 ' + show
      return Media.Episode(show, year, round, name, year)



REGEX_HANDLERS = [
  UfcHandler(),
  F1Handler(),
]

def handle(file):
  basename = os.path.basename(file)
  for handler in REGEX_HANDLERS:
    for regex in handler.getRegexs():
      match = re.search(regex, basename, re.IGNORECASE)
      if match:
        return handler.handle(match, file)


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  # Scan for video files.
  print files
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
