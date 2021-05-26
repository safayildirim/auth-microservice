import logging

from app import create_app

__LOGGING_FORMAT = '%(asctime)s [%(levelname)s:] %(message)s'
__LOGGING_DATEFMT = '%m/%d/%Y %I:%M:%S'

logging.basicConfig(level=logging.NOTSET,
                    format=__LOGGING_FORMAT, datefmt=__LOGGING_DATEFMT)

app = create_app()
app.run()
