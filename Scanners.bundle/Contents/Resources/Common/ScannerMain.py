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
  # scan(scanner, sys.argv[2], "", media)
  for m in media:
    print '%s S%sE%s %s' % (m.show, m.season, m.episode, m.name)

