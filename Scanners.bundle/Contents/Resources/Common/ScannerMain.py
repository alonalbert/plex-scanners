import os

import sys

def scan(scanner, root, path, media):
  dir = os.path.join(root, path)
  dirItems = os.listdir(dir)
  files =[]
  subdirs = []
  for item in dirItems:
    itemPath = os.path.join(dir, item)
    if os.path.isdir(itemPath):
      subdirs.append(itemPath)
    else:
      files.append(itemPath)

  scanner.Scan(path, files, media, subdirs, root=root)
  for subdir in subdirs:
    # Get subdir name with root striped out
    subdirRelative = subdir[len(root) + 1:]
    scan(scanner, root, subdirRelative, media)

if __name__ == '__main__':
  media = []
  scanner = __import__(sys.argv[1])
  # scan(scanner, sys.argv[2], "", media)
  scanner.scanFiles([
    '01.Formula1.2016.R13.Belgian.Gran.Prix.F1.Report.ts',
    '02.Formula1.2016.R13.Belgian.Gran.Prix.Driver.Press.Conference.ts',
    '03.Formula1.2016.R13.Belgian.Gran.Prix.Paddock.Uncut.ts',
    '04.Formula1.2016.R13.Belgian.Gran.Prix.Free.Practice.One.ts',
    '05.Formula1.2016.R13.Belgian.Gran.Prix.Free.Practice.Two.ts',
    '06.Formula1.2016.R13.Belgian.Gran.Prix.Team.Principals.Press.Conference.ts',
    '07.Formula1.2016.R13.Belgian.Gran.Prix.F1.Show.ts',
    '08.Formula1.2016.R13.Belgian.Gran.Prix.Free.Practice.Three.ts',
    '09.Formula1.2016.R13.Belgian.Gran.Prix.Qualifying.ts',
    '10.Formula1.2016.R13.Belgian.Gran.Prix.Ted''s.Qualifying.Notebook.ts',
    '11.Formula1.2016.R13.Belgian.Gran.Prix.Race.ts',

    '01.Formula1.2016.R12.German.Gran.Prix.F1.Report.mkv',
    '02.Formula1.2016.R12.German.Gran.Prix.Driver.Press.Conference.ts',
    '03.Formula1.2016.R12.German.Gran.Prix.Paddock.Uncut.ts',
    '04.Formula1.2016.R12.German.Gran.Prix.Free.Practice.One.ts',
    '05.Formula1.2016.R12.German.Gran.Prix.Free.Practice.Two.ts',
    '06.Formula1.2016.R12.German.Gran.Prix.Team.Principals.Press.Conference.ts',
    '07.Formula1.2016.R12.German.Gran.Prix.F1.Show.ts',
    '08.Formula1.2016.R12.German.Gran.Prix.Free.Practice.Three.ts',
    '09.Formula1.2016.R12.German.Gran.Prix.Qualifying.ts',
    '10.Formula1.2016.R12.German.Gran.Prix.Ted, Qualifying.Notebook.ts',
    '11.Formula1.2016.R12.German.Gran.Prix.Race.ts',
  ], media)

  shows = {}

  for m in media:
    if m.show not in shows:
      seasons = {}
      shows[m.show] = seasons
    else:
      seasons = shows[m.show]

    if m.season not in seasons:
      episodes = []
      seasons[m.season] = episodes
    else:
      episodes = seasons[m.season]

    episodes.append(m)

  for show, seasons in shows.iteritems():
    print show
    for season, episodes in seasons.iteritems():
      print "  " + season
      episodes.sort()
      for episode in episodes:
        print '    %s %s' % (episode.episode, episode.name)
