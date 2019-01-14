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
from tubing.logging import log

from bs4  import BeautifulSoup
from treq import get
from json import loads

from proxy.proxy     import setupAgent
from socketIO_client import SocketIO, BaseNamespace

import time
from hashlib import sha256

from utils.tools import timestamp, simpleFmt
from random import choice


socketIO = SocketIO('52.232.81.82', 5000)
chat_namespace = socketIO.define(BaseNamespace, '/restocks')

