def getImgData(x,y,phoneColor,clickType,busNo):
	import urllib, os
	import requests
	import io
	import simplejson as json
	from yelp.client import Client
	from yelp.oauth1_authenticator import Oauth1Authenticator
	from PIL import Image
	import pyocr
	import pyocr.builders
	import sys
	import os
	import numpy as np
	import numpy.matlib
	import cv2
        def overlap(b1, b2):
            return (b1[0] <= b2[0]+b2[2]) and (b1[0]+b1[2] >= b2[0]) and (b1[1] <= b2[1]+b2[3]) and (b1[1]+b1[3] >= b2[1])
        def bigrect(b1, b2):
            b0 = b1
            b0[0]=min(b1[0],b2[0])
            b0[1]=min(b1[1],b2[1])
            b0[2]=max(b1[0]+b1[2],b2[0]+b2[2]) - b0[0]
            b0[3]=max(b1[1]+b1[3],b2[1]+b2[3]) - b0[1]
            return b0
        def lbwh2lbrt(b):
            b0=b
            b0[0]=b[0]
            b0[1]=b[1]
            b0[2]=b[0]+b[2]
            b0[3]=b[1]+b[3]
            return b0
	# read API keys
	APP_ROOT = os.path.dirname(os.path.abspath('__init.py__'))   # refers to application_top
	APP_STATIC = os.path.join(APP_ROOT, 'app', 'static')
	with io.open(os.path.join(APP_STATIC,'yelp_secret.json')) as cred:
		creds = json.load(cred)
		auth = Oauth1Authenticator(**creds)
		client = Client(auth)	
	urlList = ['http://i.imgur.com/wIj4B4Xg.jpg']
	if clickType == 'screenClick':
		img = cv2.imread(os.path.join(APP_STATIC,'yelpHongKong4.jpg'))
		vis = img.copy()
		channels = cv2.text.computeNMChannels(img)
		cn = len(channels)-1
		for c in range(0,cn):
  			channels.append((255-channels[c]))
		b = []
		for channel in channels:
	  		erc1 = cv2.text.loadClassifierNM1(os.path.join(APP_STATIC,'trained_classifierNM1.xml'))
  			er1 = cv2.text.createERFilterNM1(erc1,16,0.00015,0.13,0.2,True,0.1)
  			erc2 = cv2.text.loadClassifierNM2(os.path.join(APP_STATIC,'trained_classifierNM2.xml'))
	  		er2 = cv2.text.createERFilterNM2(erc2,0.5)
  			regions = cv2.text.detectRegions(channel,er1,er2)
  			rects = cv2.text.erGrouping(img,channel,[r.tolist() for r in regions])
	  		for r in range(0,np.shape(rects)[0]):
  				b.append(rects[r])
		# consolidate overlapping rectangles
	        c = b
        	h=0
	        while h < len(c):
        	    g=len(c) - 1
	            while g > h:
        	        if overlap(c[g],c[h]):
                	    c[g] = bigrect(c[g],c[h])
	                    c = np.delete(c,h,axis=0)
        		g -= 1
            	    h += 1
        	h=0
        	while h < len(c):
            		g=len(c) - 1
            		while g > h:
                		if overlap(c[g],c[h]):
                    			c[g] = bigrect(c[g],c[h])
                    			c = np.delete(c,h,axis=0)
                		g -= 1
            		h += 1
		# center of mass (cm)
		rectCM = np.zeros((c.shape[0],2), dtype=int)
		rectCM[:,0] = c[:,0] + c[:,2]/2
		rectCM[:,1] = c[:,1] + c[:,3]/2
		cmDiff = rectCM - np.matlib.repmat(np.array([x,y]),rectCM.shape[0],1)
		closestRect = np.argmin(np.hypot(cmDiff[:,0],cmDiff[:,1]))
		rect = c[closestRect,:]
		imgData = urlList[busNo]
		imSeg = img[ rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2] ]
		tools = pyocr.get_available_tools()
		tool = tools[0]
		langs = tool.get_available_languages()
		lang = langs[0]
		
		boxText = tool.image_to_string(
	    	Image.fromarray(imSeg),
		lang="eng",
		builder=pyocr.builders.TextBuilder()
		)
		# use first line if more than one
		boxText=boxText.partition("\n")[0]
		searchCity = 'Fuk Wing Street, Hong Kong'
		params = {
    			'term': boxText,
			'limit': 1
		}
		# yResp = result from Yelp search
		yResp = client.search(searchCity, **params)
		yelpUrl = ''
		if len(yResp.businesses)!=0:
			yelpUrl =  yResp.businesses[0].url
	dataDic = {'yelpUrl': yelpUrl, 'imgData': imgData, 'boxText': boxText, 'clientx' : x, 'clienty' : y, 'busNo' : busNo }
	return dataDic
