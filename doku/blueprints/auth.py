from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound
from flask import Blueprint, session, redirect, url_for, request, \
    render_template

from doku.models import db
from doku.models.user import User

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.authenticated:
        return redirect(url_for('base.index'))
    error: Optional[str] = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user: User = db.session.query(User).filter(
                User.email == email
            ).one()
            if user.check_password(password):
                session.authenticated = True
                session['user'] = user.username
                return redirect(url_for('base.index'))
            else:
                error = 'E-Mail and password do not match. Please try again'
        except NoResultFound:
            error = 'E-Mail and password do not match. Please try again'
    return render_template('sites/auth/login.html', error=error)


@bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.authenticated = False
    return redirect(url_for('base.index'))
