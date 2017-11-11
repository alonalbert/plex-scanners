import re


class F1Agent(object):
  REGEX = re.compile('^f1', re.IGNORECASE)
  SESSION_RE = re.compile('f1 (?P<extra>extras )?(?P<round>\d\d) (?P<location>[a-z ]+)$', re.IGNORECASE)

  PARTS = {
    1: "Inside Line",
    2: "The F1 Report",
    3: "Driver Press Conference",
    4: "Paddock Uncut",
    5: "Ted's Qualifying Notebook",
    6: "Team Principal Press Conference",
    7: "The F1 Show",
    11: "Practice One",
    12: "Practice Two",
    13: "Practice Three",
    21: "Pre Qualifying",
    22: "Qualifying",
    23: "Post Qualifying",
    31: "Pre Race",
    32: "Race",
    33: "Post Race",
  }

  def __init__(self, log):
    if log is None:
      self.log = Log
    else:
      self.log = log

  def getShowMetadata(self, title):
    match = self.SESSION_RE.match(title)
    if match:
      location = match.group('location')
      if match.group('extra'):
        return {
          'poster': 'f1-show-poster.jpg',
          'background': 'f1-background-1.jpg'
          }
      else:
        return {
          'poster': 'f1-race.jpg',
          'background': self.getTrackImage(location)
          }
    else:
      return {}

  def getSeasonMetadata(self, title, season):
    return self.getShowMetadata(title)

  def getEpisodeMetadata(self, title, season, episode):
    ep = int(episode)
    match = self.SESSION_RE.match(title)
    if match:
      location = match.group('location')
      round = ep / 100
      part = ep % 100
      title = self.PARTS[part]
    else:
      return {}

    return {
      'title': title,
      'thumb': self.getTrackImage(location)
    }

  def getTrackImage(self, location):
    return 'f1-' + location.lower().replace(' ', '-') + '.png'
