#!/usr/bin/env python

# reddits-to-opml.py --- a script to transform a Reddit User's subscriptions
# to an OPML feed that can be imported into news aggregating software such
# as Google Reader or Mozilla Thunderbird. The OPML feed is printed to
# standard output; in most cases this is directed to a file.
#
# Copyright (c) 2010 Ryan Aghdam <ryan@ryanaghdam.com>
# Author: Ryan Aghdam <ryan@ryanaghdam.com>
#
# reddits-to-opml.py is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2, or (at your option) any later
# version.
# 
# It is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along
# with your copy of Emacs; see the file COPYING.  If not, write to the Free
# Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# Use:
#   python reddits-to-opml --user=<username> --password=<password>
#
# History:
#   2010-08-08 Ryan Aghdam <ryan@ryanaghdam.com>
#     Initial version

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

