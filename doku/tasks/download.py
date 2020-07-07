from typing import List, Optional

from flask import current_app

from doku import create_app
from doku.tasks import celery


@celery.task
def request_download(
    download_all: bool = False,
    include: Optional[List[int]] = None,
    exclude: Optional[List[int]] = None,
):
    """Request Download Task

    Request download
    """
    app = create_app(minimal=True)
    with app.app_context():
        current_app.logger.warn("hello")
