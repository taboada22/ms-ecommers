import logging, os
from dotenv import load_dotenv
from pathlib import Path


basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))

def format_logs(name):
    log_route = os.environ.get('LOG_REG')
    log_name = name + '.log'
    log_files = os.path.join(log_route, log_name)
    my_logger = logging.getLogger(name)
    my_logger.setLevel(logging.DEBUG)

    if not my_logger.handlers:
        format = logging.Formatter('%(asctime)s - %(threadName)s - %(processName)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(log_files)
        handler.setFormatter(format)
        my_logger.addHandler(handler)
        my_logger.propagate = False

    return my_logger
