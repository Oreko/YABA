from flask import Flask, render_template


def bad_request(error):
    """ 400 error handler """
    return render_template('errors/400.html'), 400

def page_not_found(error):
    """ 404 error handler """
    return render_template('errors/404.html'), 404

def server_error(error):
    """ 500 error handler """
    return render_template('errors/500.html'), 500


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Register the blueprint controllers
    from app.yaba.controllers import yaba
    app.register_blueprint(yaba)

    # Resister error handlers
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    return app