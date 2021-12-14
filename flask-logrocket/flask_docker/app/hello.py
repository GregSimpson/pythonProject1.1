from flask import Flask, render_template
import os
# https://stackoverflow.com/questions/23327293/flask-raises-templatenotfound-error-even-though-template-file-exists
# app = Flask(__name__, template_folder='templates')
app=Flask(__name__,template_folder='templates')


@app.route("/")
def home():
	return render_template('home.html')


@app.route("/about/")
def about():
	return render_template('about.html')


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)


'''
from flask import Flask, render_template
import os

#  app = Flask(__name__)
app=Flask(__name__,template_folder='templates')


# @app.route('/')
@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
'''
