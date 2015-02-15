#!/usr/bin/python
"""
  MetaLog - binding of multiple log files
"""
# MetaLog serves three scenarios:
# 1) logging of several different sensor sources and effector commands
# 2) exact replay of the run (like from BlackBox)
# 3) fake replay when effectors commands are not asserted
# Note, that 3rd case can be split into two when at least send/receive
# structure is kept or even that is ignored.

import os.path
import datetime
import sys

from logio import ReplayLog, LoggedSocket

class MetaLog:
    def __init__( self, filename=None ):
        if filename is None:
            self.replay = False
            self.filename = datetime.datetime.now().strftime("logs/meta_%y%m%d_%H%M%S.log")
            self.f = open( self.filename, "w" )
            self.f.write( str(sys.argv)+"\n" )
            self.f.flush()
        else:
            self.replay = True
            self.filename = filename
            self.f = open( self.filename )


    def getLog( self, prefix ):
        for line in self.f:
            print "LINE", line.strip()
            if line.startswith( prefix ):
                ret = line.split()[1].strip()
                assert ret.startswith("logs/")
                return os.path.dirname( self.filename ) + os.sep + ret[4:]
        return None # not found


    def createLoggedSocket( self, prefix, headerFormat ):
        if self.replay:
            return ReplayLog( self.getLog( prefix ), headerFormat=headerFormat )
        else:
            filename = "logs/" + prefix + datetime.datetime.now().strftime("_%y%m%d_%H%M%S.bin") # bin? txt? log??
            self.f.write( prefix + ": " + filename + "\n")
            self.f.flush()
            return LoggedSocket( filename )


# vim: expandtab sw=4 ts=4 
