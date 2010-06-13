import PyRSS2Gen

__name__ = "PyGeoRSS"



_element = PyRSS2Gen._element
_opt_element = PyRSS2Gen._opt_element

IntElement = PyRSS2Gen.IntElement
DateElement = PyRSS2Gen.DateElement
Category = PyRSS2Gen.Category
Cloud = PyRSS2Gen.Cloud
Image = PyRSS2Gen.Image
Guid = PyRSS2Gen.Guid
TextInput = PyRSS2Gen.TextInput
Enclosure = PyRSS2Gen.Enclosure
Source = PyRSS2Gen.Source
SkipHours = PyRSS2Gen.SkipHours
SkipDays = PyRSS2Gen.SkipDays



class GeoRssPoint:
	"""Publish a guid

	Defaults to being a permalink, which is the assumption if it's
	omitted.  Hence strings are always permalinks.
	"""
	def __init__(self, lat, lng):
		self.lat = str(lat)
		self.lng = str(lng)
	def publish(self, handler):
		d = {}

		_element(handler, "georss:point", "%s %s" % (self.lat, self.lng), d)
		_element(handler, "geo:lat", self.lat, d)
		_element(handler, "geo:long", self.lng, d)

class RSSItem(PyRSS2Gen.RSSItem):
	"""Publish an RSS Item"""
	element_attrs = {}
	def __init__(self, **kw):
		
		if hasattr(PyRSS2Gen.RSSItem, '__init__'):
			PyRSS2Gen.RSSItem.__init__(self, **kw)
			
		if kw.has_key('geo_rss_pt'):
			self.location = kw['geo_rss_pt']

	def publish_extensions(self, handler):
		if hasattr(self, 'location'):
			_opt_element(handler, "georss", self.location)



class RSS2(PyRSS2Gen.RSS2):
	def __init__(self, **kw):
		
		if hasattr(PyRSS2Gen.RSS2, '__init__'):
			PyRSS2Gen.RSS2.__init__(self, **kw)
		
		self.rss_attrs['xmlns:georss'] = 'http://www.georss.org/georss'
		self.rss_attrs['xmlns:geo'] = 'http://www.w3.org/2003/01/geo/wgs84_pos#'
