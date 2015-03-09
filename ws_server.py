import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
from tornado import websocket
import motor

from tornado.options import define, options
define("port", default=8002, help="run on the given port", type=int)

db = motor.MotorClient('localhost', 27017).test_db
collection = db.test_collection

class EchoWebSocket(websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"

    @tornado.gen.coroutine
    def on_message(self, message):
        yield collection.insert({"message": message})
        document = yield collection.find_one({"message": message})
        self.write_message(u"You said: " + document["message"])
        collection.remove({"message": message})

    def on_close(self):
        print "WebSocket closed"


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/ws", EchoWebSocket)],
        db=db
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

