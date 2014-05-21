#/usr/bin/env python
## -*- coding: gbk -*-

"this file is used for retrieve pdf documents from a certain web page"

import urllib
import urllib2
from HTMLParser import HTMLParser
import re
import os

def Action(url,ext='pdf',output='.'):

	lpdf = []
	urlpdf = []
	namepdf = []

	#domain
	index = url.rfind('/')
	domain = url[0:index+1];

	print domain

	request = urllib2.Request(url);
	response = urllib2.urlopen(request);

	#content
	content = response.read()

	#resource
	mode = '<a[^>]+>[^<]+.pdf[^>]+a>'
	lpdf = re.compile(mode).findall(content)
	parserurl = HTMLParser()
	parsername = HTMLParser()
	print lpdf
	for x in lpdf:
		sta = x.find("href=\"")+6
		end = x.find("\"",sta+1)
		urlpdf.append(x[sta:end])
		sta = x.find(">")+1;
		end = x.find("pdf",sta);
		namepdf.append(x[sta:end+3])
	#print len(namepdf),len(urlpdf)
	for i in range(len(urlpdf)):
		tmp = []
		parserurl.handle_data = tmp.append
		parserurl.feed(urlpdf[i])
		urlpdf[i] = '&'.join(tmp);
	parserurl.close()
	for i in range(len(namepdf)):
		tmp = []
		parsername.handle_data = tmp.append
		parsername.feed(namepdf[i])
		namepdf[i] = '&'.join(tmp);
	for i in range(len(urlpdf)):
		print urlpdf[i]
		print namepdf[i]
		urllib.urlretrieve(urlpdf[i],output + unicode(namepdf[i],"utf8"))


if __name__ == '__main__':
	print 'please enter a url :'
	url = raw_input()
	Action(url=url,output='E:\\')		




	
