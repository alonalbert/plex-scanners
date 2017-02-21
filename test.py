import json
import re
import Image
import cStringIO
import Common

import io

WIKI_PAGEINFO = "https://en.wikipedia.org//w/api.php?action=query&format=json&prop=extracts%7Crevisions&exintro=1&rvprop=content&titles="
WIKI_IMAGEINFO = "https://en.wikipedia.org///w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles=File%3A"
CLEAN_HTML_REGEX = re.compile('<.*?>')
INFOBOX_REGEX = re.compile('^\| ?(?P<key>[^ ]+) ?= ?(?P<value>.*)')

# def parseInfoBox(infoBox):
#   map = {}
#   for line in infoBox.splitlines()[1:]:
#     match = INFOBOX_REGEX.match(line)
#     map[match.group('key')] = match.group('value')
#   return map
#
# pageInfo = json.loads(urllib.urlopen(WIKI_PAGEINFO + "UFC+208").read())
# pages = pageInfo['query']['pages']
# page = pages[next(iter(pages))]
#
# contents = page['revisions'][0]['*']
#
# box = parseInfoBox(contents[0:contents.index('\n}}\n')])
#
# name = box['name']
# image = box['image']
# extract = CLEAN_HTML_REGEX.sub('', page['extract'])
#
#
#
# print name
# print image
# print extract
#
# imageInfo = json.loads(urllib.urlopen(WIKI_IMAGEINFO + image).read())
# pages = imageInfo['query']['pages']
# page = pages[next(iter(pages))]
#
# imageUrl = page['imageinfo'][0]['url']
# print imageUrl

file = cStringIO.StringIO(Common.urlopen("https://upload.wikimedia.org/wikipedia/en/6/60/UFC_208_poster.jpg").read())
img = Image.open(file)

THUMB_WIDTH=250
THUMB_HEIGHT=140
width, height =  img.size
if height > width:
  newWidth = height
  newImage = Image.new("RGB", (height, height))
  newImage.paste(img, ((height -width) / 2, 0))
  bytes = io.BytesIO()
  newImage.show()





# print json.dumps(imageInfo, indent=4, sort_keys=True)

