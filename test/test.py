from tube import tube
from source import Source
from sink import Sink

@tube
class ReverseTube(object):

      def received(self, item):
          return ''.join(reversed(item))

@tube
class TestTube(object):

      def received(self, item):
          return item

class EchoSink(Sink):
      def received(self, item):
          print('Data: %s' % item)

source = Source()
sink   = EchoSink()

series = (ReverseTube(), TestTube())
source.flowTo(series).flowTo(sink)
source.received('Some random data to echo')

source.lazyReceive('Some random data to echo')
source.lazyReceive('Some more data')
source.flow()

#Synchronous tubes do not need a twisted reactor running
#reactor.run()

