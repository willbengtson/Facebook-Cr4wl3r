#!/usr/bin/env python
import optparse, sys, os
from fb import crawl, crawl_priv, search, meta, username
from facebook import *
from lxml import etree

xmlFile = "settings.xml"
crawlUsers = False
crawlPriv = False
metadata = False
searchUser = False
login = False
user = None

def main():
    # Setup the parser and add the options
    parser = optparse.OptionParser('usage fbCr4wl3r.py -x <xml file> -c -m -u <username>')
    parser.add_option('-x', '--xml', dest='xmlFile', default="settings.xml", type='string', help='XML File containing settings')
    parser.add_option('-u', '--user', dest='user', type='string', help='User for metadata recovery')
    parser.add_option("-c", "--crawl", action="store_true", dest="crawlUsers", help="Crawl Users")
    parser.add_option("-p", "--crawl_priv", action="store_true", dest="crawlPriv", help="Crawl Users with Privileges")
    parser.add_option("-m", "--meta", action="store_true", dest="metadata", help="Print Metadata for User")
    parser.add_option("-s", "--search_user", action="store_true", dest="searchUser", help="Search for a Facebook User")
    parser.add_option("-l", "--fb_login", action="store_true", dest="login", help="Get a Facebook Token")
    
    # Parse the options
    (options, args) = parser.parse_args()
    xmlFile = options.xmlFile
    user = options.user
    crawlUsers = options.crawlUsers
    crawlPriv = options.crawlPriv
    metadata = options.metadata
    searchUser = options.searchUser
    login = options.login

    if crawlUsers == True:
	    crawl(xmlFile)
	    exit(0)
    elif crawlPriv == True:
        crawl_priv(xmlFile)
        exit(0)
    elif metadata == True:
        if user == None:
            print "Must specify user using '-u' option"
            exit(1)
        meta(xmlFile, user)
        exit(0)
    elif searchUser == True:
        if user == None:
            print "Must specify user using '-u' option"
            exit(1)
        search(xmlFile, user)
        exit(0)
    elif login == True:
        os.system("python facebook.py -x " + xmlFile)
        exit(0)
    elif user != None:
        username(xmlFile, user)
        exit(0)
    else:	
        print parser.usage
			
if __name__ == '__main__':
    main()