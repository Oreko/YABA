from flask import Blueprint, render_template

yaba = Blueprint('yaba', __name__, url_prefix='/posts')

@yaba.route('', methods=['GET'])
def temp_func():
    return render_template('test.html')