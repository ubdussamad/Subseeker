#!/usr/bin/env python
import apt
import os
from shutil import copyfile
cache = apt.Cache()

from subprocess import call

import time
if cache['nautilus-actions'].is_installed:
    pass
else:
    print("Nautilus Action Tool is not installed, You can install it by typing: \n sudo apt-get install nautilus-actions")
    if str(input("Would you like to?(y/n):")) == 'y':
        call(["apt-get", "install", "nautilus-actions"])
    else:
        print("Can't keep going!")
        exit()


def first_run():
	try:
		z = open('usr_config.ini')
		z.close()
		del z
		return 0
	except:
            print(''' Welcome to Subseeker 2v1\n For downloading subtitles through this utility
                      you should have a opensubtitle username and password , please create your account and sign in:''')
            username = str( input ("Enter username: ") )
            password = str( input ("Enter password: ") )
            print("\n User Created!")
            f = open('usr_config.ini','w')
            f.write('%s|%s'%(username,password))
            f.close()
first_run()

print("Now installing ......")
print("\n Copying Files......")

cwd = os.getcwd()
try:
    os.makedirs(os.path.expanduser('~')+'/.subseeker/')
except:
    print("Directory Already exists!")

#copyfile(cwd+'/subseeker.py', os.path.expanduser('~')+'/.subseeker/')

call(['cp',cwd+'/subseeker.py',os.path.expanduser('~')+'/.subseeker/'])
print("Copying Config Files...")
time.sleep(2)
call(['cp',cwd+'/usr_config.ini',os.path.expanduser('~')+'/.subseeker/'])
print("Copying Config Files:OK!")
time.sleep(2)
print("Files copied \n Installation completed , Opening readme....")





string = '''
 Subseeker 2v2  \n Installation complete , just one step from here and we're ready to go!

 \n * Open Nautilus Action Config Tool for the Search Bar.
 \n * Select "Tools" from the top toolbar of Nautilus Action Config Tool.
 \n * Select "Import assistant" from the Dropdown Menu.
 \n * A New window will open , Click "Next" in it. , A file selection window appears.
 \n * Navigate it to the main extracted folder (Where you extrated the Compressed Archive).
 \n * Select the config file (Named Like:config_67db8ea9"".schemas) and Comple the Import.
 \n * Click the save Icon (Just left of Red off button) and if anything prompts , click "Yes".
 \n * Restart the Computer.
 \n * Delete the extracted Archive to save disk space.
 \n * Delete the "subseeker" folder and the readme file you extracted to save disk space.
 \n\n     ** Test Installation. **
 \n * Navigate to a video file , In the third last row click "Nautilus Actions" and Then "Get Subs".
 \n * The Subtitle will be Automatically Downloaded in the same folder as Video.
 \n * Enjoy! '''

f = open(os.path.expanduser('~')+'/readme.txt','w')
f.write(string)
f.close()

call(["gedit",os.path.expanduser('~')+'/readme.txt'])




