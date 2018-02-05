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
url     = 'https://rise45.com/products.json?limit=1000'

headers = {
             'User-Agent' : agent
          }

_IGNORE = 'ignored'


@tube
class MonitorTube(object):

      #@inlineCallbacks
      def received(self, page):
          try:
           #text = yield self.undefer(page)
           json = loads(page)
           return json
          except Exception as e:
           print(e)

      @inlineCallbacks
      def undefer(self, deferred):
          print('Called')
          text = yield deferred#.text('utf8')
          print('Done')
          yield text

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

"""Output
[Product]: b'Nike Air Huarache Run Premium "ACG" (704830-200)'
[Product]: b'Vans Sherpa Slides (VN0004LGQ0X)'
[Product]: b'Adidas Ultra Boost 4.0 "Multi-Color" (BB6165)'
[Product]: b'Men\'s Timberland 6" Premium Field Boot "Reptile" (TB0A1PVH)'
[Product]: b'Timberland 6" Field Waterproof Boot "Burnt Sienna" (TB0A1NW4)'
[Product]: b'Air Jordan XIII Retro "Olive" (414571-006)'
[Product]: b'Adidas Ultra Boost Laceless "Black Boost" (BB6137)'
[Product]: b'Adidas EQT Cushion ADV "Black White Royal" (CQ2374)'
[Product]: b'Adidas EQT Cushion ADV "Colette Blue" (CQ2380)'
[Product]: b'Air Jordan 1 Retro Low "Metallic Gold" (554723-032)'
[Product]: b'Adidas NMD Racer Primeknit (CQ2441)'
[Product]: b'Adidas Prophere "Olive" (CQ3024)'
[Product]: b'Nike Air Foamposite One "Abalone" (575420-009)'
[Product]: b'Adidas x Daniel Arsham New York (CM7193)'
[Product]: b'Air Jordan XI Retro GS "Win Like \'96" (378038-623)'
[Product]: b'Air Jordan I Mid "Tumbled Leather" (554724-041)'
[Product]: b'Air Jordan I Retro High OG "LA" (555088-031)'
[Product]: b'Adidas Ultra Boost 4.0 "Pure White" (BB6168)'
[Product]: b'Adidas Ultra Boost 3.0 "Trace Khaki" (CG3039)'
[Product]: b'Timberland 6" Premium Waterproof Boot "640 Below" (TB0A1M98)'
[Product]: b'Adidas Prophere "Grey" (CQ3023)'
[Product]: b'Adidas Prophere "Black OG" (CQ3022)'
[Product]: b'Air Jordan XIII Retro "Altitude" (414571-042)'
[Product]: b'Nike Air Max 1 Anniversary "Obsidian" (908375-104)'
[Product]: b'Air Jordan VI Retro "Like Mike" (384664-145)'
[Product]: b"Adidas x Daniel Arsham New York 'Present' (DB1971)"
[Product]: b'Women\'s Nike Special Field Air Force 1 "Cedar Red" (857872-600)'
[Product]: b'Adidas NMD R2 "Vapor Grey" (CQ2399)'
[Product]: b'Adidas Iniki Runner I-5923 "White Gum" (B42224)'
[Product]: b'Adidas Iniki Runner I-5923 "Red Gum" (B42225)'
"""
