# TODO: Replace manual input with GUI form

netname = None
password = None
sourceEmail = None
emailPass = None
toSendText = 0
toSendEmail = 0
toSendDesktopNotification = 0
cellNum = None
provider = None
destEmail = None

import sqlite3

conn = sqlite3.connect('ConcordiaGrades.db')

# Check if the settings table exists, if not then create it
cursor = conn.execute('''SELECT name 
						 FROM sqlite_master 
						 WHERE type='table' 
						 AND name='Settings';''')

existingSettings = not (len(cursor.fetchall()) == 0)

if not existingSettings:
	conn.execute('''CREATE TABLE Settings(
						Netname VARCHAR(7) PRIMARY KEY,
						Password VARCHAR(30) NOT NULL,
						SourceEmail VARCHAR(254) NOT NULL,
						EmailPass VARCHAR(50) NOT NULL,
						ToSendText INTEGER NOT NULL,
						ToSendEmail INTEGER NOT NULL,
						ToSendDesktopNotification INTEGER NOT NULL,
						CellNum VARCHAR(11),
						Provider VARCHAR(40),
						DestEmail VARCHAR(254)
					);''')
	print "MyConcordia netname: "
	netname = raw_input()
	print "MyConcordia password: "
	password = raw_input()
	print "Gmail username to send texts/emails from: "
	sourceEmail = raw_input()
	print "Gmail password: "
	emailPass = raw_input()
	
	print "This script can notify you of new grades by text message, email, and/or desktop notification."
	print "Please note: Choosing to receive texts by email-to-SMS Gateway might result in extra phone bill charges, depending on your carrier. Use at your own discretion."
	
	print "Do you want to receive text message notifications? (y/n): "
	toSendText = raw_input()
	while True:
		if toSendText == 'y':
			toSendText = 1
			break
		elif toSendText == 'n':
			toSendText = 0
			break
		else:
			print "Invalid input. Do you want to receive text message notifications? (y/n): "
			toSendText = raw_input()

	print "Do you want to receive email notifications? (y/n): "
	toSendEmail = raw_input()
	while True:
		if toSendEmail == 'y':
			toSendEmail = 1
			break
		elif toSendEmail == 'n':
			toSendEmail = 0
			break
		else:
			print "Invalid input. Do you want to receive email notifications? (y/n): "
			toSendEmail = raw_input()

	print "Do you want to receive desktop notifications? (y/n): "
	toSendDesktopNotification = raw_input()
	while True:
		if toSendDesktopNotification == 'y':
			toSendDesktopNotification = 1
			break
		elif toSendDesktopNotification == 'n':
			toSendDesktopNotification = 0
			break
		else:
			print "Invalid input. Do you want to receive desktop notifications? (y/n): "
			toSendDesktopNotification = raw_input()
	
	if toSendText:
		print "Input cell number to receive text messages at: "
		cellNum = raw_input()
		print "Input cell provider (Select a provider from smsGateways.txt; if yours is not there, add it to file): "
		provider = raw_input()
	
	if toSendEmail:
		print "Input email to receive notifications at: "
		destEmail = raw_input()

	conn.execute("INSERT INTO `Settings` " +
	"(`Netname`, `Password`, `SourceEmail`, `EmailPass`, `ToSendText`, `ToSendEmail`, `ToSendDesktopNotification`, `CellNum`, `Provider`, `DestEmail`)" +
	" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
	(netname, password, sourceEmail, emailPass, toSendText, toSendEmail, toSendDesktopNotification, cellNum, provider, destEmail))
	conn.commit()
else:
	print "Settings already exist. To input new settings, please delete ConcordiaGrades.db"
	# TODO: Replace with "Value is [val]; Replace?" (unless password; then do not display)
	# cursor = conn.execute('''SELECT * FROM `Settings`;''')

conn.close()