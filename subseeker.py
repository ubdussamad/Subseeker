#!/usr/bin/env python
import struct,os,sys,socket
import os.path
from urllib import urlopen
from zipfile import ZipFile
from StringIO import StringIO
from xmlrpclib import ServerProxy, Transport

REMOTE_SERVER = "www.opensubtitles.org"

def is_connected(hostname):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80), 2)
    return True
  except:pass
  return False

def hashFile(name): 
      try: 
                longlongformat = '<q'  # little-endian long long
                bytesize = struct.calcsize(longlongformat)     
                f = open(name, "rb")    
                filesize = os.path.getsize(name) 
                hash = filesize     
                if filesize < 65536 * 2: 
                       return "SizeError"  
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number      
                f.seek(max(0,filesize-65536),0) 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF                  
                f.close()
                returnedhash =  "%016x" % hash 
                return returnedhash 
      except(IOError): 
                return "IOError"

class LoginError(Exception):#Login Faliures
    pass
    
class URLError(Exception):#Internet Connectivity Faliures
    pass

class NoLangMatchError(Exception):#Default language dosen't matches
    pass
    
           
class Settings(object):
    OPENSUBTITLES_SERVER = 'http://api.opensubtitles.org/xml-rpc'
    USER_AGENT = 'TemporaryUserAgent'
    LANGUAGE = 'en'
    
def lang_name_from_lang_code(code):
  with open(os.path.expanduser('~/.subseeker/lang_pack.csv'),'r') as lang_code:
    lang_code = lang_code.read().split('\n')
    lang_code = dict( [i.split(',')[:] for i in lang_code if len(i) > 1])
  try:
    return(lang_code[code])
  except:
    return(code.upper())

            
class OpenSubtitles(object):
    def __init__(self, language=None, user_agent=None):
        self.language = language or Settings.LANGUAGE
        self.token = None
        self.user_agent = user_agent or os.getenv('OS_USER_AGENT') or Settings.USER_AGENT

        transport = Transport()
        transport.user_agent = self.user_agent

        self.xmlrpc = ServerProxy(Settings.OPENSUBTITLES_SERVER,
                                  allow_none=True, transport=transport)

    def _get_from_data_or_none(self, key):
        '''Return the key getted from data if the status is 200, otherwise return None.'''
        status = self.data.get('status').split()[0]
        return self.data.get(key) if '200' == status else None

    def login(self, username, password):
        '''Returns token is login is ok, otherwise None.'''
        self.data = self.xmlrpc.LogIn(username, password,
                                 self.language, self.user_agent)
        token = self._get_from_data_or_none('token')
        if token:self.token = token
        return token

    def logout(self):
        '''Returns True is logout is ok, otherwise None.
        '''
        data = self.xmlrpc.LogOut(self.token)
        return '200' in data.get('status')

    def search_subtitles(self, params):
        '''Returns a list with the subtitles info.'''
        self.data = self.xmlrpc.SearchSubtitles(self.token, params)
        return self._get_from_data_or_none('data')


full_path = sys.argv[1]#,usr,password = sys.argv
f = open(os.path.expanduser('~/.subseeker/usr_config.ini'),'r')
data = f.read().strip('\n').split('|')
usr,password,default_lang = data
f.close()



try:
    if not(is_connected(REMOTE_SERVER)):
        raise URLError,("No Internet Connection.")
    
    movie_hash = hashFile(full_path) #Covered
    ost = OpenSubtitles() #Username and password are given as arguments | Covered
    
    if not(ost.login(usr,password)):
        raise LoginError("Bad Login, Please check credentials.")

    size = str(os.path.getsize(full_path))
    data = ost.search_subtitles([{'sublanguageid': 'en', 'moviehash': str(movie_hash), 'moviebytesize': size }])
    ziplink = None
    for i in data:
      if i.get('SubLanguageID') == default_lang:
            ziplink = i.get('ZipDownloadLink')
            break

    if len(data) and not ziplink:
      from options_diag import *
      if ext():
        available_subs = []
        for n,i in enumerate(data):
          available_subs.append((str(n),i.get('SubFileName'),lang_name_from_lang_code(i.get('SubLanguageID')),str(i.get('Score')),i.get('ZipDownloadLink')))
        from selection_panel import *
        z = run(available_subs)
        if z is not None:
          ziplink = available_subs[int(z)][4]
    if not ziplink:
      raise NoLangMatchError,("Your default language's sub not found.")
    if ziplink:#Downloding n extracting the subtitle
        url = urlopen(ziplink)
        zip_ref = ZipFile(StringIO(url.read()))
        zip_ref.extractall('/'.join(full_path.split('/')[:-1]))
        zip_ref.close()
    print("Subtitle Download Complete.")
except Exception as err:
    print(err)
    f = open('Sorry, We can\'t find a Sub.txt','w')
    f.write(''' We are truely sorry for the inconvinience caused! \n
            \n We tried to get the subtitle for your movie/video:
            \n %s \n\n But had no Luck! \n This can happen due to some of the reasons below:
            \n * Sub dosen't exists on Opensubtitles.org
            \n * The movie is new and it's Hash isn't available or linked to the Subtitle.
            \n * Internet Connection problem.
            \n * The video is not popular (A recorded video or A music video).
            \n\n All of the above reasons could introduce this error!
            \n   Contact ubdussamad at_the_rate gmail _.com , To report any persistent Error.
            \n ||Thanks for using Subseeker ||'''%(full_path.split('/')[-1]))
    f.close()
ost.logout()
