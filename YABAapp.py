from flask import render_template

from app import create_app

app = create_app()

@app.route('/')
@app.route('/index')
def index():
    """ serves static index file """
    return render_template('index.html')

if __name__ == '__main__':
    app.run()  # Run the app