import importlib
import signal

import hpotter.plugins
from hpotter.env import logger, stop_shell, close_db

plugins_dict = hpotter.plugins.__dict__

def shutdown_servers(signum, frame):
    for plugin_name in plugins_dict['__all__']:
        importlib.import_module('hpotter.plugins.' + plugin_name)
        plugin = plugins_dict[plugin_name]
        logger.info('Stopping %s', plugin_name)
        plugin.stop_server()
        logger.info('Done stopping %s', plugin_name)

    # shell might have been started by telnet, ssh, ...
    stop_shell()
    close_db()

def startup_servers():
    for plugin_name in plugins_dict['__all__']:
        importlib.import_module('hpotter.plugins.' + plugin_name)
        plugin = plugins_dict[plugin_name]
        logger.info('Starting %s', plugin_name)
        plugin.start_server()

if "__main__" == __name__:
    signal.signal(signal.SIGTERM, shutdown_servers)
    signal.signal(signal.SIGINT, shutdown_servers)

    startup_servers()
