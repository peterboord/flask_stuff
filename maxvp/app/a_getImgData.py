def getImgData(x,y,busNo):
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
	APP_ROOT = os.path.dirname(os.path.abspath('__init.py__'))   # refers to application_top
	APP_STATIC = os.path.join(APP_ROOT, 'app', 'static')

	# ref rectifyImage.ipynb
	img = cv2.imread(os.path.join(APP_STATIC,'yelpHongKong4.jpg'))
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	H, W = img.shape[:2]



	# ref procImage.ipynb
        def overlap(b1, b2):
            return (b1[0] <= b2[0]+b2[2]) and (b1[0]+b1[2] >= b2[0]) and (b1[1] <= b2[1]+b2[3]) and (b1[1]+b1[3] >= b2[1])
        # return rect encompassing both boxes
        def bigrect(b1, b2):
            b0 = b1
            b0[0]=min(b1[0],b2[0])
            b0[1]=min(b1[1],b2[1])
            b0[2]=max(b1[0]+b1[2],b2[0]+b2[2]) - b0[0]
            b0[3]=max(b1[1]+b1[3],b2[1]+b2[3]) - b0[1]
            return b0
        # convert rect(left,btm,width,height) to rect(left,btm,right,top)
        def lbwh2lbrt(b):
            b0=b
            b0[0]=b[0]
            b0[1]=b[1]
            b0[2]=b[0]+b[2]
            b0[3]=b[1]+b[3]
            return b0
	urlList = ['http://i.imgur.com/wIj4B4Xg.jpg']
	img = cv2.imread(os.path.join(APP_STATIC,'warped.jpg'))
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
	rectCM[:,0] = c[:,0] + np.true_divide(c[:,2],2)
	rectCM[:,1] = c[:,1] + np.true_divide(c[:,3],2)
	cmDiff = rectCM - np.matlib.repmat(np.array([x,y]),rectCM.shape[0],1)
	closestRect = np.argmin(np.hypot(cmDiff[:,0],cmDiff[:,1]))
	rect = c[closestRect,:]
	imgUrl = urlList[busNo]
	imSeg = img[ rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2] ]
	cv2.imwrite(os.path.join(APP_STATIC,'textbox.jpg'),imSeg)
	
	from PIL import Image
	import pyocr
	import pyocr.builders
	tools = pyocr.get_available_tools()
	tool = tools[0]
	langs = tool.get_available_languages()
	lang = langs[0]
		
		#Image.fromarray(imSeg),
	boxText = tool.image_to_string(
		Image.open(os.path.join(APP_STATIC,'textbox.jpg')),
		lang="chi_sim",
		builder=pyocr.builders.TextBuilder()
	)
	# use first line if more than one
	boxText=boxText.partition("\n")[0]
	print 'boxText is ' + boxText
	

	# pbYelp.ipynb
	# read API keys
	with io.open(os.path.join(APP_STATIC,'yelp_secret.json')) as cred:
    		creds = json.load(cred)
    		auth = Oauth1Authenticator(**creds)
    		client = Client(auth)
	with io.open(os.path.join(APP_STATIC,'google_secret.json')) as cred:
    		google_secret = json.load(cred)
	from geopy.distance import vincenty
	hk1 = 22.329038,114.166347
	hk2 = hk1[0]+0.004,hk1[1]+0.004
	geoDist = vincenty(hk1, hk2).meters
	str(geoDist*2)
	import sys
	import urllib2
	reload(sys)  
	sys.setdefaultencoding('utf8')
	sys.getdefaultencoding()
	# construct Google Places url
	hk1 = 22.329038,114.166347
	hk2 = hk1[0]+0.004,hk1[1]+0.004
	geoDist = vincenty(hk1, hk2).meters
	str(geoDist*2)
	googleUrl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
	googleUrl += 'location=' + str(hk2[0]) + ',' + str(hk2[1]) + '&'
	googleUrl += 'radius=' + str(geoDist*2) + '&type=restaurant&'
	googleUrl += 'query=' + boxText.replace(' ','') + '&'
	googleUrl += 'key=' + google_secret['key']
	response = urllib2.urlopen(googleUrl)
	string = response.read().decode('utf-8')
	googleJson = json.loads(string)
	vicinity = googleJson['results'][0]['vicinity'] + ',' + 'Hong Kong, HK'
	params = {
    		'location': vicinity
	}
	# yResp = result from Yelp search
	yResp = client.search( **params)
	# call url
	yelpUrl = ''
	if len(yResp.businesses)!=0:
		yelpUrl =  yResp.businesses[0].url
	
	boxText = 'boxText = ' + boxText + ', vicinity = ' + vicinity

	dataDic = {'yelpUrl': yelpUrl, 'imgUrl': imgUrl, 'boxText': boxText, 'clientx' : x, 'clienty' : y, 'busNo' : busNo }
	return dataDic
