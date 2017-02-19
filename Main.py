import os

import sys

series = __import__("Plex Series Scanner")

def scan_all(root, path, media):
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

  series.Scan(path, files, media, subdirs, root=root)
  for subdir in subdirs:
    # Get subdir name with root striped out
    subdirRelative = subdir[len(root) + 1:]
    scan_all(root, subdirRelative, media)

if __name__ == '__main__':
  media = []
  scan_all(sys.argv[1], "", media)
  for m in media:
    print m
