import re
import Wikipedia

class UfcFightNightAgent(object):
  REGEX = re.compile('^ufc.fight.night', re.IGNORECASE)

  def __init__(self, log):
    if log is None:
      self.log = Log
    else:
      self.log = log

  def getShowMetadata(self, title):
    return {
      'poster': 'ufc-poster.jpg',
      'background': 'ufc-background.jpg'
    }

  def getSeasonMetadata(self, title, season):
    return {
      'poster': 'ufc-poster.jpg',
    }

  def getEpisodeMetadata(self, title, season, episode):
    return {
      'thumb': 'ufc-poster.jpg',
      'title': title,
      'summary': '',
    }

def Log(str):
  print str
