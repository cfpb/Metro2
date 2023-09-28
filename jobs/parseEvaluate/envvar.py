import os
import logging
import sys


def fetch_env_var(var_name: str, default=None):
    logger = logging.getLogger('envvar.fetch_env_var')
    # Get an environment variable from the environment. If the var is
    # not present, use the provided default. If no default, exit
    # with an error message.
    try:
        return os.environ[var_name]
    except KeyError as e:
        if default != None:
            logger.debug(f"Using default value for env var {var_name}: {default}")
            return default
        else:
            logger.error(f"Required env var not set: {var_name}. Exiting.")
            raise
