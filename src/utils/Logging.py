import logging
import os
from datetime import date


def logging_setup():
    log_dir = f"/app/logs/{date.today()}"  # Path inside the container
    # Create a 'logs' directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(log_dir, f'internal.log'),
        level=logging.INFO,
        format="%(name)s %(asctime)s %(levelname)s %(message)s"
    )

    return logging.getLogger(__name__)