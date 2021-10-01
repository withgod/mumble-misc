#!/usr/bin/env python
# -*- coding: utf-8

import sys,os,string,Ice
from datadog import initialize, statsd

proxy = 'Meta:tcp -h 127.0.0.1 -p 6502'
slice = '/usr/share/slice/Murmur.ice'
server = 1


Ice.loadSlice("--all -I%s %s" % ("/usr/share/ice/slice", slice))
import Murmur
ice = Ice.initialize()
prx = ice.stringToProxy(proxy)
murmur = Murmur.MetaPrx.checkedCast(prx)

_server = murmur.getServer(server)
server_name = _server.getConf("registerName")
user_count  = 0

if _server.isRunning:
	server_version = murmur.getVersion()
	# release 1.1.8  or under getPlayers but now trunk is getUsers
	if server_version[0] <= 1 and server_version[1] <= 1 and server_version[2] <= 8:
		user_count = len(_server.getPlayers())
	else:
		user_count = len(_server.getUsers())

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

initialize(**options)
statsd.gauge('murmur.users', user_count)
print "mumble.users %d" % (user_count)


if ice:
    try:
        ice.destroy()
    except:
        traceback.print_exc()
        status = 1

