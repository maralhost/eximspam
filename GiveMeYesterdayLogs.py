import os
import urllib2
from __builtin__ import file

log_path = r"/var/log/exim_mainlog"
tmp_path = r"/tmp/"
spam_detection_point = 50

yesterday_date=os.popen("date -d \'-1 day\' \'+%Y-%m-%d\'").read()
today_date=os.popen("date \'+%Y-%m-%d\'").read()

yesterday_emails = list()

#gather emails of yesterday

file = open(log_path,'r')
for line in file.readlines():
    date = line.split(" ")[0].strip()

    if(date == yesterday_date.strip()):
        yesterday_emails.append(line)

    if(date == today_date.strip()):
        break

file.close()

# write yesterday emails to a file

yesterday_emails_path = tmp_path+'_yesterday_mails'
file = open(yesterday_emails_path,'w')
for line in yesterday_emails:
    file.write(line+"\n")

file.close()
