from flask import Flask,render_template

# https://stackoverflow.com/questions/23327293/flask-raises-templatenotfound-error-even-though-template-file-exists

app=Flask(__name__,template_folder='templates')


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about/")
def about():
    return render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)
