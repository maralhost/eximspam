#!/usr/bin/python

import smtplib
import sys
import base64
import urllib2
import os 

server = sys.argv[1]
usr = sys.argv[2]
passw = sys.argv[3]
recv1 = sys.argv[4]
recv2 = sys.argv[5]
recv3 = sys.argv[6]

ip = urllib2.urlopen("http://ipecho.net/plain")
ip = ip.read()
hostname = spammers = os.popen("hostname").read();
yesterday_date=os.popen("date -d \'-1 day\' \'+%Y-%m-%d\'").read()

sender = usr
receivers = list()
receivers.append(recv1)
receivers.append(recv2)
receivers.append(recv3)

filename = "/tmp/spam_detail.txt"

# Read a file and encode it into base64 format
fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)  # base64


marker = "AUNIQUEMARKER"

body ="""
Server ip address => {0} \n
Server hostname => {1}
Server date => {2}
""".format(ip,hostname,yesterday_date)
# Define the main headers.
part1 = """From: Maralhost <spam@maralhost.com>
To: To Person <spam_analyzers@maralhost.com>
Subject: Sending Attachement
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)
message = part1 + part2 + part3


try :

	smtpObj = smtplib.SMTP(server)
	smtpObj.login(usr, passw)
	smtpObj.sendmail(sender, receivers, message)
	print "Successfully sent email"

except :

	print "Unable to send mail"
