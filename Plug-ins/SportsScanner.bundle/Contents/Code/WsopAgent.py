import re

class WsopAgent(object):
  def get_regex(self):
    return re.compile('^wsop', re.IGNORECASE)

  def __init__(self, log):
    if log is None:
      self.log = Log
    else:
      self.log = log

  def getShowMetadata(self, title):
    return {
      'poster': 'wsop-poster.jpg',
      'background': 'wsop-background.jpg'
    }

  def getSeasonMetadata(self, title, season):
    return {
      'poster': 'wsop-poster.jpg',
    }

  def getEpisodeMetadata(self, title, season, episode):
    return {
      'thumb': 'wsop-poster.jpg',
      'title': title,
      'summary': '',
    }

def Log(str):
  print str
