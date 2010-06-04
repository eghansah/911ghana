import cgi

import pages

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Call(db.Model):
	caller = db.StringProperty()
	phone_number = db.StringProperty()
	location = db.StringProperty()
	complaint = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	#call_operator = db.UserProperty()


class Police_officer(db.Model):
	#Although this could be improved by splitting the officer and officer_locations,
	#for now I don't c much benefit in doing it the right way.
	#Of course, we could always improve it later
	officer = db.StringProperty()
	last_known_location = db.StringProperty()
	date_and_time = db.DateTimeProperty(auto_now_add=True)



class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write( pages.index % {'msg':''} )
	
	def post(self):
		#Simply post data into datastore.
		#and confirm post
		
		call = Call()
		call.caller = self.request.get('caller')
		call.phone_number = self.request.get('phone-number')
		call.complaint = self.request.get('complaint')
		call.location = self.request.get('location')
		#call.call_operator = db.UserProperty()
		
		
		try:
			call.put()
			self.response.out.write( pages.index % {'msg':'Complaint from <b>%s</b> logged' % call.caller} )
		except:
			self.response.out.write( pages.index % {'msg':'System error.'} )



application = webapp.WSGIApplication(
                                     [
										('/', MainPage),
									 ],
                                     debug=True)

	
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
