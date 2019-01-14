from tubing.source  import Source
from tubing.sink    import LoopingSink, Sink
from tubing.tube    import tube
from tubing.visual  import dump
from tubing.tlogging import log

from requests import get
from json import loads

@tube
class RequestTube(object):
      """Data Source"""
      def received(self, _):
          resp = get('https://api.ipify.org?format=json')
          return resp
@tube
class DataTube(object):
      """Get the text"""
      def received(self, resp):
          return resp.text

@tube
class ParseTube(object):
      """Get the ip from the data"""
      def received(self, data):
          return loads(data)['ip']

class IPSink(Sink):
    """Show the ip"""
    def received(self, ip):
        print('Your ip is: %s' % ip)

def retry(error, source, _):
    log('Network Error', 'Treq request failed. Retrying..')
    source.received()

def main():

    source = Source()
    series = (DataTube(), ParseTube())
    sink   = IPSink()

    source.flowFrom(RequestTube())
    source.flowTo(series).flowTo(sink)
    source.flowFailed(retry, args=[])

    dump(source, series, sink)

    source.received(None)

if __name__ == '__main__':
   main()
