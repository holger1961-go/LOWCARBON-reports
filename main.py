from .utils.logging_setup import logger
from .pipeline.steps import Pipeline


logger.info("MAIN")

Pipeline().run("N")