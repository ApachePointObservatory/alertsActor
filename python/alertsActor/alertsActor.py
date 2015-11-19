from __future__ import division, absolute_import

import opscore

import RO.Comm.HubConnection
# from RO.Comm.TwistedTimer import Timer

from twistedActor import Actor, expandUserCmd, log, UserCmd

# from .commandSet import arcticFWCommandSet
from .version import __version__

tronHost = "localhost"
tronCmdrPort = 6093

def stateCallback (sock):
    state, reason = sock.fullState
    if reason:
        print("%s: %s" % (state, reason))
    else:
        print(state)

class AlertsActor(Actor):
    # State options
    DefaultTimeLim = 5 # default time limit, in seconds
    def __init__(self,
        name,
        userPort,
        testMode=False,
    ):
        """!Construct an AlertsFWActor

        @param[in] name  actor name
        @param[in] userPort  int, a port on which this thing runs
        @param[in] testMode  bool.
        """
        Actor.__init__(self,
            userPort = userPort,
            maxUsers = 1,
            name = name,
            version = __version__,
            )

        # setup hub dispatcher
        # network connection
        if testMode:
            print "Running in test mode, no real connection possible"
            connection = RO.Comm.HubConnection.NullConnection(stateCallback=stateCallback)
        else:
            connection = RO.Comm.TCPConnection.TCPConnection(
                host = tronHost,
                port = tronCmdrPort,
                stateCallback=stateCallback,
                )
            connection.cmdr = name
        # keyword dispatcher
        self.dispatcher = opscore.actor.cmdkeydispatcher.CmdKeyVarDispatcher(
            name = name,
            connection = connection,
            includeName = True, # this is required to keep the hub happy
            callKeyVarsOnDisconnect = True,
        )


        opscore.actor.model.Model.setDispatcher(self.dispatcher)
        self.models = {}
        for actor in ["tcc"]:#["boss", "guider", "platedb", "mcp", "sop", "tcc", "apogee"]:
            self.models[actor] = opscore.actor.model.Model(actor)


    @property
    def connection(self):
        return self.dispatcher.connection

    def init(self, userCmd=None, getStatus=True, timeLim=DefaultTimeLim):
        """! Initialize all devices, and get status if wanted
        @param[in]  userCmd  a UserCmd or None
        @param[in]  getStatus if true, query all devices for status
        """
        userCmd = expandUserCmd(userCmd)
        log.info("%s.init(userCmd=%s, timeLim=%s, getStatus=%s)" % (self, userCmd, timeLim, getStatus))
        # if getStatus:
        #     self.cmd_status(userCmd) # sets done
        # else:
        #     userCmd.setState(userCmd.Done)
        userCmd.setState(userCmd.Done)
        return userCmd

    def cmd_init(self, userCmd):
        """! Implement the init command
        @param[in]  userCmd  a twistedActor command
        """
        log.info("%s.cmd_init(userCmd=%s)"%(self, str(userCmd)))
        # print("%s.cmd_init(userCmd=%s)"%(self, str(userCmd)))
        self.init(userCmd, getStatus=True)
        # userCmd.setState(userCmd.Done)
        return True

    def cmd_ping(self, userCmd):
        """! Implement the ping command
        @param[in]  userCmd  a twistedActor command
        """
        log.info("%s.cmd_ping(userCmd=%s)"%(self, str(userCmd)))
        # print("%s.cmd_ping(userCmd=%s)"%(self, str(userCmd)))
        userCmd.setState(userCmd.Done, textMsg="alive")
        return True

    def cmd_status(self, userCmd=None):
        userCmd = expandUserCmd(userCmd)
        self.writeToUsers("i", "text=Status!", userCmd)
        userCmd.setState(userCmd.Done)
        return True

    def cmd_connect(self, userCmd=None):
        """!Connect to the hub

        @param[in]  userCmd  a twistedActor command
        """
        userCmd = expandUserCmd(userCmd)
        self.connection.connect()
        userCmd.setState(userCmd.Done)
        return True








