#!/usr/bin/env python

from __future__ import print_function
import struct, os
import os,sys
import os.path
from urllib import urlopen
from zipfile import ZipFile
from StringIO import StringIO
import sys
try:                    #Python 2
    from xmlrpclib import ServerProxy, Transport
except ImportError:     #Python 3
    from xmlrpc.client import ServerProxy, Transport
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
                
class Settings(object):
    OPENSUBTITLES_SERVER = 'http://api.opensubtitles.org/xml-rpc'
    USER_AGENT = 'TemporaryUserAgent'
    LANGUAGE = 'en'
class OpenSubtitles(object):
    '''OpenSubtitles API wrapper.
    Please check the official API documentation at:
    http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
    '''
    def __init__(self, language=None, user_agent=None):
        """
        Initialize the OpenSubtitles client
        
        :param language: language for login
        :param user_agent: User Agent to include with requests.
            Can be specified here, via the OS_USER_AGENT environment variable,
            or via Settings.USER_AGENT (default)
            
            For more information: http://trac.opensubtitles.org/projects/opensubtitles/wiki/DevReadFirst#Howtorequestanewuseragent 
        """
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
        '''Returns token is login is ok, otherwise None.
        '''
        self.data = self.xmlrpc.LogIn(username, password,
                                 self.language, self.user_agent)
        token = self._get_from_data_or_none('token')
        if token:
            self.token = token
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
    def no_operation(self):
        '''Return True if the session is actived, False othercase.
        .. note:: this method should be called 15 minutes after last request tothe xmlrpc server.'''
        data = self.xmlrpc.NoOperation(self.token)
        return '200' in data.get('status')
    def auto_update(self, program):
        '''Returns info of the program: last_version, url, comments...'''
        data = self.xmlrpc.AutoUpdate(program)
        return data if '200' in data.get('status') else None
    def check_subtitle_hash(self,sub_hash):
        '''Returns a dictionary where key is subtitle file hash and value is SubtitleFileID.
        If subtitle file is not found then value is 0.
        :param sub_hash: list of subtitle file hashes.'''
        self.data = self.xmlrpc.CheckSubHash(self.token, sub_hash)
        return self._get_from_data_or_none('data')
    def check_movie_hash(self, movie_hash):
        '''Returns a dictionary with hash as key and movie information as value.
        :param movie_hash: list of hash of movies.'''
        self.data = self.xmlrpc.CheckMovieHash(self.token, movie_hash)
        return self._get_from_data_or_none('data')
    def get_subtitle_languages(self,language='en'):
        '''Returns list of supported subtitle languages in specified langauge; default is english.'''
        self.data = self.xmlrpc.GetSubLanguages(language)
        return self.data['data']
    def get_imdb_movie_details(self,imdb_id):
        '''Returns movie information from IMDb.com'''
        self.data = self.xmlrpc.GetIMDBMovieDetails(self.token,imdb_id)
        return self._get_from_data_or_none('data')
    def subtitles_votes(self,vote):
        '''Give rating to subtitle.
        Returns Subtitle Rating, Total number of votes and ID of Subtitle if rating was successful else None.
        :param vote: Dictionay with idsubtitle and score.'''
        self.data = self.xmlrpc.SubtitlesVote(self.token,vote)
        return self._get_from_data_or_none('data')



#apt-get install nautilus-actions
full_path = sys.argv[1]#,usr,password = sys.argv

f = open(os.path.expanduser('~/.subseeker/usr_config.ini'),'r')
data = f.read().split('|')
usr,password = data
f.close()



try:
    movie_hash = hashFile(full_path)
    ost = OpenSubtitles()
    ost.login(usr,password) #Username and password are given as arguments
    print('Path and names are:',full_path)
    size = str(os.path.getsize(full_path))
    #nautilus actions must be used
    #apt-get install nautilus-actions
    data = ost.search_subtitles([{'sublanguageid': 'en', 'moviehash': str(movie_hash), 'moviebytesize': size }])

    for i in data:
        if i.get('SubLanguageID') == 'eng':
            ziplink = i.get('ZipDownloadLink')
            break
    if ziplink:#Downloding n extracting the subtitle
        url = urlopen(ziplink)
        zip_ref = ZipFile(StringIO(url.read()))
        zip_ref.extractall('/'.join(full_path.split('/')[:-1]))
        zip_ref.close()
except:
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
