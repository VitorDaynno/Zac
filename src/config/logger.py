import coloredlogs
import logging

logger = logging.getLogger("Zac")
coloredlogs.install(level='DEBUG')

formatter = logging.Formatter(("%(asctime)s - %(name)s - %(levelname)s -"
                               "[%(filename)s] %(message)s"))
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
