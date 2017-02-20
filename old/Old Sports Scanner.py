#
# Copyright (c) 2010 Plex Development Team. All rights reserved.
#
import re, os, sys, titlecase
import Media, VideoFiles
import ConfigParser

class RegexHandler(object):
  def handle(self, match, filename):
    pass
  def getRegexs(self):
    return []

class F1Handler(RegexHandler):
  def getRegexs(self):
    return [
      '^(?P<year>[12][0-9][0-9][0-9]?)(?P<month>[0-9][0-9]?)(?P<day>[0-9][0-9]?)_F1(_R(?P<race>[0-9][0-9]*?))?_(?P<session>.*?)_?(?P<channel>Sky|BBC?)[^_]*_(?P<location>.*?)(\.pt(?P<part>[1-9][0-9]*?))?.*',
      '^(?P<year>[12][0-9][0-9][0-9]?)(?P<month>[0-9][0-9]?)(?P<day>[0-9][0-9]?)_F1 ([12][0-9][0-9][0-9])?[- _.]+Race (?P<race>[0-9][0-9]*?)[- _.]+(?P<location>.*?)[- _.]+(?P<session>.*?)[- _.]+(?P<channel>Sky|BBC?)(HD)?(\.pt(?P<part>[1-9][0-9]*?))?.*',
      ]

  SESSIONS = {
    "practice1" : 0,
    "practice 1" : 0,
    "p1" : 0,
    "practice2" : 1,
    "practice 2" : 1,
    "p2" : 1,
    "practice3" : 2,
    "practice 3" : 2,
    "p3" : 2,
    "qualifying" : 3,
    "qual" : 3,
    "" : 4,
    }

  RACES = {
    2012: {
      "Australia": "1",
      "Malaysia": "2",
      "China": "3",
      "Bahrain": "4",
      "Spain": "5",
      "Monaco": "6",
      "Canada": "7",
      "Europe": "8",
      "Great Britain": "9",
      "German": "10",
      "Hungary": "11",
      "Belgium": "12",
      "Italy": "13",
      "Singapore": "14",
      "Japan": "15",
      "Korea": "16",
      "India": "17",
      "Abu Dhabi": "18",
      "USA": "19",
      "Brasil": "20",
      }
  }

  def handle(self, match, filename):
    channel = match.group('channel')
    if channel == "SKY":
      channel = "Sky"
    showName = "Formula 1 " + channel
    year = int(match.group('year'))
    location = match.group('location')
    race = match.group('race')
    if race is None:
      race = self.RACES[year][location]
    episode = int(race) * 10
    session = match.group('session')
    if session is not None:
      episode += self.SESSIONS[session.lower()]
    else:
      episode += 4
    episode *= 10

    title = "Race %s %s %s" % (race, location, session)
    part = match.group('part')
    if part is not None:
      episode += int(part) - 1
      title += " #" + part
    episode += 1

    return Media.Episode(showName, year, episode, title, year)


class F1Handler1(RegexHandler):
  LOCATIONS = {
    2013: [
      "Australia",
      "Malaysia",
      "China",
      "Bahrain",
      "Spain",
      "Monaco",
      "Canada",
      "Europe",
      "Great Britain",
      "German",
      "Hungary",
      "Belgium",
      "Italy",
      "Singapore",
      "Japan",
      "Korea",
      "India",
      "Abu Dhabi",
      "USA",
      "Brasil",
      ]
  }

  def getRegexs(self):
    return [
      '^(?P<year>[12][0-9][0-9][0-9]?)(?P<month>[0-9][0-9]?)[0-9]?(?P<day>[0-9][0-9]?)_F1.*',
    ]

  def handle(self, match, filename):
    if filename.lower().find("bbc") >= 0:
      channel = "BBC"
    else:
      channel = "SKY"
    showName = "Formula 1 " + channel
    year = int(match.group('year'))
