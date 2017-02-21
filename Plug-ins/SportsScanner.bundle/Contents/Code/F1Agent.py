import re

class F1Agent(object):
  REGEX = re.compile('^f1 ', re.IGNORECASE)

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
    elif title == 'F1 Race':
      return {
        'poster': 'f1-race.jpg',
        'background': 'f1-background-2.jpg'
      }
    elif title == 'F1 Qualifying':
      return {
        'poster': 'f1-qualifying.jpg',
        'background': 'f1-background-3.jpg'
      }
    else:
      return {}

  def getSeasonMetadata(self, title, season):
    return self.getShowMetadata(title)

  def getEpisodeMetadata(self, title, season, episode):
    location = self.LOCATIONS[season][int(episode) - 1]
    return {
      'title' : location + ' Grand Prix',
      'thumb' : 'f1-' + location.lower().replace(' ', '-') + '.png'
    }

