import json
import urllib2
#from threading import *
from pymongo import MongoClient
from xml.dom import minidom
from dicttoxml import dicttoxml

"""
    t = Thread(target = conn_scan, args = (tgtHost, int(tgtPort)))
    t.start()
"""
#screenLock = Semaphore(value = 1)

baseUrl = "http://graph.facebook.com/"
secureBaseUrl = "https://graph.facebook.com/"
token = "asdfasdf"
log = 0

# Kick off a crawler
def crawl(xmlFile):
    xmldoc = minidom.parse('settings.xml')
    crawlSettings = xmldoc.getElementsByTagName('crawl')
    start = int(crawlSettings[0].attributes['start'].value)
    end = int(crawlSettings[1].attributes['end'].value)
    
    mongoSettings = xmldoc.getElementsByTagName('mongo')
    ipAddress = mongoSettings[0].attributes['ip'].value
    port = int(mongoSettings[1].attributes['port'].value)
    log = int(mongoSettings[2].attributes['log'].value)
    
    fbTokenSettings = xmldoc.getElementsByTagName('fb')
    token = fbTokenSettings[0].attributes['token'].value
    
    if log == 1:
        client = MongoClient(ipAddress, port)
        db = client.facebookCrawler
        users = db.users
    
    userCount = 0
    
    print "Starting crawl...Start: %s, End: %s" % (start, end)
    
    for x in range(start, end):
        try:
            if x % 100 == 0:
                print "Working...%s\n" % (x)
            urlToVisit = baseUrl + str(x);
            data = json.load(urllib2.urlopen(urlToVisit))
        
            if log == 1:
                users.insert(data)

            userCount += 1
            print data['name']
        except:
            pass
    
    print "\n" + str(userCount) + " Results Found!"
    print "Done crawling"

# Kick off a crawler with privileges
def crawl_priv(xmlFile):
    xmldoc = minidom.parse('settings.xml')
    crawlSettings = xmldoc.getElementsByTagName('crawl')
    start = int(crawlSettings[0].attributes['start'].value)
    end = int(crawlSettings[1].attributes['end'].value)

    mongoSettings = xmldoc.getElementsByTagName('mongo')
    ipAddress = mongoSettings[0].attributes['ip'].value
    port = int(mongoSettings[1].attributes['port'].value)
    log = int(mongoSettings[2].attributes['log'].value)

    fbTokenSettings = xmldoc.getElementsByTagName('fb')
    token = fbTokenSettings[0].attributes['token'].value

    if log == 1:
        client = MongoClient(ipAddress, port)
        db = client.facebookCrawler
        users = db.users

    userCount = 0

    print "Starting crawl with privileges...Start: %s, End: %s" % (start, end)

    for x in range(start, end):
        try:
            if x % 100 == 0:
                print "Working...%s\n" % (x)
            urlToVisit = secureBaseUrl + str(x) + '?access_token=' + str(token)
            data = json.load(urllib2.urlopen(urlToVisit))

            if log == 1:
                users.insert(data)

            userCount += 1
            print data['name']
        except:
            pass

    print "\n" + str(userCount) + " Results Found!"
    print "Done crawling"

# Search for a user
def search(xmlFile, name):
    xmldoc = minidom.parse('settings.xml')
    crawlSettings = xmldoc.getElementsByTagName('fb')
    token = crawlSettings[0].attributes['token'].value
    
    name = name.replace(" ", "%20")
    url = secureBaseUrl + 'search?q=' + str(name) + '&type=user&access_token=' + str(token)
    count = 1
    try:
        data = json.load(urllib2.urlopen(url))
        
        print "Search returned %s results" % len(data['data'])
        for x in range(0, len(data['data'])):
            print count, '-', data['data'][x]['name']
            count = count + 1
    except:
        print "Error retrieving search results"

# See what metadata you can get from a User
def meta(xmlFile, username):
    xmldoc = minidom.parse('settings.xml')
    crawlSettings = xmldoc.getElementsByTagName('fb')
    token = crawlSettings[0].attributes['token'].value
    
    url = secureBaseUrl + str(username) + '?metadata=1&access_token=' + str(token)

    count = 1
    try:
        data = json.load(urllib2.urlopen(url))
        for k, v in data['metadata']['connections'].items():
            print count, '-', k
            count = count + 1
        xmldata = dicttoxml(data)
        with open(username + "_metadata.xml", 'w') as file_handle:
            file_handle.write(xmldata)
    except:
        print "Error retrieving metadata\n"

# Crawl a specific user
def username(xmlFile, user):
    xmldoc = minidom.parse('settings.xml')
    crawlSettings = xmldoc.getElementsByTagName('fb')
    token = crawlSettings[0].attributes['token'].value

    url = secureBaseUrl + str(user) + '?access_token=' + str(token)

    count = 1
    try:
        data = json.load(urllib2.urlopen(url))
        xmldata = dicttoxml(data)
        with open(user + ".xml", 'w') as file_handle:
            file_handle.write(xmldata)
    except:
        print "Error retrieving user data\n"    
