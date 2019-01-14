from twisted.internet.defer import Deferred

from tubing.sink import Sink, LoopingSink

import time

class Source(object):

      def __init__(self):
          self.sink    = None
          self.data    = []
          self.tubeSeries = ()
          self.sourceTube = None

      def flowFrom(self, tube):
          self.sourceTube = tube

      def flowTo(self, series):
          if isinstance(series, tuple):
             self.tubeSeries = series
          elif isinstance(series, Sink):
             self.sink = series
          return self

      def received(self, item):

          if isinstance(self.sink, LoopingSink):

             while True:

                _data = self.sourceTube.received(item)

                for tube in self.tubeSeries:
                    _data = tube.received(_data)

                self.sink.received(_data)
                time.sleep(self.sink.delay)
          else:
                _data = self.sourceTube.received(item)
                for tube in self.tubeSeries:
                    _data = tube.received(_data)

                self.sink.received(_data)

      def deferredReceived(self):
          _data = self.sourceTube.received(None)

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
