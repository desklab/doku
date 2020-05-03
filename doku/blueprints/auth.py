from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, BadRequest
from flask import Blueprint, session, redirect, url_for, request, \
    render_template

from doku.models import db
from doku.models.user import User
from doku.utils.decorators import login_required

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
@login_required
def logout():
    # remove the username from the session if it's there
    session.authenticated = False
    return redirect(url_for('base.index'))


@bp.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('sites/auth/account.html')


@bp.route('/account/password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('rpt_password')
    if not new_password == confirm_password:
        return render_template(
            'sites/auth/account.html',
            error_new='Passwords don\'t match'), BadRequest.code
    user = db.session.query(User).filter_by(username=session['user']).one()
    if not user.check_password(old_password):
        return render_template(
            'sites/auth/account.html',
            error_old='Invalid password'), BadRequest.code
    user.set_password(new_password)
    db.session.commit()
    return redirect(url_for('auth.account'))
