#--------------------------------------------------
#--------------------------------------------------
# Name:   GeeksForGeeks Article Extractor
# Purpose: To download and save articles filed under each and every tag mentioned in www.geeksforgeeks.org 
# developed by Aryak Sengupta(@aryak93) and modified by Prabhanshu Attri (@nirmankarta)
#--------------------------------------------------
#--------------------------------------------------

from bs4 import BeautifulSoup
import urllib2
import os.path
import string

#nonTags = ['c', 'c-plus-plus', 'java','data-structures', 'fundamentals-of-algorithms']

nonTags = ['java']#,'data-structures', 'fundamentals-of-algorithms']

AllTags = []#['interview-experience','advance-data-structures','dynamic-programming','Greedy-Algorithm','backtracking','pattern-searching','divide-and-conquer','graph','MathematicalAlgo','recursion', 'amazon']


path = ""      # Specify your path here
#path = "E:\GeeksForGeeks\\" 	#Sample windows path
#path = "/home/nirmankarta/" 	#Sample windows path

def Main():	
	print '\n\nGeeksforGeeks Website extracter'
	print '-------------------------------------------------------------------------------------'
	print 'developed by Aryak Sengupta(@aryak93) and further modified by Prabhanshu Attri (@nirmankarta)'
	print '-------------------------------------------------------------------------------------'
	print 'Parsing Website...'
	ExtractMainLinks(AllTags,path)

def ExtractMainLinks(AllTags,path):
	n = 0
	for i in nonTags:		
		url = "http://www.geeksforgeeks.org/" + i +"/"
		print '\nRetrieving {0} of {1}: {2}'.format(n+1,len(nonTags),i)
		try:		
			data = urllib2.urlopen(url).read()
		except urllib2.HTTPError, err:
		   if err.code == 404:
		       print "404: Page not found! | {0}".format(url)
		   elif err.code == 403:
		       print "403: Access denied! | {0}".format(url)
		   else:
		       print "Something happened! Error code: {0} | {1}".format(err.code,url)
		except urllib2.URLError, err:
		    print "Some other error happened: {0} | {1}".format(err.reason,url)
		soup = BeautifulSoup(data)
		allLinks = soup.findAll("div",attrs={'class':'page-content'})
		listofLinks = []
		for link in allLinks:
			for num in range(0,len(link.findAll("a"))-1):
				mainLink = str(link.findAll("a")[num]).split("<a href=")[1].split('rel="bookmark"')[0].strip('"').split('"')[0]
				listofLinks.append(mainLink)
		Extract_And_Save_Page_Data('http://geeksquiz.com/', listofLinks,path,i)
		n = n + 1
	n=0

	for i in AllTags:		
		url = "http://www.geeksforgeeks.org/tag/" + i +"/"
		print '\nRetrieving tag {0} of {1}: {2} | Page 1'.format(n+1,len(AllTags),i)
		try:		
			data = urllib2.urlopen(url).read()
		except urllib2.HTTPError, err:
		   if err.code == 404:
		       print "404: Page not found! | {0}".format(url)
		   elif err.code == 403:
		       print "403: Access denied! | {0}".format(url)
		   else:
		       print "Something happened! Error code: {0} | {1}".format(err.code,url)
		except urllib2.URLError, err:
		    print "Some other error happened: {0} | {1}".format(err.reason,url)
		soup = BeautifulSoup(data)
		
		lastPage = soup.findAll("a",class_="last")
		if len(lastPage) != 0:
			lastPage = lastPage[0]['href']
			lastPage = lastPage.split('/')
			end = lastPage[len(lastPage)-2]
		else:
			lastPage = soup.findAll("a",class_="page larger")
			if len(lastPage) != 0:
				lastPage = lastPage[len(lastPage)-1]['href']
				lastPage = lastPage.split('/')
				end = lastPage[len(lastPage)-2]
			else:
				end = 0
		num = 2
		#print end
		while True:
			allLinks = soup.findAll("h2",class_="post-title")
			listofLinks = []
			for link in allLinks:
				mainLink = str(link.findAll("a")[0]).split("<a href=")[1].split('rel="bookmark"')[0].strip('"').split('"')[0]
				listofLinks.append(mainLink)
			Extract_And_Save_Page_Data(url,listofLinks,path,i)
			if (int(num) > int(end)):
				break
			url = "http://www.geeksforgeeks.org/tag/" + i +"/page/" + str(num) + "/"
			print '\nRetrieving tag {0} of {1}: {2} | Page {3} of {4}'.format(n+1,len(AllTags),i, num, end)		
			try:		
				data = urllib2.urlopen(url).read()
			except urllib2.HTTPError, err:
			   if err.code == 404:
			       print "404: Page not found! | {0}".format(url)
			   elif err.code == 403:
			       print "403: Access denied! | {0}".format(url)
			   else:
			       print "Something happened! Error code: {0} | {1}".format(err.code,url)
			except urllib2.URLError, err:
			    print "Some other error happened: {0} | {1}".format(err.reason,url)
			soup = BeautifulSoup(data)
			num = num + 1
		n = n + 1

def Extract_And_Save_Page_Data(url,listofLinks,path,i):
	No = 0
	listofTitles = []
	if not os.path.exists(path+i):
		os.mkdir(path+i)
	for item in listofLinks:
		pageName = item[:-1]
		pageName = pageName.split('/')
		pageName = pageName[len(pageName)-1]
		'''if 'http://www.geeksforgeeks.org/' not in item:
			pageName = item.replace("http://geeksquiz.com/", "");
		else:
			pageName = item.replace("http://www.geeksforgeeks.org/", "");'''
		pageName = pageName+".html"
		filePath = path + i[0:] +"/" +pageName
		No = No +1
		
		if os.path.isfile(filePath):
			print '\t{0} of {1}: {2} exists!'.format(No, len(listofLinks), pageName)
		else:
			pageData = ""
			try:		
				pageData = urllib2.urlopen(item).read()
				soup_d = BeautifulSoup(pageData)
				title1 = str(soup_d.title)
				title1 = title1[7:-10]
				#title1 = title1.replace("GeeksforGeeks</title>","");
				#title1 = string.replace("<title>","");
				print title1
				listofTitles.append(title1)
				with open(filePath,"wb") as f:
					f.write(str(pageData))		
				print '\t{0} of {1}: {2} is saved!'.format(No, len(listofLinks), pageName)
			except urllib2.HTTPError, err:
			   if err.code == 404:
			       print "404: Page not found! | {0}".format(item)
			   elif err.code == 403:
			       print "403: Access denied! | {0}".format(item)
			   else:
			       print "Something happened! Error code: {0} | {1}".format(err.code,item)
			except urllib2.URLError, err:
			    print "Some other error happened: {0} | {1}".format(err.reason,item)
	indexData = '<html><a href="l.html">link</a></html>'
	with open(path + i[0:] + "/index.html","wb") as f:
		f.write(str(indexData))	
	print listofTitles
			

Main()