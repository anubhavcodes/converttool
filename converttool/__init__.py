import csv
import os
import logging

logger = logging.getLogger('converttool')
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
