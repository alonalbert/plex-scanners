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
    episodeNum = (int) (episode)
    part = episodeNum % 10
    info = Wikipedia.getInfo('UFC+%s' % (episodeNum / 10))
    imageUrl = Wikipedia.getImageUrl(info['image'])
    name = info['name']
    if part == 1:
      name = "Weigh In - " + name
    elif part == 2:
      name = "Prelims - " + name
    return {
      'thumb': imageUrl,
      'title': name,
      'summary': info['extract'],
    }

def Log(str):
  print str