#    location = match.group('location')

    match = re.search("F1_R(?P<race>[0-9][0-9]*?)", filename);
    race = int(match.group("race"))
    episode = int(race) * 10

    if filename.find("_P1") >= 0:
      sessionNum = 0
      sessionName = "P1"
    elif filename.find("_P2") >= 0:
      sessionNum = 1
      sessionName = "P2"
    elif filename.find("_P3") >= 0:
      sessionNum = 2
      sessionName = "P3"
    elif filename.find("Q1") >= 0:
      sessionNum = 3
      sessionName = "Q1"
    elif filename.find("Q2") >= 0:
      sessionNum = 4
      sessionName = "Q2"
    elif filename.find("Q3") >= 0:
      sessionNum = 5
      sessionName = "Q3"
    elif filename.find("QF1") >= 0:
      sessionNum = 3
      sessionName = "Q1"
    elif filename.find("QF2") >= 0:
      sessionNum = 4
      sessionName = "Q2"
    elif filename.find("QF3") >= 0:
      sessionNum = 5
      sessionName = "Q3"
    elif filename.find("_QF_Q2Q3") >= 0:
      sessionNum = 4
      sessionName = "Q23"
    elif filename.find("QF") >= 0:
      sessionNum = 3
      sessionName = "Q"
    else:
      sessionNum = 7
      sessionName = "Race"
    episode += sessionNum
    episode *= 10

    location = self.LOCATIONS[year][int(race) - 1]
    title = "Race %s %s %s" % (race, location, sessionName)

    p1 = filename.find(".pt")
    if p1 >= 0:
      p2 = filename.find(".", p1 + 1)
      part = filename[p1 + 3:p2]
    else:
      part = None

    if part is not None:
      episode += int(part) - 1
      title += " #" + part
    episode += 1



    return Media.Episode(showName, year, episode, title, year)


class GP2Handler(RegexHandler):
#  20120421_GP2_Round2_Race 1_SkySD_Bahrain.pt1.thebox.e45.avi
  SESSIONS = {
    "practice" : 0,
    "qualifying" : 1,
    "race1" : 2,
    "race 1" : 2,
    "race2" : 3,
    "race 2" : 3,
  }

  def getRegexs(self):
    return ['^(?P<year>[12][0-9][0-9][0-9]?)[0-9][0-9][0-9][0-9]_GP2_Round[_ ]?(?P<round>[0-9][0-9]*?)_(?P<session>.*?)_?(Sky|BBC)[^_]*_(?P<location>.*?)(\.pt(?P<part>[1-9][0-9]*?))?\.thebox.*']

  def handle(self, match, filename):
    showName = "GP2"
    year = int(match.group('year'))
    round = int(match.group('round'))
    session = match.group('session')
    location = match.group('location')
    episode = round * 100 + self.SESSIONS[session.lower()] * 10
    title = "Round %d %s %s" % (round, location, session)
    part = match.group('part')
    if part is not None:
      episode += int(part) - 1
      title += " #" + part
    episode += 1

    return Media.Episode(showName, year, episode, title, year)

class UFCHandler1(RegexHandler):
  def getRegexs(self):
    return [
      '^ufc(?P<year>[12][0-9][0-9][0-9]?)(?P<month>[0-9][0-9]?)[0-9]?(?P<day>[0-9][0-9]?)_F1.*',
    ]

  def handle(self, match, filename):
    if filename.lower().find("bbc") >= 0:
      channel = "BBC"
    else:
      channel = "SKY"
    showName = "Formula 1 " + channel
    year = int(match.group('year'))
#    location = match.group('location')

    match = re.search("F1_R(?P<race>[0-9][0-9]*?)", filename);
    race = int(match.group("race"))
    episode = int(race) * 10

    if filename.find("_P1") >= 0:
      sessionNum = 0
      sessionName = "P1"
    elif filename.find("_P2") >= 0:
      sessionNum = 1
      sessionName = "P2"
    elif filename.find("_P3") >= 0:
      sessionNum = 2
      sessionName = "P3"
    elif filename.find("_QF_Q1") >= 0:
      sessionNum = 3
      sessionName = "Q1"
    elif filename.find("Q1") >= 0:
      sessionNum = 3
      sessionName = "Q1"
    elif filename.find("Q2") >= 0:
      sessionNum = 4
      sessionName = "Q2"
    elif filename.find("Q3") >= 0:
      sessionNum = 5
      sessionName = "Q3"
    elif filename.find("_QF_Q2Q3") >= 0:
      sessionNum = 4
      sessionName = "Q23"
    elif filename.find("_QF") >= 0:
      sessionNum = 3
      sessionName = "Q"
    else:
      sessionNum = 6
      sessionName = "Race"
    episode += sessionNum
    episode *= 10

    location = self.LOCATIONS[year][int(race) - 1]
    title = "Race %s %s %s" % (race, location, sessionName)

    p1 = filename.find(".pt")
    if p1 >= 0:
      p2 = filename.find(".", p1 + 1)
      part = filename[p1 + 3:p2]
    else:
      part = None

    if part is not None:
      episode += int(part) - 1
      title += " #" + part
    episode += 1



    return Media.Episode(showName, year, episode, title, year)

