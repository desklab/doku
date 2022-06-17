import os
import zipfile
import shutil
from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from werkzeug.security import safe_join

from doku.tasks import celery
from doku.models import db
from doku.models.document import Document
from doku.utils import EMPTY


@celery.task(bind=True)
def request_download(
    self,
    download_all: bool = False,
    include: Optional[List[int]] = None,
    exclude: Optional[List[int]] = None,
):
    """Request Download Task

    Request download
    """
    from doku import create_app

    app = create_app(minimal=True)
    with app.app_context():
        if download_all or exclude not in EMPTY:
            include = set(
                [_id[0] for _id in db.session.query(Document.id).distinct().all()]
            )
        if exclude not in EMPTY:
            include -= set(exclude)
        if include in EMPTY:
            return None

        task_id = self.request.id
        shared_dir = app.config.get("SHARED_FOLDER")
        directory = safe_join(shared_dir, str(task_id))
        os.mkdir(directory)
        try:
            zip_filename = f"{task_id}.zip"
            zip_path = safe_join(shared_dir, zip_filename)
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
                for document_id in include:
                    try:
                        document = (
                            db.session.query(Document).filter_by(id=document_id).one()
                        )
                    except NoResultFound:
                        app.logger.warning(f"No document found with ID {document_id}")
                        continue
                    filename = f"{document.filename}.pdf"
                    document_path = safe_join(directory, filename)
                    document.write_pdf(document_path)
                    archive.write(document_path, arcname=filename)
            return zip_filename
        finally:
            shutil.rmtree(directory)
