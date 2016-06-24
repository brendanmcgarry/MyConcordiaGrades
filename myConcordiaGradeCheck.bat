@echo off
set newgrade=0
set checkedgrade=1

REM empties txt files to store data in, in case they contains text
echo. 2>hold.txt
echo. 2>newcheckedgrades.txt

REM for each grade in table on MyConcordia, delimt'd so %%a is course code, %%b is grade
for /f "tokens=1,2 delims=:" %%a in ('phantomjs MyConcordiaGrades.js username pass') do (
	REM for each grade from most recent grades check
	for /f "tokens=1,2 delims=:" %%i in ('type checkedgrades.txt') do (
		REM each grade with changes to it is appended to hold.txt
		IF %%a==%%i (
			IF NOT %%b==%%j (
				echo|set /p=%%a:%%b >> hold.txt
			)
		)
	)
	echo %%a:%%b>> newcheckedgrades.txt
)

REM if grades have changed, i.e. if hold.txt is not-empty
for /f %%i in ("hold.txt") do set size=%%~zi
if %size% gtr 0 (
	REM send text message with new grades; py script uses hold.txt for message
	py emailForNewGrades.py
)

REM replace old archived grades with most recent grades
mv newcheckedgrades.txt checkedgrades.txt
rm hold.txt