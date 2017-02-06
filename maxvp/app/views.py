# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from app import app
from a_getImgData import getImgData

@app.route('/_imgClick')
def imgClick():
	x = request.args.get('x', 0, type=int)
	y = request.args.get('y', 0, type=int)
	dataDic = getImgData(x,y)
	return jsonify(dataDic)
                    

@app.route('/')
def index():
	imgData = open('/home/pboord/Downloads/yelp/waitrose.jpg', 'rb').read().encode('base64').replace('\n', '')
	return render_template('index.html', imgData = imgData)

if __name__ == '__main__':
    app.run()
