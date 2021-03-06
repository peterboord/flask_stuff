# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from app import app
from a_getImgData import getImgData

@app.route('/_screenClick')
def screenClick():
	x = request.args.get('x', 0, type=int)
	y = request.args.get('y', 0, type=int)
	busNo = request.args.get('busNo', 0, type=int)
	dataDic = getImgData(x,y,busNo)
	return jsonify(dataDic)

@app.route('/talkStart')
def talkStart():
	return render_template('talkStart.html')

@app.route('/talkContinue')
def talkContinue():
	return render_template('talkContinue.html')

@app.route('/')
def index():
	imgUrl='http://i.imgur.com/wIj4B4Xg.jpg'
	return render_template('index.html', imgUrl = imgUrl)

if __name__ == '__main__':
    app.run()
