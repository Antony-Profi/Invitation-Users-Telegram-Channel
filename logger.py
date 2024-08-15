import logging
import os
import sys

from datetime import datetime


def setupLogger(log_file="app.log"):
    log_folder = "logging"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_path = os.path.join(log_folder, log_file)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setStream(open(sys.stdout.fileno(), mode='w', encoding='utf-8', closefd=False))

    return logging.getLogger(__name__)


logger = setupLogger()
