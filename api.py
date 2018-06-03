# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import hashlib
import urllib
import base64
import random as rd


allocine_secret_key = '29d185d98c984a359e6e6f26a0474269'
allocine_partner = '100043982026'
formatUrl = 'json'

def init_connect():

	### Initialisation : ip et user-agent aleatoire
	## ip

	ip = str(rd.randint(0, 255)) + '.' + str(rd.randint(0, 255)) + '.' + str(rd.randint(0, 255)) + '.' + str(rd.randint(0, 255))

	## user-agent

	v = str(rd.randint(1, 4)) + '.' + str(rd.randint(0,9))
	a = str(rd.randint(0, 9))
	b = str(rd.randint(0, 99))
	c = str(rd.randint(0, 999))

	userAgents = [
		"Mozilla/5.0 (Linux; U; Android " + v + "; fr-fr; Nexus One Build/FRF91) AppleWebKit/5" + b + "." + c + " (KHTML, like Gecko) Version/" + a + "." + a + " Mobile Safari/5" + b + "." + c + "",
	    "Mozilla/5.0 (Linux; U; Android " + v + "; fr-fr; Dell Streak Build/Donut AppleWebKit/5" + b + "." + c + "+ (KHTML, like Gecko) Version/3." + a + ".2 Mobile Safari/ 5" + b + "." + c + ".1",
	    "Mozilla/5.0 (Linux; U; Android 4." + v + "; fr-fr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
	    "Mozilla/5.0 (Linux; U; Android 4." + v + "; fr-fr; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
	    "Mozilla/5.0 (Linux; U; Android " + v + "; en-gb) AppleWebKit/999+ (KHTML, like Gecko) Safari/9" + b + "." + a + "",
	    "Mozilla/5.0 (Linux; U; Android " + v + ".5; fr-fr; HTC_IncredibleS_S710e Build/GRJ" + b + ") AppleWebKit/5" + b + ".1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5" + b + ".1",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; HTC Vision Build/GRI" + b + ") AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	    "Mozilla/5.0 (Linux; U; Android " + v + ".4; fr-fr; HTC Desire Build/GRJ" + b + ") AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	    "Mozilla/5.0 (Linux; U; Android " + v + ".3; fr-fr; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; HTC Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5" + b + ".1",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; LG-LU3000 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5" + b + ".1",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; HTC_DesireS_S510e Build/GRI" + a + ") AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/" + c + ".1",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile",
	    "Mozilla/5.0 (Linux; U; Android " + v + ".3; fr-fr; HTC Desire Build/GRI" + a + ") AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	    "Mozilla/5.0 (Linux; U; Android 2." + v + "; fr-fr; HTC Desire Build/FRF" + a + ") AppleWebKit/533.1 (KHTML, like Gecko) Version/" + a + ".0 Mobile Safari/533.1",
	    "Mozilla/5.0 (Linux; U; Android " + v + "; fr-lu; HTC Legend Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/" + a + "." + a + " Mobile Safari/" + c + "." + a + "",
	    "Mozilla/5.0 (Linux; U; Android " + v + "; fr-fr; HTC_DesireHD_A9191 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
	    "Mozilla/5.0 (Linux; U; Android " + v + ".1; fr-fr; HTC_DesireZ_A7" + c + " Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/" + c + "." + a + "",
	    "Mozilla/5.0 (Linux; U; Android " + v + ".1; en-gb; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/" + c + ".1",
	    "Mozilla/5.0 (Linux; U; Android " + v + "; fr-fr; LG-P5" + b + " Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
	]

	headersUA = {'user-agent' : userAgents[rd.randint(0,len(userAgents)-1)]}

	return (ip, headersUA)

def getDate():
	dateComplete = datetime.now()
	year = dateComplete.year
	month = dateComplete.month
	day = dateComplete.day

	if month < 10:
		strMonth = '0' + str(month)
	else:
		strMonth = str(month)
	if day < 10:
		strDay = '0' + str(day)
	else:
		strDay = str(day)

	YMDstr = str(year) + strMonth + strDay

	return YMDstr

def cityDesc(city):

	"""
		code de retour : 
			100 : tout est normal
			200 : la requete n'a pas abouti
			300 : pas de cine dans la ville
			400 : la ville n'existe pas
	"""

	ip, headersUA = init_connect()
	YMDstr = getDate()

	searchField = city
	filterField = ''
	countField = '500'
	pageField = '1'

	url = 'q=' + searchField + '&filter=' + filterField + '&count=' + countField + '&page=' + pageField + '&format=json&partner=' + allocine_partner + '&sed=' + YMDstr

	toEncrypt = allocine_secret_key + url

	sig = urllib.quote_plus(base64.b64encode(hashlib.sha1(toEncrypt).digest()))

	urlComplete = 'http://api.allocine.fr/rest/v3/search?' + url + "&sig=" + sig
	
	req = requests.get(urlComplete, headers=headersUA)

	listeCine = []
	codePostal = 0

	codeRetour = 100

	if req.status_code == 200:

		if 'location' in req.json()['feed']:

			codePostal = req.json()['feed']['location'][0]['postalCode']

			if 'theater' in req.json()['feed']:
				for theaterCity in req.json()['feed']['theater']:
					listeCine.append(theaterCity)
			else:
				codeRetour = 300
		else:
			codeRetour = 400

	else:
		codeRetour = 200

	return codePostal, listeCine, codeRetour

def showtimeInTheater(codeTheater, jour):
	ip, headersUA = init_connect()
	YMDstr = getDate()

	searchField = codeTheater
	filterField = ''
	countField = '500'
	pageField = '1'

	url = 'theaters=' + searchField + '&date='+ jour + '&filter=' + filterField + '&count=' + countField + '&page=' + pageField + '&format=json&partner=' + allocine_partner + '&sed=' + YMDstr

	toEncrypt = allocine_secret_key + url

	sig = urllib.quote_plus(base64.b64encode(hashlib.sha1(toEncrypt).digest()))

	urlComplete = 'http://api.allocine.fr/rest/v3/showtimelist?' + url + "&sig=" + sig
	
	# print(urlComplete)

	req = requests.get(urlComplete, headers=headersUA)

	# print(req.json())

	return req.json()['feed']

def infoFilm(codeFilm):
	ip, headersUA = init_connect()
	YMDstr = getDate()

	searchField = str(codeFilm)
	filterField = ''
	countField = '500'
	pageField = '1'

	url = 'code=' + searchField + '&filter=' + filterField + '&count=' + countField + '&page=' + pageField + '&format=json&partner=' + allocine_partner + '&sed=' + YMDstr

	toEncrypt = allocine_secret_key + url

	sig = urllib.quote_plus(base64.b64encode(hashlib.sha1(toEncrypt).digest()))

	urlComplete = 'http://api.allocine.fr/rest/v3/movie?' + url + "&sig=" + sig

	req = requests.get(urlComplete, headers=headersUA)

	return req.json()

def getImg(url):
	urllib.urlretrieve(url, ".poster/poster.jpg")