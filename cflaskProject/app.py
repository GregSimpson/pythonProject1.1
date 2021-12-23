
from flask import Flask, url_for, request, jsonify, render_template
##from flasgger import Swagger

# https://www.jetbrains.com/help/pycharm/creating-flask-project.html
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
# https://flask.palletsprojects.com/en/2.0.x/tutorial/

app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#	# return 'Hello World!'
#	return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello(name):
	return f"Hello, {escape(name)}!"


@app.route('/index')
def index1():
	return 'Index1 Page'


@app.route('/hello2')
def hello2():
	return 'Hello2, World'


from markupsafe import escape


@app.route('/user1/<username>')
def show_user_profile(username):
	# show the user profile for that user
	return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
	# show the post with the given id, the id is an integer
	return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	# show the subpath after /path/
	return f'Subpath {escape(subpath)}'


# trailing slash
@app.route('/projects/')
def projects():
	return 'The project page'


@app.route('/about')
def about():
	return 'The about page'


# ---
@app.route('/')
def index2():
	return 'index2'


@app.route('/login')
def login():
	return 'login'


@app.route('/user/<username>')
def profile(username):
	return f'{username}\'s profile'


# shows the urls for the endpoints that url_for calls
with app.test_request_context():
	print(url_for('index2'))
	print(url_for('login'))
	print(url_for('login', next='/'))
	print(url_for('profile', username='John Doe'))
	print(url_for('static', filename='style.css'))


@app.route('/login', methods=['GET', 'POST'])
def login4():
	if request.method == 'POST':
		return do_the_login()
	else:
		return show_the_login_form()


def do_the_login():
	return 'do_the_login'


def show_the_login_form():
	return 'show_the_login_form'




@app.route('/hello3/')
@app.route('/hello3/<name>')
def hello3(name=None):
	return render_template('hello.html', name=name)




with app.test_request_context('/hello3', method='POST'):
	# now you can do something with the request until the
	# end of the with block, such as basic assertions:
	assert request.path == '/hello3'
	assert request.method == 'POST'


#@app.route('/login5', methods=['POST', 'GET'])
#def login5():
#    error = None
#    if request.method == 'POST':
#        if valid_login(request.form['username'],
#                       request.form['password']):
#            return log_the_user_in(request.form['username'])
#        else:
#            error = 'Invalid username/password'
#    # the code below is executed if the request method
#    # was GET or the credentials were invalid
#    return render_template('login.html', error=error)



@app.route("/users")
def users_api():
    users = "user1, user2, user45" #get_all_users()
    return jsonify([user.to_json() for user in users])

if __name__ == '__main__':

	app.run()
