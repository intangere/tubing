from twisted.internet       import reactor
from twisted.internet.task  import react
from twisted.internet.defer import inlineCallbacks
from twisted.web.client     import Agent

from treq   import get
from source import Source
from sink   import Sink
from tube   import tube
from json   import loads

agent   = 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0'
url     = 'some url'

headers = {
             'User-Agent' : agent
          }

_IGNORE = 'ignored'


@tube
class MonitorTube(object):

      def received(self, page):
          try:
           json = loads(page)
           return json
          except Exception as e:
           print(e)

@tube
class TreqTube(object):

      def received(self, _):
          return _

class ProductSink(Sink):

      def parseProducts(self, json):
          for product in json['products']:
              print('[Product]: %s' % product['title'].encode())
          reactor.stop()

      def received(self, items):
          self.parseProducts(items)

@inlineCallbacks
def main(reactor):

    source = Source()
    sink   = ProductSink()


    series = (TreqTube(), MonitorTube())

    source.flowTo(series).flowTo(sink)
    d    = yield get(url, headers = headers, agent = Agent(reactor))
    text = yield d.text('utf8')
    source.received(text)

if __name__ == '__main__':
   react(main)

#Tubes can be combined with inlineCallbacks as well. You don't have to get the deferred result first. You can directly pass in a deferred to source.received.
#This just shows how you can combine tubes with treq.
