#!/usr/bin/env python
try:
    import tkinter as tk
except:
    import Tkinter as tk

import os,sys,apt,time
from subprocess import call
if apt.Cache()['nautilus-actions'].is_installed:
    pass
else:
    print("Nautilus Action Tool is not installed, You can install it by typing: \n sudo apt-get install nautilus-actions")
    if str(input("Would you like to?(y/n):")) == 'y':
        call(["apt-get", "install", "nautilus-actions"])
    else:
        print("Can't keep going!")
        exit()


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('Subseeker Installer')
        self.header()
        self.input_fields()
        self.language_selection()
        self.button()
        self.exit_button()
    def header(self):
        #Header layout for stuff
        heading1_label=tk.Label(self.parent,text="\nWelcome to Subseeker Setup Utility\n",fg="black",font="NanumGothicCoding 15 bold")
        heading1_label.pack(padx=20)
        heading ='You are supposed to have an opensubtitle account\nto continue with Subseeker, please provide your\nlogin credentials below:'
        heading2_label=tk.Label(self.parent,text=heading,fg='blue',font='NanumGothicCoding 10 italic').pack()
    def input_fields(self):
        usr_label=tk.Label(self.parent,text='\nEnter username:',fg='black',font='NanumGothicCoding 10',anchor='e').pack()
        self.usr_entry = tk.Entry(self.parent)
        self.usr_entry.pack()
        usr_label=tk.Label(self.parent,text='\nEnter password:',fg='black',font='NanumGothicCoding 10',anchor='e').pack()
        self.pwd_entry = tk.Entry(self.parent,show="*")
        self.pwd_entry.pack()
    def language_selection(self):
        heading = tk.Label(self.parent,text='\nSelect Your default language for subtitles below:').pack()
        with open('lang_pack.csv','r') as languages:
            languages = languages.read().split('\n')
            languages = [i.split(',')[1] for i in languages if len(i) > 1]
        self.language = tk.StringVar(self.parent)
        self.language.set(languages[2]) # default value
        self.lang_selection = tk.OptionMenu(self.parent,self.language, *languages)
        self.lang_selection.pack()
    def button(self):
        submit_button = tk.Button(self.parent,text='Submit',font='Consolas 11',command=self.process).pack(padx=160,pady=10)

    def process(self):
        if self.usr_entry.get() and self.pwd_entry.get() and self.lang_selection:
            print("Process Started!")
            with open('lang_pack.csv') as lang_code:
                lang_code = lang_code.read().split('\n')
                lang_code = dict( [i.split(',')[::-1] for i in lang_code if len(i) > 1])
            username,password,default_lang = [self.usr_entry.get(),self.pwd_entry.get(),lang_code[self.language.get()]]
            f = open('usr_config.ini','w')
            f.write('%s|%s|%s'%(username,password,default_lang))
            f.close()
            self.parent.destroy()
            print("Now installing ......")
            print("\n Copying Files......")

            cwd = os.getcwd()
            try:
                os.mkdir(os.path.expanduser('~')+'/.subseeker/')
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
            self.launch_readme()
        else:
            print("Plese provide with usrname and password!")
    def exit_button(self):
        exit_button = tk.Button(root,text='Exit!',font="NanumGothicCoding 12 bold",fg='dark red',command=root.destroy).pack(pady=0)

    def mycolor(x):
        return '#%02x%02x%02x' % x
    def launch_readme(self):
        f = open(os.path.expanduser('~')+'/readme.txt','w')
        f.write(string)
        f.close()
        call(["gedit",os.path.expanduser('~')+'/readme.txt'])
    
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
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
