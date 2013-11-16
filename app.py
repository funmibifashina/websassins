"""
app

This is the application's main module.
"""

import web
from web import form
from twilio.rest import TwilioRestClient

import twiliocreds

# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
    '/',              'index',
    '/death',         'death',
    '/twilTest',      'twilTest',
    '/seeMsg',      'seeMsg',
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
                from_=twiliocreds.our_phone,
                body="Test")
        return render.twilTest(str(message.sid))

message = form.Form(
    form.Textbox('message'),
    form.Button('Send'),
)

class seeMsg:
    def GET(self):
        msgForm = message()
        return render.seeMsg(msgForm, None)

    def POST(self):
        msgForm = message()
        if not msgForm.validates():
            return render.seeMsg(msgForm, None)
        else:
            user_data = web.input()
            return render.seeMsg(msgForm, user_data.message)

# Initialize the application
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()

