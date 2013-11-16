"""
app

This is the application's main module.
"""

import web              # A simple-looking Python HTTP framework I just found
  
# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
  '/',                  'index',
  '/death',        'death',
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

# Initialize the application
if __name__ == "__main__":
  web.internalerror = web.debugerror
  app = web.application(urls, globals())
  app.run()