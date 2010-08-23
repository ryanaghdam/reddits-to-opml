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
# Use:
#   python reddits-to-opml --user=<username> --password=<password>
#
# History:
#   2010-08-09 Ryan Aghdam <ryan@ryanaghdam.com>
#     Rewrite
#
#   2010-08-08 Ryan Aghdam <ryan@ryanaghdam.com>
#     Initial version

import urllib2
import urllib

# Apparently ElementTree can exist in different locations depending on the
# version of Python.
#
# http://google-app-engine-samples.googlecode.com/svn-history/r97/trunk/muvmuv/main.py
try:
  from xml.etree.cElementTree import *
except ImportError:
  try:
    from xml.etree.ElementTree import *
  except ImportError:
    from elementtree.ElementTree import *

import argparse

# Constants
REDDITS_URL = 'http://www.reddit.com/reddits/mine/.xml'
LOGIN_URL = 'http://www.reddit.com/api/login'
PROGRAM_DESCRIPTION = "Prints an OPML Feed for a user's subscribed Reddits"
PROGRAM_USAGE = "%(prog)s USERNAME PASSWORD"

def fetch_subscriptions(credentials):
  """ Given URL Encoded account credentials, return a RSS Feed
  containing the the user's subscriptions """
  
  # Create a URLOpener, with Cookie support
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
  urllib2.install_opener(opener)

  # Send credentials; a cookie is stored if successful.
  opener.open(LOGIN_URL, credentials)

  # Return Subscription RSS Feed
  return opener.open(REDDITS_URL)

def encode_credentials(user, passwd):
  """ URL Encode the given username and password """
  return urllib.urlencode(dict(user=user, passwd=passwd))

def parse_subscription_feed(feed):
  reddits = []
  for subscription in parse(feed).findall('channel/item'):
    reddits.append({
        'text': subscription.findtext('title'),
        'xmlUrl': "http://www.reddit.com%s" % (subscription.findtext('link'))
      })
  return reddits

def create_opml_feed(reddits=[]):
  # Root element of OPML feed
  opml_root = Element("opml")
  opml_root.set("version", "1.0")

  # Create a body Element
  body = SubElement(opml_root, "body")

  # Add each reddit to feed
  for reddit in reddits:
    outline = SubElement(body, "outline")
    outline.set("type", "rss")
    outline.set("text", reddit["text"])
    outline.set("xmlUrl", reddit["xmlUrl"])

  # Return the feed
  return opml_root

def main(argv):
  print prettyprint(create_opml_feed(parse_subscription_feed(fetch_subscriptions(encode_credentials(argv.user,
    argv.passwd)))))



if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION,
      usage=PROGRAM_USAGE)
  parser.add_argument('-u', '--user', required=True, help="Reddit Username")
  parser.add_argument('-p', '--passwd', required=True, help="Reddit Password")
  main(parser.parse_args())
