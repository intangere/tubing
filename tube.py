from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implementer

from zope.interface.verify import verifyClass


def tube(cls):
    """
    C{tube}: Class wrapper to create tubes.
    :param cls: A class with a received method.
    Creates the attributes needed for the tube
    """
    def received(self, item):
        """
        The function called when data is received
        """
        print('Default called')

    attrs = [('received', received)]

    notDef = object()

    for name, value in attrs:
        if getattr(cls, name, notDef) is notDef:
           setattr(cls, name, value)

    setattr(cls, '_name', cls.__name__)

    cls = implementer(Tube)(cls)
    verifyClass(Tube, cls)
    return cls

class Tube(Interface):
      """
      L{Tube} implements the tube interface.
      Creates the attributes needed for the tube.
      All a tube does is transform inputs into outputs
      These tubes SHOULD be based on generators.
      """
      inputType = Attribute(
           """Type of the data expected from the source"""
      )

      outputType = Attribute(
          """The type of the data expected for the sink"""
      )

      def received(item):
          """An item was recieved from another tube or source"""

@implementer(Tube)
class TubeImp(object):
      """A tube created for C{@tube}"""
      def __init__(self, inputType, outputType, received, name):
          self.inputType  = inputType
          self.outputType = outputType
          self.received   = received
          self._name      = name
