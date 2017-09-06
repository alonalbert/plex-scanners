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
  scan(scanner, sys.argv[2], "", media)

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

    episodes.append('%s %s' % (m.episode, m.name))

  for show in sorted(shows):
    seasons = shows[show]
    print show
    for season in sorted(seasons):
      episodes = seasons[season]
      print "  " + str(season)
      for episode in sorted(episodes):
        print '    ' + episode
