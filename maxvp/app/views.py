# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from app import app
from a_getImgData import getImgData

@app.route('/_screenClick')
def screenClick():
	x = request.args.get('x', 0, type=int)
	y = request.args.get('y', 0, type=int)
	pc = request.args.get('pc', "black", type=str)
	busNo = request.args.get('busNo', 0, type=int)
	dataDic = getImgData(x,y,pc,"screenClick",busNo)
	return jsonify(dataDic)

@app.route('/_caseClick')
def caseClick():
	x = request.args.get('x', 0, type=int)
	y = request.args.get('y', 0, type=int)
        pc = request.args.get('pc', "black", type=str)
	busNo = request.args.get('busNo', 0, type=int)
	busNo += 1
        dataDic = getImgData(x,y,pc,"caseClick",busNo)
        #dataDic = {'yelpUrl': 'yelp.com', 'imgData': '', 'boxText': '', 'clientx' : x, 'clienty' : y, 'busNo' : busNo }
        return jsonify(dataDic)
                    

@app.route('/')
def index():
	imgData = open('/home/pboord/Downloads/yelp/img/yelpHongKong4.jpg', 'rb').read().encode('base64').replace('\n', '')
	return render_template('index.html', imgData = imgData)

if __name__ == '__main__':
    app.run()
