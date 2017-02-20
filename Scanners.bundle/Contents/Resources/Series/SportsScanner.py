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
    if year is None:
      year = getYearFromFile(file)

    return Media.Episode(show, year, episode, title, year)


REGEX_HANDLERS = [
  UfcHandler(),
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
