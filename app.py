"""
app

This is the application's main module.
"""

import web
from twilio.rest import TwilioRestClient
import twiliocreds

# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
    '/',              'index',
    '/death',         'death',
    '/twilTest',      'twilTest',
)

# Tell web.py where to look to find page templates
render = web.template.render('templates/');

# Classes that handle URLs
class index:
    def GET(self):
        return render.index()

class death:
    def GET(self):
        return render.death()

class twilTest:
    def GET(self):
        client = TwilioRestClient(twiliocreds.account_sid,
                twiliocreds.auth_token)
        message = client.messages.create(to=twiliocreds.sams_phone,
                from_="+16616674124",
                body="Test")
        return render.twilTest(str(message.sid))

# Initialize the application
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()

