import logging
import os
from datetime import date


def logging_setup():
    log_dir = os.getenv("LOGGING_DIR_PATH")
    if len(log_dir) > 0 and log_dir[-1] == '/':
        log_dir = log_dir[:-1]
    log_dir = f"{log_dir}/{date.today()}"
    # Create a 'logs' directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(log_dir, f'internal.log'),
        level=logging.DEBUG,
        format="%(name)s %(asctime)s %(levelname)s %(message)s"
    )