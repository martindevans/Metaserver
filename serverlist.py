from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import uuid

class ServerEntry(db.Model):
	name = db.StringProperty()
	address = db.StringProperty()
	secret = db.StringProperty()
	game = db.StringProperty()
	creation = db.DateTimeProperty(auto_now_add=True)
	modification = db.DateTimeProperty(auto_now=True)

def FilterEntries(webRequest):
	return ServerEntry.all().filter("game = ", webRequest.get('game'))
	
class ListHandler(webapp.RequestHandler):
    def get(self):
		self.response.headers["Content-Type"] = "text/plain"
	
		w = self.response.out.write
		w('<serverlist>')
		if (self.request.get('game') == ''):
			w('<error>No game defined</error>')
		else:
			for e in FilterEntries(self.request):
				w('<entry name="' + e.name + '" address="' + e.address + '" />')
		w('</serverlist>')

class CreateHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		
		gameOk = self.request.get('game') is not ''
		nameOk = self.request.get('name') is not ''
		addrOk = self.request.get('address') is not ''
		
		w = self.response.out.write
		w('<servercreate>')
		if (not gameOk):
			w("<error>No game defined</error>")
		if (not nameOk):
			w("<error>No name defined</error>")
		if (not addrOk):
			w("<error>No address defined</error>")
		if (gameOk and nameOk and addrOk):
			entry = ServerEntry()
			entry.name = self.request.get('name')
			entry.address = self.request.get('address')
			entry.game = self.request.get('game')
			entry.secret = str(uuid.uuid4())
			dbKey = db.put(entry)
			w("<db_key>" + str(dbKey) + "</db_key>")
			w("<secret>" + str(entry.secret) + "</secret>")
		w('<servercreate>')
		
class PingHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		
		secretOk = self.request.get('secret') is not ''
		
		w = self.response.out.write
		w('<pong>')
		if (not secretOk):
			w("<error>No secret defined</error>")
		else:
			entry = ServerEntry.all().filter("secret = ", self.request.get('secret')).get()
			if (not entry):
				w("<error>Not found</error>")
			else:
				if (self.request.get('delete') == 'true'):
					entry.delete()
					w('<deleted />')
				else:
					entry.put()
		w('</pong>')
		
def main():
    application = webapp.WSGIApplication([('/serverlist/list', ListHandler),
										  ('/serverlist/create', CreateHandler),
										  ('/serverlist/ping', PingHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()