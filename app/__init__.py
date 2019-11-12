from flask import Flask, render_template


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Register the blueprint controllers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp)

    from app.index import bp as index_bp
    app.register_blueprint(index_bp)

    return app
