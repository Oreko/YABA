from flask import render_template

from app.errors import bp

@bp.app_errorhandler(400)
def bad_request(error):
    """ 400 error handler """
    return render_template('errors/400.html'), 400

@bp.app_errorhandler(404)
def page_not_found(error):
    """ 404 error handler """
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def server_error(error):
    """ 500 error handler """
    return render_template('errors/500.html'), 500
