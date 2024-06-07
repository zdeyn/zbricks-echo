from .base import zBrick
from .augmentations import handler
from .logging import zbricks_logger
logger = zbricks_logger(__name__)

if __name__ == '__main__':
    logger.info("Running as main.")
    brick = zBrick()
    brick._dump()