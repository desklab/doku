import os
import mimetypes

from flask import current_app
from weasyprint import default_url_fetcher
from weasyprint.urls import URLFetchingError
from werkzeug.security import safe_join


def url_fetcher(url: str, **kwargs):
    if url.startswith("dokures:"):
        resource = url.lstrip("dokures:")
        res_path = safe_join(current_app.config["UPLOAD_FOLDER"], resource)
        mime_type, __ = mimetypes.guess_type(res_path, strict=True)
        if mime_type is None:
            mime_type = 'image/*'
        if not os.path.isfile(res_path):
            raise URLFetchingError()
        return {"mime_type": mime_type, "file_obj": open(res_path, "rb")}
    else:
        return default_url_fetcher(url, **kwargs)
