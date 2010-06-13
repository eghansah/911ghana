import cgi

import key
import pages
import urllib

import datetime
import PyGeoRSS
from cStringIO import StringIO

from geo.geomodel import GeoModel
from BeautifulSoup import BeautifulSoup

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db





def getGeoCode( town ):
	
	lat = lng = None
	
	try:
		url = "http://maps.google.com/maps/api/geocode/xml?%s"
		params = urllib.urlencode({
					'address': town,
					'sensor':'false'	
		})

	
		f = urllib.urlopen( url % params )
		xml = f.read()
		f.close()
	
		soup = BeautifulSoup(xml)
		loc = soup('location')[0]
		lat = loc.lat.text
		lng = loc.lng.text
	except:
		pass
	return (lat, lng)



def getNearestOfficers( loc ):
	results = Police_officer_loc.proximity_fetch(
			Police_officer_loc.all(),
			loc,  # Or db.GeoPt
			max_results=10,
			max_distance=80467)
	
	
	return [officer.name for officer in results]



class Call(GeoModel):
	caller = db.StringProperty()
	phone_number = db.StringProperty()
	location_name = db.StringProperty()
	#geoloc = db.GeoPtProperty()
	complaint = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	#call_operator = db.UserProperty()


class Police_officer_loc(GeoModel):
	#Although this could be improved by splitting the officer and officer_locations,
	#for now I don't c much benefit in doing it the right way.
	#Of course, we could always improve it later
	name = db.StringProperty()
	last_known_location = db.StringProperty()
	date_and_time = db.DateTimeProperty(auto_now_add=True)



class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write( pages.index % {'msg':''} )
	
	def post(self):
		#Simply post data into datastore.
		#and confirm post
		
		call = Call( location=db.GeoPt(0, 0) )
		call.caller = self.request.get('caller')
		call.phone_number = self.request.get('phone-number')
		call.complaint = self.request.get('complaint')
		call.location_name = "%s, ghana" % self.request.get('location')
		
		lat, lng = getGeoCode( call.location_name )
		loc = "Unknown"
		if lat or lng:
			call.location = db.GeoPt(lat, lng)
			call.update_location()
			loc = (lat, lng)


		try:
			call.put()
			context = {
						'msg':'Complaint from <b>%s</b> logged.<br />Officers notified: %s' % (call.caller, getNearestOfficers(call.location)) }
						#'msg':'Complaint from <b>%s</b> logged.<br />Officers notified: %s' % (call.caller, loc) }
			self.response.out.write( pages.index % context )
		except:
			self.response.out.write( pages.index % {'msg':'System error.'} )







class UpdateOfficerLocPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write( pages.officer_loc % {'msg':''} )
	
	def post(self):
		#Simply post data into datastore.
		#and confirm post
		
		officer = Police_officer_loc( location=db.GeoPt(0, 0) )
		officer.name = self.request.get('officer')
		officer.last_known_location = "%s, ghana" % self.request.get('last_known_location')
		
		lat, lng = getGeoCode( officer.last_known_location )
		loc = "Unknown"
		if lat or lng:
			officer.location = db.GeoPt(lat, lng)
			officer.update_location()
			loc = (lat, lng)

		try:
			officer.put()
			context = {
						'msg':'Officer %s\'s location has been updated.' % officer.name }
						#'msg':'Complaint from <b>%s</b> logged.<br />Officers notified: %s' % (call.caller, loc) }
			self.response.out.write( pages.officer_loc % context )
		except:
			self.response.out.write( pages.officer_loc % {'msg':'System error.'} )






class RssCrime(webapp.RequestHandler):
	def get(self):
		
		crimes = Call.all()
		list_of_reported_crimes = []
		i = 0

		for crime in crimes:
			i += 1
			list_of_reported_crimes.append(
				PyGeoRSS.RSSItem(
					title = crime.caller,
					link = "http://911ghana.appspot.com/",
					description = crime.complaint,
					pubDate = crime.date,
					guid = PyGeoRSS.Guid("http://911ghana.appspot.com/%s" % str(i) ),
					geo_rss_pt = PyGeoRSS.GeoRssPoint(crime.location.lat, crime.location.lon),
					#location = PyGeoRSS.GeoRssPoint(0, 0),
				)
			)
			
		
		rss = PyGeoRSS.RSS2(
			title = "911Ghana Crime feed",
			link = "http://911ghana.appspot.com/rsscrime",
			description = "Realtime crime feed.",
			lastBuildDate = datetime.datetime.now(),

			items = list_of_reported_crimes)

		rss_response = StringIO()
		rss.write_xml(rss_response)
		d = datetime.datetime.now()
		
		self.response.headers["Content-Type"] = "application/rss+xml"
		self.response.headers.add_header("Expires", d.strftime("%a, %d %b %Y %H:%M:%S GMT"))
		self.response.out.write(rss.to_xml())

		rss_response.close()
		




application = webapp.WSGIApplication(
                                     [
										('/', MainPage),
										('/rsscrime.*', RssCrime),
										('/update_location', UpdateOfficerLocPage),
									 ],
                                     debug=True)

	
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
