from flask import render_template
from flaskexample import app
from flask import request
from a_getUrl import getUrl

@app.route('/')
@app.route('/index')
def index():
   user = { 'nickname': 'Miguel' } # fake user
   #photo1 = 'http://i.imgur.com/Oyz9Lgg.jpg'
   photo1 = open('waitrose.jpg', 'rb').read().encode('base64').replace('\n', '')
   return render_template("basic.html",
       title = 'Home',
       photo1 = photo1,
       user = user)

@app.route('/input')
def basic_input():
    return render_template("input.html")

@app.route('/output')
def basic_output():
	theUrl = getUrl()
	return render_template("output.html",
		theUrl = theUrl)
