#!/usr/bin/env python

import urllib
import urllib2

try:
  from xml.etree.cElementTree import *
except ImportError:
  try:
    from xml.etree.ElementTree import *
  except ImportError:
    from elementtree.ElementTree import *

REDDITS_URL = 'http://www.reddit.com/reddits/mine/.xml'
LOGIN_URL = 'http://www.reddit.com/api/login'
AUTH_INFO = urllib.urlencode(dict(user='raghdam', passwd='secret'))

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

opener.open(LOGIN_URL, AUTH_INFO)
reddits = parse(opener.open(REDDITS_URL))

root = Element("opml")
root.set("version", "1.0")

body = SubElement(root, "body")

for reddit in reddits.findall('channel/item'):
  feed = SubElement(body, "outline")
  feed.set("text", reddit.findtext('title'))
  feed.set("type", "rss")
  feed.set("xmlUrl", "http://www.reddit.com%s" % (reddit.findtext('link')))

print tostring(root)

