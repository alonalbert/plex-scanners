import urllib, json
import re

WIKI_PAGEINFO = "https://en.wikipedia.org//w/api.php?action=query&format=json&prop=extracts%7Crevisions&exintro=1&rvprop=content&titles="
WIKI_IMAGEINFO = "https://en.wikipedia.org///w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles=File%3A"
CLEAN_HTML_REGEX = re.compile('<.*?>')
INFOBOX_REGEX = re.compile('^\| ?(?P<key>[^ ]+) ?= ?(?P<value>.*)')

def parseInfoBox(infoBox):
  map = {}
  for line in infoBox.splitlines()[1:]:
    match = INFOBOX_REGEX.match(line)
    map[match.group('key')] = match.group('value')
  return map

pageInfo = json.loads(urllib.urlopen(WIKI_PAGEINFO + "UFC+208").read())
pages = pageInfo['query']['pages']
page = pages[next(iter(pages))]

contents = page['revisions'][0]['*']

box = parseInfoBox(contents[0:contents.index('\n}}\n')])

name = box['name']
image = box['image']
extract = CLEAN_HTML_REGEX.sub('', page['extract'])



print name
print image
print extract

imageInfo = json.loads(urllib.urlopen(WIKI_IMAGEINFO + image).read())
pages = imageInfo['query']['pages']
page = pages[next(iter(pages))]
print page['imageinfo'][0]['url']

# print json.dumps(imageInfo, indent=4, sort_keys=True)

