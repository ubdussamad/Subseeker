import os,struct,socket
from xmlrpclib import ServerProxy, Transport

''' //////////////////////////////////////////
    This module contains Utility methods for subseeker
    ////////////////////////////////// ''' 


'''  /////////////////////
     Returns the Language name from the obtained Language Codes
     ///////////////////// '''

def lang_name_from_lang_code(code):
  with open(os.path.expanduser('~/.subseeker/lang_pack.csv'),'r') as lang_code:

    lang_code = lang_code.read().split('\n')
    lang_code = dict( [i.split(',')[:] for i in lang_code if len(i) > 1])
    
  return lang_code[code] if code in lang_code else code.upper()


''' /////////////////////
    For Calculating Movie hash
    ///////////////////// '''

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

''' /////////////////////
    Checking Internet Connectivity Status
    ///////////////////// '''

def is_connected(hostname):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80), 2)
    return True
  except:return False

''' ////////////////////
    Opensubtitles XML RPC API Client's Python Implimentaion
    ////////////////////  '''

class Settings(object):
    OPENSUBTITLES_SERVER = 'http://api.opensubtitles.org/xml-rpc'
    USER_AGENT = 'subseeker_v7'
    LANGUAGE = 'eng'

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

''' /////////////////////
    Internal Method Tests
    ///////////////////// '''

if __name__ == '__main__':
    print("Testing Components....\n"+'-'*20)
    if is_connected("www.google.com"): print('Function is_connected: Ok!')
    else: print("Function is_connected: Failed!")
    
    if lang_name_from_lang_code('eng'): print('Function lang_name_from_lang_code: Ok!')
    else: print("Function lang_name_from_lang_code: Failed!\n")

    if hashFile('utils.py'): print('Function hashFile: Ok!')
    else: print("Function hashFile: Failed!")
