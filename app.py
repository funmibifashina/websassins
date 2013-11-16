"""
app

This is the application's main module.
"""

import web
from web import form
from twilio.rest import TwilioRestClient
import twilio.twiml
import twiliocreds
import string
import random
import sqlite3
import re
import sys

# Convenience functions
def GetRandomString():
        chars = string.ascii_uppercase + string.digits
        size = 4;
        return ''.join(random.choice(chars) for x in range(size))

#Access Database

# regex for game ids
gameIdRe = '([A-Z0-9]{4})'

# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
    '/',              'index',
    '/create/' + gameIdRe,   'createdeath',
    '/start/' + gameIdRe,    'startdeath',
    '/game/' + gameIdRe,     'deathmatch',
    '/join',          'join',
    '/leave',         'leave',
    '/activation',    'activation',
    '/seeMsg',        'seeMsg',
    '/echoChamber',   'echoChamber',
    '/handleSms',   'handleSms',
)


# Tell web.py where to look to find page templates
render = web.template.render('templates/');

# Classes that handle URLs

# Form that handles the buttons on the index page
class index:
    def GET(self):
        web.setcookie('fakesession', GetRandomString() + GetRandomString())
        chars = string.ascii_uppercase + string.digits
        size = 4;
        game_id = GetRandomString()
        return render.index(game_id)

class createdeath:
    def GET(self, game_id):
        # logic for dealing with reacurring game IDs
        con = None
        try:
            con = sqlite3.connect('test.db')
            cur = con.cursor()    
            cur.execute("SELECT id FROM Game WHERE id = '" + game_id + "'")
            data = cur.fetchone()

            if data is None:
                cur.execute("INSERT into Game(id) VALUES('" + game_id + "')")
                con.commit()
                return render.createdeath(game_id)
            else:
                game_id = GetRandomString()
                return web.redirect('/create/' + game_id)          
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

class startdeath:
    def GET(self, game_id):
        # Start the game
        # Redirect to game page
        # return render.deathmatch(game_id)
        con = None
        try:
            con = sqlite3.connect('test.db')
            cur = con.cursor()   
            cur.execute("SELECT player_id FROM Players WHERE id = '" + game_id + "'")
            data = cur.fetchall()
            count = len( data )
            print "Number of players: ", count
            for x in xrange(count):
                assassin = data[x][0]
                target = data[(x+1)%count][0]
                print "Here's an assassin: ", assassin, " --> target: ", target

            return web.redirect('/create/' + game_id)          
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()

        web.redirect('/game/' + game_id)

class deathmatch:
    def GET(self, game_id):
        return render.deathmatch(game_id)

joining = form.Form(
    form.Textbox(name="username", description="Assassin name"),
    form.Textbox(name="game_id", description="What Game ID are you trying to join?"),
    form.Button('Join!', class_='btn btn-lg btn-primary'),
)

class join:
    def GET(self):
        # Does the game exist
        joinForm = joining()
        return render.join(joinForm)

    def POST(self):
        user_data = web.input()
        # if the game ID Exists.......
        con = None
        try:
            con = sqlite3.connect('test.db')
            cur = con.cursor()    
            cur.execute('SELECT * from game WHERE id ="' + user_data.game_id + '"')
            data = cur.fetchone()
            if(data is None):
                print "Game does not exist"
                joinForm = joining()
                return render.failedjoin(joinForm)
            else:
                # add this user to the game
                queryStr = "INSERT into Players(id, player_id) VALUES( '%s' , '%s ' )" % (user_data.game_id, user_data.username.replace(' ', ''))
                cur.execute( queryStr )
                con.commit()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.close()
        
        
        web.redirect('/game/' + user_data.game_id)

class leave:
    def GET(self):
        # let this user exit the game
        web.redirect('/')

class activation:
    def GET(self):
        return render.activation()

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

    def POST(self):
        user_data = web.input()
        resp = twilio.twiml.Response()
        try:
            resp.message(user_data.Body)
        except AttributeError:
            resp.message("You said nothing.")
        web.debug("Sayin' this:" + str(resp))
        web.header('Content-Type', 'text/xml')
        return str(resp)

class handleSms:
    def POST(self):
        user_data = web.input()
        resp = twilio.twiml.Response()

        try:
            text = user_data.Body.lower()
            phoneNum = user_data.From
            if text[0] == "j":
                split = text.split(" ")
                if len(split) < 2:
                    resp.message("Malformed command '" + text + "'")
                else:
                    split[1] = split[1].upper()
                    con = None
                    try:
                        con = sqlite3.connect('test.db')
                        cur = con.cursor()    
                        cur.execute('SELECT * from game WHERE id ="' + split[1] + '"')
                        data = cur.fetchone()
                        if(data is None):
                            resp.message("Game '" + split[1] + "' does not exist")
                        else:
                            resp.message("Joined '" + split[1] + "'")
                            queryStr = "INSERT into Players(id, player_id) VALUES( '%s' , '%s ' )" % (split[1], phoneNum)
                            cur.execute( queryStr )
                            con.commit()
                    except sqlite3.Error, e:
                        resp.message("Error " + str(e.args[0]))
                    finally:
                        if con:
                            con.close()
            elif text[0] == "k":
                resp.message("KILL SUM FOOLZ")
            elif text[0] == "d":
                resp.message("YOU DAYID")
            else:
                resp.message("lol wut")
        except AttributeError:
            resp.message("No command entered")

        web.header('Content-Type', 'text/xml')
        return str(resp)

# Initialize the application
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()