class RegexMatcher:
  def __init__(self,
               name,
               regex,
               show="%s", showArgs="show",
               season="%s", seasonArgs="season",
               episode="%s", episodeArgs="episode",
               title="Episode %s", titleArgs = "episode",
               year="%s", yearArgs="year"):
    self.name = name
    self.regex = regex
    self.show = show
    self.showArgs = showArgs
    self.season = season
    self.seasonArgs = seasonArgs
    self.episode = episode
    self.episodeArgs = episodeArgs
    self.title = title
    self.titleArgs = titleArgs
    self.year = year
    self.yearArgs = yearArgs


class GenericScanner():
  def __init__(self):
    config = ConfigParser.ConfigParser()
    configFilename = os.path.expanduser("~/.mySportsScanner.cfg")
    config.read(configFilename)

    matcherMap = {}
    for section in config.sections():
      matcher = RegexMatcher(section, config.get(section, "regex"))
      order = int(config.get(section, "order"))
      matcherMap[order] = matcher
      if config.has_option(section, "show"):
        matcher.show =  config.get(section, "show")
      if config.has_option(section, "showArgs"):
        matcher.showArgs =  config.get(section, "showArgs")
      if config.has_option(section, "season"):
        matcher.season =  config.get(section, "season")
      if config.has_option(section, "seasonArgs"):
        matcher.seasonArgs =  config.get(section, "seasonArgs")
      if config.has_option(section, "episode"):
        matcher.episode =  config.get(section, "episode")
      if config.has_option(section, "episodeArgs"):
        matcher.episodeArgs =  config.get(section, "episodeArgs")
      if config.has_option(section, "title"):
        matcher.title =  config.get(section, "title")
      if config.has_option(section, "titleArgs"):
        matcher.titleArgs =  config.get(section, "titleArgs")
      if config.has_option(section, "year"):
        matcher.year =  config.get(section, "year")
      if config.has_option(section, "yearArgs"):
        matcher.yearArgs =  config.get(section, "yearArgs")
    self.matcherList = []
    for order in sorted(matcherMap.iterkeys()):
      matcher = matcherMap[order]
      self.matcherList.append(matcher)

  def getString(self, match, format, argsString):
    args = ()
    for group in argsString.split(","):
      if group != "":
        arg = match.group(group)
        if group == "show":
          arg = arg.replace(".", " ").replace("-", " ").replace("_", " ")
        elif group == "episode" or group == "year":
          if arg is None and group == "year":
            arg = 2012
          arg = int(arg)
        args = args + (arg,)
    value = format % args
    if value == "":
      value = None
    return value

  def scan(self, filename):
    for matcher in self.matcherList:
      match = re.search(matcher.regex, filename, re.IGNORECASE)
      if match:
        showName = titlecase.titlecase(self.getString(match, matcher.show, matcher.showArgs).replace(".", " ").replace("-", " ").replace("_", " "))
        season = int(self.getString(match, matcher.season, matcher.seasonArgs))
        episode = int(self.getString(match, matcher.episode, matcher.episodeArgs))
        year = self.getString(match, matcher.year, matcher.yearArgs)
        if year is not None:
          year = int(year)
        title = self.getString(match, matcher.title, matcher.titleArgs)
        partMatch = re.search("p(ar)?t[ _-](?P<part>[0-9]+)", filename, re.IGNORECASE)
        if partMatch:
          part = int(partMatch.group("part"))
          episode = episode * 10 + part - 1
          title = title + " Part " + str(part)

        return  Media.Episode(showName, season, episode, title, year)


REGEX_HANDLERS = [
  #F1Handler(),
  F1Handler1(),
  #GP2Handler(),
]

def customScan(filename):
  for handler in REGEX_HANDLERS:
    for regex in handler.getRegexs():
      match = re.search(regex, filename, re.IGNORECASE)
      if match:
        return handler.handle(match, filename)


def Scan(path, files, mediaList, subdirs):
  # Scan for video files.
  print files
  VideoFiles.Scan(path, files, mediaList, subdirs)
  scanner = GenericScanner()
  # Run the select regexps we allow at the top level.
  for file in files:
    filename, ext = os.path.splitext(os.path.basename(file))
    show = customScan(filename)
    if show is None:
      show = scanner.scan(filename)
    if show is None:
      show = scanner.scan(file)
    if show is not None:
      print(filename)
      print("  Show: %s\n  Season: %d\n  episode: %d\n  title: %s\n  Year: %s" % (show.show, show.season, show.episode, show.name, show.year))
      show.parts.append(file)
      mediaList.append(show)

if __name__ == '__main__':
  if len(sys.argv) < 2:
    path = "files"
  else:
    path = sys.argv[1]
  files = [os.path.join(path, file) for file in os.listdir(path)]
  media = []
  Scan(path[1:], files, media, [])
  print "Total: %d" % len(media)
