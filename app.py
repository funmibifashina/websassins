"""
app

This is the application's main module.
"""

import web              # A simple-looking Python HTTP framework I just found

# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
    '/',             'index',
    '/createdeath',  'createdeath',
    '/death',        'death',
    '/target',        'target',
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

class target:
    def GET(self):
        return render.target()

# Initialize the application
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()
