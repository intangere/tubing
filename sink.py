from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implementer

from zope.interface.verify import verifyClass

from twisted.internet import reactor

class Sink(object):

      def __init__(self):
          self.sink   = None
          self.source = None
          self.data   = []

      def flowFrom(self, source):
          self.source = source

      def received(self, item):
          self.data.append(item)

      def _consume(self):
          return

      def consume(self):
          for item in self.tube:
              self._consume(item)

          self.source.data = []

      def consumeAll(self):
          self._consume(self.data)
          self.source.data = []

class LoopingSink(Sink):

      def __init__(self, source, deferred, delay):
          self.source   = source
          self.deferred = deferred
          self.delay    = delay

      def loop(self, _):
          reactor.callLater(self.delay, self.source.deferredReceived, self.deferred)
