def errorLogging(error):
	print "The error: "+str(type(error))+" has occurred"

myGmail = "myGmail"
myPass = "myPass"

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS()	# use Firefox() to be able to access "less secure apps" page properly
								# TODO: Use headless Firefox (no disturbance for user; can access page(?) )
wait = WebDriverWait(driver, 10)
exceptions = False

# Connect to the gmail sign in page
driver.get("https://www.gmail.com")

try:
	# Set the username and click Next
	username = wait.until(EC.presence_of_element_located((By.ID, "Email")))
	next = wait.until(EC.presence_of_element_located((By.ID, "next")))

	username.clear()
	username.send_keys(myGmail)
	next.submit()
	
	# Once page loads, input password and log in
	wait.until(EC.staleness_of(username))
	password = wait.until(EC.presence_of_element_located((By.ID, "Passwd")))

	password.clear()
	password.send_keys(myPass)
	signIn = driver.find_element_by_id("signIn")
	signIn.click()
	
	# Wait for login to complete
	wait.until(EC.staleness_of(signIn))
	
	# Load page for enabling "less secure apps" to allow gmail SMTP usage for this account
	driver.get("https://www.google.com/settings/security/lesssecureapps")
	
	# Output entire html of page for testing purposes
	# print(driver.page_source.encode('utf-8'))
	
except Exception as e:
	errorLogging(e)
	exceptions = True
finally:
	driver.quit()

	if exceptions:
		sys.exit()