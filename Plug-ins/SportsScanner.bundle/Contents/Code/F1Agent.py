import re

class F1Agent(object):
  REGEX = re.compile('^f1', re.IGNORECASE)
  PARTS = {
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
  LOCATIONS = {
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

  def __init__(self, log):
    if log is None:
      self.log = Log
    else:
      self.log = log

  def getShowMetadata(self, title):
    if title == 'F1 Show':
      return {
        'poster': 'f1-show-poster.jpg',
        'background': 'f1-background-1.jpg'
      }
    elif title == 'F1':
      return {
        'poster': 'f1-race.jpg',
        'background': 'f1-background-2.jpg'
      }
    else:
      return {}

  def getSeasonMetadata(self, title, season):
    return self.getShowMetadata(title)

  def getEpisodeMetadata(self, title, season, episode):
    ep = int(episode)
    if title == 'F1':
      round = ep / 100
      part = ep % 100
      location = self.LOCATIONS[season][round]
      partName = self.PARTS[part]
      title = location + ' ' + partName
    else:
      location = self.LOCATIONS[season][ep]
      title = location

    return {
      'title' : title,
      'thumb' : 'f1-' + location.lower().replace(' ', '-') + '.png'
    }

