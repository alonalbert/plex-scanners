import urllib
import json
import re

WIKI_PAGEINFO = "https://en.wikipedia.org//w/api.php?action=query&format=json&prop=extracts%7Crevisions&exintro=1&rvprop=content&titles="
WIKI_IMAGEINFO = "https://en.wikipedia.org///w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles=File%3A"
CLEAN_HTML_REGEX = re.compile('<.*?>')
INFOBOX_REGEX = re.compile('^\| ?(?P<key>[^ ]+) ?= ?(?P<value>.*)')


def getFirst(map):
  for key, value in map.iteritems():
      return value

def getInfo(title):
  pageInfo = json.loads(urllib.urlopen(WIKI_PAGEINFO + title).read())
  pages = pageInfo['query']['pages']
  page = getFirst(pages)

  contents = page['revisions'][0]['*']
  infoBox = contents[0:contents.index('\n}}\n')]

  map = {}
  for line in infoBox.splitlines()[1:]:
    match = INFOBOX_REGEX.match(line)
    map[match.group('key')] = match.group('value')

  map['extract'] = CLEAN_HTML_REGEX.sub('', page['extract'])
  return map

def getImageUrl(image):
  imageInfo = json.loads(urllib.urlopen(WIKI_IMAGEINFO + image).read())
  pages = imageInfo['query']['pages']
  page = getFirst(pages)
  return page['imageinfo'][0]['url']
