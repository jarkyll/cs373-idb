from flask import Flask

app = Flask(__name__)


@app.route("/")
def homepage():
	return "Hi there, this is where you return the html"



@app.route("/about")
def about():
	return "this html is about us"


@app.route("/characters")
def characters():
	return "this html is about the list of characters"


@app.route("/comicseries")
def series():
	return "this html is about the list of comic book series"

@app.route("/publishers")
def publishers():
	return "this html is about the list of comic book publishers"



if __name__=="__main__":
	app.run()
