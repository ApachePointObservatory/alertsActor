#!/usr/bin/env python2
from __future__ import division, absolute_import
"""Run the Arctic Filter Wheel actor
"""
import os

from twisted.internet import reactor
from twistedActor import startFileLogging

from alertsActor import AlertsActor


UserPort = 9995
# for now no logging
# homeDir = os.getenv("HOME")
# logDir = os.path.join(homeDir, "logs/arcticFilterWheel")

# try:
#     startFileLogging(logDir)
# except KeyError:
#    # don't start logging
#    pass

if __name__ == "__main__":
    print("AlertsActor running on port %i"%UserPort)
    AlertsActor = AlertsActor(name="AlertsActor", userPort=UserPort)
    reactor.run()