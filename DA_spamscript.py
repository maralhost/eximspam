import os
import urllib2
from __builtin__ import file
import sys

email_1 = sys.argv[1]
#email_1 = sys.argv[2]
#email_1 = sys.argv[3]

log_path = r"/var/log/exim/mainlog"
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

# now its time to find spammers

possible_spammers_file_path = tmp_path+'_spammers'
cmd = "awk \'$3 ~ /^cwd/{print $3}\'  /tmp/_yesterday_mails | sort | uniq -c | sed \"s|^ *||g\"| sort -nr "

spammers = os.popen(cmd).readlines()
filtered_spammers = list()
for spammer in spammers:
    if(spammer.find("/home") != -1):
        num = spammer.strip().split(" ")[0]
        if int(num) > spam_detection_point:
            filtered_spammers.append(spammer.strip())



ip = urllib2.urlopen("http://ipecho.net/plain")
ip = ip.read()
hostname = spammers = os.popen("hostname").read();
mail_body = "Ip address => {0}\nHostname => {1}\nDate => {2}\nspammers : \n\n".format(ip,hostname.split(),yesterday_date.strip())

for spammer in filtered_spammers:
    mail_body += spammer + "\n"

file = open("/tmp/Spammers.txt",'w')
file.write(mail_body)
file.close()

send_mail1  = "mail -s \"Spammers ({0})\" {1} < ".format(ip,email_1)+ "/tmp/Spammers.txt"

os.system(send_mail1)
