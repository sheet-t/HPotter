import signal, sys, inspect, os

import hpotter.plugins
from hpotter.plugins.handler import start_plugins, stop_plugins
from hpotter.env import logger, stop_shell, close_db

def shutdown_servers(signum, frame):
    stop_plugins()
    if sys.platform == 'linux':
        deleteiptables()
    # shell might have been started by telnet, ssh, ...
    stop_shell()
    close_db()

def shutdown_win_servers(signum):
    stop_plugins()
    # shell might have been started by telnet, ssh, ...
    stop_shell()
    close_db()

def createiptables():
    import iptc	
    print("Creating HPotter iptable ruleset")
    table = iptc.Table(iptc.Table.FILTER)
    chain = table.create_chain("DOCKER")

def deleteiptables():
    import iptc
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "DOCKER")
    print("Deleting HPotter iptable ruleset")
    table = iptc.Table('filter')
    rules = chain.rules
    chains = chain
    #print ("deleting ", len(chains.rules), "rules from", table.name, "/", chain.name)
    for rule in rules:
        chain.delete_rule(rule)
    iptc.easy.delete_chain('filter','DOCKER', flush=True)
    table.commit()
    table.close()

if sys.platform != 'win32':
    if "__main__" == __name__:
      signal.signal(signal.SIGTERM, shutdown_servers)
      signal.signal(signal.SIGINT, shutdown_servers)
    if sys.platform == 'linux':
          createiptables()
    start_plugins()
else:
    if "__main__" == __name__:
       import win32api
       win32api.SetConsoleCtrlHandler(shutdown_win_servers)
    start_plugins()
