from twisted.internet.defer import Deferred

from tubing.sink import Sink, LoopingSink

class Source(object):

      def __init__(self):
          self.sink    = None
          self.data    = []
          self.tubeSeries = ()

      def flowTo(self, series):
          if isinstance(series, tuple):
             self.tubeSeries = series
          elif isinstance(series, Sink):
             self.sink = series
          return self

      def flowTo(self, series):
          if isinstance(series, tuple):
             self.tubeSeries = series
          elif isinstance(series, Sink):
             self.sink = series
          return self

      def received(self, item):
          _data = item

          for tube in self.tubeSeries:
              _data = tube.received(_data)
          self.sink.received(_data)

      def deferredReceived(self, item):
          _data = item

          for tube in self.tubeSeries:
              _data.addCallback(tube.received)

          _data.addCallback(self.sink.received)

          if isinstance(self.sink, LoopingSink):
             _data.addCallback(self.sink.loop)

          _data.addErrback(self.retry, self, self.retry_args)

      def lazyReceive(self, item):
          self.data.append(item)

      def flow(self):
          for item in self.data:
              _data = item
              for tube in self.tubeSeries:
                  _data = tube.received(_data)
              self.sink.received(_data)
          self.data = []

      def flowFailed(self, function, args):
          self.retry      = function
          self.retry_args = args
