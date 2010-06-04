import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class call(db.Model):
	caller = db.StringProperty()
	phone_number = db.StringProperty()
	location = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
	call_operator = db.UserProperty()


class police_officer(db.Model):
	#Although this could be improved by splitting the officer and officer_locations,
	#for now I don't c much benefit in doing it the right way.
	#Of course, we could always improve it later
	officer = db.StringProperty()
	last_known_location = db.StringProperty()
	date_and_time = db.DateTimeProperty(auto_now_add=True)


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
									  ('/logout', Logout)],
                                     debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
