import re
import Wikipedia

class UfcAgent(object):
  REGEX = re.compile('^ufc', re.IGNORECASE)

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
    info = Wikipedia.getInfo('UFC+%s' % episode)
    imageUrl = Wikipedia.getImageUrl(info['image'])
    return {
      'thumb': imageUrl,
      'title': info['name'],
      'summary': info['extract'],
    }

def Log(str):
  print str
