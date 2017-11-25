import re

class BellatorAgent(object):
  REGEX = re.compile('^bellator', re.IGNORECASE)

  def __init__(self, log):
    if log is None:
      self.log = Log
    else:
      self.log = log

  def getShowMetadata(self, title):
    return {
      'poster': 'bellator-poster.jpg',
      'background': 'bellator-background.jpg'
    }

  def getSeasonMetadata(self, title, season):
    return {
      'poster': 'bellator-poster.jpg',
    }

  def getEpisodeMetadata(self, title, season, episode):
    return {
      'thumb': 'bellator-poster.jpg',
      'title': title,
      'summary': '',
    }

def Log(str):
  print str
