import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
import websocket
import uuid
import gevent
from gevent import pool
from gevent import monkey
monkey.patch_all()

from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

ws_keeper = {}
p = pool.Pool(20)

class IndexHandler(tornado.web.RequestHandler):

    @staticmethod
    def random_string():
        return str(uuid.uuid4())

    def ws_conn(self):
        if id(gevent.getcurrent()) not in ws_keeper:
            ws = websocket.create_connection("ws://localhost:8002/ws")
            ws_keeper[id(gevent.getcurrent())] = ws
        else:
            ws = ws_keeper[id(gevent.getcurrent())]
        ws.send(self.random_string())
        result = ws.recv()
        # print "Received '%s'" % result

    def get(self):
        p.spawn(self.ws_conn)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
