import logging
import os
import sys

from envvar import fetch_env_var

LOGFILE_LOCATION = fetch_env_var('LOGFILE_LOCATION', "")
LOGFILE_LOGGING_LEVEL = fetch_env_var('LOGFILE_LOGGING_LEVEL', "DEBUG")
CONSOLE_LOGGING_LEVEL = fetch_env_var('CONSOLE_LOGGING_LEVEL', "INFO")

def getLogger(name):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.getLevelName(LOGFILE_LOGGING_LEVEL.upper()),
                    format='%(asctime)s, %(name)-12s: %(levelname)-8s %(message)s',
                    filename=os.path.join(LOGFILE_LOCATION, 'info.log'),
                    filemode='a')
    logger = logging.getLogger(name)

    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.getLevelName(CONSOLE_LOGGING_LEVEL.upper()))
    # create formatter and add it to the handlers
    ch_formatter = logging.Formatter('%(asctime)s, %(name)-12s: %(levelname)-8s %(message)s')

    ch.setFormatter(ch_formatter)
    # add the handlers to logger
    logger.addHandler(ch)

    return logger
