MyConcordiaGrades
=================

This guide assumes the use of Python 2.7; it has not been tested with other versions yet. We also assume you are using gmail, and we do not support other email providers yet but this might change in future updates.

Right now MyConcordiaGrades is a simple selenium based web crawler that checks for new grades in the summer 2016 semester.
In the future it will be updated to handle every semester and will be automated, but for now it will mostly be targeting 
tech savvy individuals. This small guide assumes you have python and PhantomJS installed and you are able to use the pip command in your terminal, if not then go to this link: [Installing Pip](https://pip.pypa.io/en/stable/installing/)

#### IMPORTANT NOTE: 

We are not responsible if someone takes your computer and looks at this file. Right now nothing is compiled or hashed 
so your password is stored in plain text. This will be changed in the future, so if you are worried then wait for the 
update.

Also, using the email-to-SMS service that many cell phone carriers provide can result in extra costs on your phone bill; use at your own discretion.

Setting up the files
====================

The first thing you want to do is download "pushNewGrades.py", after doing so you must change the following variables inside 
the script:

* yourUsername => MyConcordia username
* yourPassword => MyConcordia password
* yourEmail    => Your email; must have "Allow less secured apps" enabled. I recommend creating a dummy email.

You can do so here: [link](https://www.google.com/settings/security/lesssecureapps)

* yourEmailPass => Your email's password
* yourNumber    => Your phone number
* yourProvider  => The suffix needed to send an SMS via email for your specific provider. For rogers it's: "sms.rogers.com"

Dependencies
============
Python 2.7

PhantomJS (tested with v. 1.9.8 & v. 2.1.1)

MyConcordiaGrades needs the following modules for Python:

* selenium
* sqlite3
* smtplib

Luckily for us sqlite3 and smtplib are usually pre-packaged with Python.

To install selenium simply run the following command in the terminal:

```
  pip install selenium
```

Setting up a cron job on a Mac
==============================

__*Step 1*__

This step is pretty straight forward. Run the following command in your terminal:

```
  env EDITOR=vi crontab -e
```

You have the choice of replacing "vi" with your preferred editor.

__*Step 1.5*__

You may have to run, "sudo env EDITOR=vi crontab -e" instead depending on your permissions. I personally ran into an error 
where it couldn't detect phantomJS in the PATH even though it was clearly there. You can use the method below to figure out if you are receiving this error.

__*Step 2*__

Finally add the following line inside the editor:

```
  */10 * * * * cd /Path/To/Directory/With/Script && python2.7 pushNewGrades.py
```

This cronjob is tasked to run every 10 minutes. Make sure to change the directory path on the cd command to the proper 
directory  that is currently holding the pushNewGrades.py script. On my mac I have it in "/Users/name/CronTasks". For 
more information on cron jobs go here: [Cron Jobs](http://www.adminschoice.com/crontab-quick-reference)

__*Step 2.5*__

If you want to redirect potential errors from the pushNewGrades.py scripts then add the following to your crontab instead:

```
  */10 * * * * cd /Path/To/Directory/With/Script && python2.7 pushNewGrades.py >> /Path/To/Directory/With/Log.log &2>1
```

__*Step 3*__

After saving the file run this in your terminal:

```
  crontab -l
```

and it should display the cron job that you added previously (NOTE: If you ran crontab with sudo previously you must also run this command with sudo).

Setting up a Scheduled Task on a PC
===========================================
Open the Windows Task Scheduler

Click "Create Task" in the right sidebar

In the General tab:

* Give the task a descriptive/unique name in "Name:"
* Check "Run with highest privileges" and "Run whether user is logged on or not"
* Under "Configure for", select your OS (or the closest option)

In the Triggers tab:

* Click "New..."
* Check "Daily"
* Start: Current date at "12:00:00 AM"
* "Recur every": 1 days
* Check "Repeat task every:" and input "5 minutes" (or however often you want it to run)

In the Actions tab:

* Click "New..."
* "Start in (optional):" the folder location where pushNewGrades.py is
* "Program/script:" pushNewGrades.py

Regardless of the time of day, the task should begin to run at every time increment after 12:00:00 AM.
For example, if the task is configured to run every 5 minutes and you create this task at 3:41 PM, its Next Run Time should immediately be 3:45 PM.
