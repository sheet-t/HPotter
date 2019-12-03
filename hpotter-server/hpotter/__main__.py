import signal, sys, inspect, os

import hpotter.plugins
from hpotter.docker.controller import startup_hpotter, shutdown_hpotter
from hpotter.env import logger, stop_shell, close_db

def shutdown_servers(signum, frame):
    shutdown_hpotter()
    # shell might have been started by telnet, ssh, ...
    stop_shell()
    close_db()

def shutdown_win_servers(signum):
    stop_hpotter()
    # shell might have been started by telnet, ssh, ...
    stop_shell()
    close_db()

# if sys.platform != 'win32':
#     if "__main__" == __name__:
#       signal.signal(signal.SIGTERM, shutdown_servers)
#       signal.signal(signal.SIGINT, shutdown_servers)
#     start_plugins()
# else:
#     if "__main__" == __name__:
#        import win32api
#        win32api.SetConsoleCtrlHandler(shutdown_win_servers)
#     start_plugins()

if "__main__" == __name__:
    if sys.platform != 'win32':
        signal.signal(signal.SIGTERM, shutdown_servers)
        signal.signal(signal.SIGINT, shutdown_servers)
    else:
        import win32api
        win32api.SetConsoleCtrlHandler(shutdown_win_servers)
    startup_hpotter()
