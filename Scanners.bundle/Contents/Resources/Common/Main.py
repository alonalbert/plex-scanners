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
  for m in media:
    print m
