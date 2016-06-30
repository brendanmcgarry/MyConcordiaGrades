def errorLogging(error):
	print "The error: "+str(type(error))+" has occurred"

# Initialize all of these variables to your information
yourUsername  = "user"
yourPassword  = "pass"
yourEmail     = "email"
yourEmailPass = "emailPass"
yourNumber    = "num"
yourProvider  = "provider"	# Select your provider from smsGateways.txt
							# If your carrier is not there, please add them and their gateway to smsGateways.txt in the proper format

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver     = webdriver.PhantomJS()
wait       = WebDriverWait(driver, 10)
exceptions = False
grades     = {}

# Connect to the "View My Grades" page
driver.get("https://campus.concordia.ca/psp/pscsprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?")

try:
	# Set the username and password
	username = wait.until(EC.presence_of_element_located((By.ID, "userid")))
	password = wait.until(EC.presence_of_element_located((By.ID, "pwd")))

	username.clear()
	password.clear()

	username.send_keys(yourUsername)
	password.send_keys(yourPassword)

	# Hit login
	driver.find_element_by_class_name("form_button_submit").click()
	
	# Wait until the iframe is loaded (it waits a max of 10 seconds at the moment)
	iFrameSrc = wait.until(EC.presence_of_element_located((By.ID, "ptifrmtgtframe")))

	# Go to the iframe page
	driver.get(iFrameSrc.get_attribute("src"))

	# Click the summer radio button
	radioBtn = wait.until(EC.presence_of_element_located((By.ID, "SSR_DUMMY_RECV1$sels$2$$0")))
	radioBtn.click()

	driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()

	try:
		# Wait until the 'change term' button loads
		wait.until(EC.presence_of_element_located((By.ID, "DERIVED_SSS_SCT_SSS_TERM_LINK")))

		# Loop keeps going until it can't find anymore grades
		i = 0
		while True:
			grade  = driver.find_element_by_id("win0divSTDNT_ENRL_SSV1_GRADE_POINTS$"+str(i))
			grade  = grade.find_elements_by_css_selector("*")[0].get_attribute("innerHTML")
			gClass = driver.find_element_by_id("CLS_LINK$"+str(i)).get_attribute("innerHTML")

			# Store the grade
			if grade != "&nbsp;":
				grades[gClass] = grade

			i += 1
	except Exception as e:
		if "TimeException" in str(type(e)):
			errorLogging(e)
			exceptions = True
except Exception as e:
	errorLogging(e)
	exceptions = True
finally:
	driver.quit()

	if exceptions:
		sys.exit()

# Check if the grade already exists in the database
import sqlite3

conn = sqlite3.connect('ConcordiaGrades.db')

# Check if the grades table exists, if not then create it
cursor = conn.execute('''SELECT name 
						 FROM sqlite_master 
						 WHERE type='table' 
						 AND name='Grades';''')

if len(cursor.fetchall()) == 0:
	conn.execute('''CREATE TABLE Grades(
						ID INTEGER PRIMARY KEY,
						Class VARCHAR(30) NOT NULL,
						Grade VARECHAR(4) NOT NULL
					);''')

cursor = conn.execute('''SELECT `Class`, `Grade`
						 FROM `Grades`;''')

newGrades = grades

# Make sure we haven't already sent the grades already
for row in cursor:
	if row[0] in newGrades:
		del newGrades[row[0]]

# Get carrier sms gateway
smsGateway = ""
fp = open("smsGateways.txt")	# file with carriers and sms gateways, comma separated
lines = fp.read().split("\n")
fp.close()

for line in lines:
	aCarrier = line.split(",")[0]
	aGateway = line.split(",")[1]
	if yourProvider in aCarrier:
		smsGateway = aGateway

if len(newGrades) > 0:
	# Send the new grades to the valid SMS email
	import smtplib

	message = "\n"
	for grade in newGrades:
		message += grade + ": " + newGrades[grade] + "\n"

	to = yourNumber+smsGateway
	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(yourEmail, yourEmailPass)
	header = 'To:' + to + '\n' + 'From: ' + yourEmail + '\n' + 'Subject:New grade(s) \n'
	msg = header + '\n ' + message + ' \n\n'
	smtpserver.sendmail(yourEmail, to, msg)
	smtpserver.close()

	# Add the new grades to the DB
	for grade in newGrades:
		conn.execute("INSERT INTO `Grades` (`Class`, `Grade`) VALUES (\'"+grade+"\', \'"+newGrades[grade]+"\');")
	conn.commit()

	# REMOVE IN PRODUCTION
	print "Grades successfully sent via SMS"
else:
	# REMOVE IN PRODUCTION
	print "No new grades to push"

conn.close()
