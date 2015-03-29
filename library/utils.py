from functools import wraps
from flask.ext.login import current_user
from werkzeug.exceptions import abort


def can_edit_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated() or \
                not current_user.can_edit:
            abort(404)
        return view(*args, **kwargs)
    return wrapper