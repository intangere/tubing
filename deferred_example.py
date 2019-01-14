from twisted.internet       import reactor
from twisted.internet.task  import react
from twisted.internet.defer import inlineCallbacks
from twisted.web.client     import Agent
from twisted.internet.defer import Deferred
from twisted.internet.defer import returnValue

from tubing.source  import Source
from tubing.sink    import LoopingSink
from tubing.tube    import tube
from tubing.visual  import dump
from tubing.tlogging import log

from treq import get
from json import loads

@tube
class RequestTube(object):
      """Deferred generator for our Source"""
      def received(self, _):
          page = get('https://api.ipify.org?format=json')
          return page

@tube
class DataTube(object):
      """Yield from the request and return the data"""
      @inlineCallbacks
      def received(self, page):
          req = yield page
          data = yield req.text()
          return data

@tube
class ParseTube(object):
      """Get the ip from the data"""
      def received(self, data):
          return loads(data)['ip']

class IPSink(LoopingSink):
    """Show the ip"""
    def received(self, ip):
        print('Your ip is: %s' % ip)

def retry(error, source, _):
    log('Network Error', 'Treq request failed. Retrying..')
    source.deferredReceived()

@inlineCallbacks
def main(reactor):

    source = Source()
    series = (DataTube(), ParseTube())
    sink   = IPSink(source = source, delay = 5)

    source.flowFrom(RequestTube())
    source.flowTo(series).flowTo(sink)
    source.flowFailed(retry, args=[])
    source.deferredReceived()

    dump(source, series, sink)

    yield Deferred()

if __name__ == '__main__':
   react(main)
