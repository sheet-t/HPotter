import signal, sys, inspect, os

import hpotter.plugins
from hpotter.plugins.handler import start_plugins, stop_plugins
from hpotter.env import logger, stop_shell, close_db

def shutdown_servers(signum, frame):
    """
    Shutdown HPotter servers.

    Stop all running plugins, shutdown docker shell, close SQLite database.
    
    Parameters:
        signum (int): Signal received by HPotter.
        frame (frame object): Stack frame interrupted by given signum.
    """
    stop_plugins()
    stop_shell()
    close_db()

def shutdown_win_servers(signum):
    """
    Shutdown HPotter servers (Windows).

    Provide a method for shutting down servers that can be parsed by win32api.
    
    Parameters:
        signum (int): Signal received by HPotter.
    """
    stop_plugins()
    stop_shell()
    close_db()

if sys.platform != 'win32':
    """Provide signal handling for UNIX systems"""
    if "__main__" == __name__:
      signal.signal(signal.SIGTERM, shutdown_servers)
      signal.signal(signal.SIGINT, shutdown_servers)
    start_plugins()
else:
    """Provide signal handling for Windows systems"""
    if "__main__" == __name__:
       import win32api
       win32api.SetConsoleCtrlHandler(shutdown_win_servers)
    start_plugins()
