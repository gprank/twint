import logging, os

from .config import Config
from .__version__ import __version__
from . import run
from logging.handlers import RotatingFileHandler
import datetime

logger = logging.getLogger()
_output_fn = './logs/twint.log'
os.makedirs(os.path.dirname(_output_fn), exist_ok=True)
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(_output_fn, maxBytes=16000, backupCount=5)
formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug("___________________________________")
logger.debug(_output_fn)
now = datetime.datetime.now()
logger.info("Starting... " + now.strftime("%Y-%m-%d %H:%M:%S"))