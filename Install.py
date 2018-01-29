#!/usr/bin/env python
try:
    import apt,os,time
except:
    print("Please run this installer by python3.")
    raise ImportError("Use Python 3 for this script.")
from shutil import copyfile
from subprocess import call
cache = apt.Cache()

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
            print('''Welcome to Subseeker 2v1\nFor downloading subtitles through this utility you should have a \nopensubtitle username and password , please create your account and sign in:''')
            username = str( input ("\nEnter username: ") )
            password = str( input ("\nEnter password: ") )
            print('''\nChoose you default subtitle language code below:\nFor a detailed language code list, please visit: \nhttps://www.opensubtitles.org/addons/export_languages.php  (Use the three letter codes!) \nLeave it blank by pressing Enter for English.''')
            default_lang = str ( input( "Enter the language code for the default Subtitle language you want to choose:" ))
            if default_lang == '':
                default_lang = 'eng'
                print("\nDefault Language set to English.")
            print("\n User Created!")
            f = open('usr_config.ini','w')
            f.write('%s|%s|%s'%(username,password,default_lang))
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
 \n\n                        ** Test Installation. **
 \n * Navigate to a video file , In the third last row click "Nautilus Actions" and Then "Get Subs".
 \n * The Subtitle will be Automatically Downloaded in the same folder as Video.
 \n * Enjoy! '''

f = open(os.path.expanduser('~')+'/readme.txt','w')
f.write(string)
f.close()

call(["gedit",os.path.expanduser('~')+'/readme.txt'])
