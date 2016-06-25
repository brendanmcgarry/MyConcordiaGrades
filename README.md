MyConcordiaGrades
=================

This guide assumes the use of Python 2.7, it has not been tested with other versions yet.

Right now MyConcordiaGrades is a simple selenium based web crawler that checks for new grades in the summer 2016 semester.
In the future it will be updated to handle every semester and will be automated, but for now it will mostly be targetting 
tech savvy individuals. This small guide assumes you have python installed and you are able to use the pip command in your terminal, if not then go to this link: [Installing Pip](https://pip.pypa.io/en/stable/installing/)

#### IMPORTANT NOTE: 

We are not responsible if someone takes your computer and looks at this file. Right now nothing is compiled or hashed 
so your password is stored in plain text. This will be changed in the future, so if you are worried then wait for the 
update.

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

Dependencies on Mac
===================

MyConcordiaGrades needs the following modules for python:

* selenium
* sqlite3
* smtplib

Luckily for us sqlite3 and smtplib are usually pre-packaged with python.

To install selenium simply run the following command in the terminal:

```
  pip install selenium
```

Setting up a cron job on a Mac
==============================

This step is pretty straight forward. Run the following command in your terminal:

```
  env EDITOR=vi crontab -e
```

You have the choice of replacing "vi" with your preferred editor.

Finally add the following line inside the editor:

```
  */10 * * * * cd /Path/To/Directory/With/Script && python2.7 pushNewGrades.py
```

This cronjob is tasked to run every 10 minutes. Make sure to change the directory path on the cd command to the proper 
directory  that is currently holding the pushNewGrades.py script. On my mac I have it in "/Users/name/CronTasks". For 
more information on cron jobs go here: [Cron Jobs](http://www.adminschoice.com/crontab-quick-reference)

After saving the file run this in your terminal:

```
  crontab -l
```

and it should list "*/10 * * * * cd /Path/To/Directory/With/Script && python2.7 pushNewGrades.py", if not then you 
did something incorrectly.

