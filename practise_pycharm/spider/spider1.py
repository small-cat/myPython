import urllib2
response = urllib2.urlopen("http://producingoss.com/zh/")
print response.read()