from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth
from lxml import etree
import optparse

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '161907000675044'
FACEBOOK_APP_SECRET = '9e41cc201fe5d20a5ed60ea4db592a2d'
oauth_token = ''

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

xmlFile = "settings.xml"

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email'}
                            )

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
                                                      request.args['error_reason'],
                                                      request.args['error_description']
                                                      )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')

    tree = etree.parse(xmlFile)
    for elem in tree.xpath(".//fb"):
        elem.attrib['token'] = str(session.get('oauth_token')[0])
    
    with open(xmlFile, 'w') as file_handle:
        file_handle.write(etree.tostring(tree, pretty_print=True, encoding='utf8'))
    
    return 'Successfully received Token!  Logged in as id=%s name=%s redirect=%s.  Please restart Crawler with Crawl options!' % \
        (me.data['id'], me.data['name'], request.args.get('next'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

if __name__ == '__main__':
    print "Facebook Cr4wl3r Token Getter"
    parser = optparse.OptionParser('usage fbCrawler.py -x <xml file> -c -m')
    parser.add_option('-x', '--xml', dest='xmlFile', default="settings.xml", type='string', help='XML File containing settings')
    (options, args) = parser.parse_args()
    xmlFile = options.xmlFile
    app.run()