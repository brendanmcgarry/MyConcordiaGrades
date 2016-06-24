import smtplib
import sys

fp = open("hold.txt")	# new grades
message = fp.read()

to = 'num@sms.rogers.com'	# input phone num in place of "num";
							# replace "sms.rogers.com" with your carrier's email-to-sms service
gmail_user = 'gmailaddr'	# gmail account must have "less secure apps" enabled in its settings:
							# https://support.google.com/accounts/answer/6010255?hl=en
gmail_pwd = 'gmailpass'
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:New grade(s) \n'
msg = header + '\n ' + message + ' \n\n'
smtpserver.sendmail(gmail_user, to, msg)
smtpserver.close()
