def errorLogging(error):
	print "The error: "+str(type(error))+" has occurred"

# Initialize all of these variables to your information
yourUsername  = "user"
yourPassword  = "pass"
yourEmail     = "email"
yourEmailPass = "emailPassword"
yourNumber    = "num"
yourProvider  = "provider" # Sms email suffix of your provider

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS()
wait   = WebDriverWait(driver, 10)

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
			grade = driver.find_element_by_id("win0divSTDNT_ENRL_SSV1_GRADE_POINTS$"+str(i))
			children = grade.find_elements_by_css_selector("*")

			# Print the class name + grade
			print driver.find_element_by_id("CLS_LINK$"+str(i)).get_attribute("innerHTML")+": "+ \
				  children[0].get_attribute("innerHTML")
			i += 1
	except Exception as e:
		# Ignore the exception
		pass
except Exception as e:
	errorLogging(e)
	sys.exit()

driver.quit()