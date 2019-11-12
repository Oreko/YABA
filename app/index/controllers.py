from flask import render_template, url_for

from app.index import bp

@bp.route('/')
@bp.route('/index')
def index():
    """ serves static index file """
    post_number = 1234567890
    post_number_gifs = [url_for('static', filename="images/counter/{}.gif".format(num)) for num in str(post_number)]
    return render_template('index.html', post_number=(post_number, post_number_gifs))
