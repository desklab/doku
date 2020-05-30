from flask import current_app
from weasyprint import default_url_fetcher
from weasyprint.urls import URLFetchingError
from werkzeug.security import safe_join

from doku.models import db
from doku.models.resource import Resource
from doku.utils.db import get_or_404


def url_fetcher(url: str, **kwargs):
    if url.startswith('dokures:'):
        resource_id = url.lstrip('dokures:')
        try:
            resource_id = int(resource_id)
        except ValueError as exc:
            raise URLFetchingError(
                f'Unable to parse resource id {resource_id}') from exc
        resource: Resource = get_or_404(
            db.session.query(Resource).filter_by(id=resource_id)
        )
        mime_type = 'image/png'
        res_path = safe_join(
            current_app.config['UPLOAD_FOLDER'], resource.filename
        )
        return {
            'mime_type': mime_type,
            'file_obj': open(res_path, 'rb')
        }
    else:
        return default_url_fetcher(url, **kwargs)
