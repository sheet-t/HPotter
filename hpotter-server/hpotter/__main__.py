import signal, sys, inspect, os

import hpotter.plugins
from hpotter.plugins.handler import start_plugins, stop_plugins
from hpotter.env import logger, stop_shell, close_db
from hpotter.plugins.ssh import create_ssh_rules
from hpotter.plugins.telnet import create_telnet_rules

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
    print("Creating SSH iptables rule")
    create_ssh_rules()
    print("Creating Telnet iptable rule")
    create_telnet_rules()

def deleteiptables():
    print("Deleting SSH and telnet iptables rules")
    table = iptc.Table('filter')
    hpotterchain = iptc.Chain(iptc.Table(iptc.Table.FILTER), 'INPUT')
    print ("deleting ", len(hpotterchain.rules), "rules from", table.name, "/", hpotterchain.name)
    rules = hpotterchain.rules
    for rule in rules:
        hpotterchain.delete_rule(rule)
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