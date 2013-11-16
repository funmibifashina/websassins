"""
app

This is the application's main module.
"""

import web
from web import form
from twilio.rest import TwilioRestClient
import twilio.twiml

import twiliocreds
import web              # A simple-looking Python HTTP framework I just found

# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
    '/',              'index',
    '/createdeath',   'createdeath',
    '/deathmatch',    'deathmatch',
    '/seeMsg',        'seeMsg',
    '/echoChamber',        'echoChamber',
)

# Tell web.py where to look to find page templates
render = web.template.render('templates/');

# Classes that handle URLs
class index:
    def GET(self):
        return render.index()

class createdeath:
    def GET(self):
        return render.createdeath()

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
            client = TwilioRestClient(twiliocreds.account_sid,
                    twiliocreds.auth_token)
            sms = client.messages.create(to=twiliocreds.sams_phone,
                    from_=twiliocreds.our_phone,
                    body=user_data.message)
            return render.seeMsg(msgForm, "Sent " + user_data.message + " " +
                    str(sms.sid))

class target:
    def GET(self):
        return render.target()

class echoChamber:
    def GET(self):
        resp = twilio.twiml.Response()
        resp.message("This is a reply")
        return str(resp)

# Initialize the application
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()

