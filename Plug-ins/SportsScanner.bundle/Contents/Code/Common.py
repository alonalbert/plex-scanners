import sys
import urllib2
import ssl

def urlopen(url):
  subversion = sys.version_info[1]
  if subversion >= 7:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return urllib2.urlopen(url, context=context)
  else:
    return urllib2.urlopen(url)
