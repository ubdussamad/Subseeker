#!/usr/bin/env python
import os,sys,re
from utils import *
from urllib import urlopen
from zipfile import ZipFile
from StringIO import StringIO


class config(object):
  config_file_object = open(os.path.expanduser('~/.subseeker/usr_config.ini'),'r')
  config_file = config_file_object.read()
  config_file_object.close()
  config_data = config_file.strip('\n').split('|')
  username,password,default_language = config_data



class target(object):
  if len(sys.argv) >= 2: media_path = sys.argv[1]

  else: media_path = '/home/samad/Silicon-Valley-5x05.mp4'#'[Insert Movie Link here to test]' #Change it to your local file to run tests

  series = re.findall('(\w\d\d\w\d\d)',media_path) or re.findall('(\\d+[x]\\d+)',media_path)
  series = series[0]
  media_hash = str(hashFile(media_path))
  media_size = str(os.path.getsize(media_path))

  if series:
    media_name  = ' '.join(media_path.split('/')[-1].replace(series,' ').split('.')[:-1]).strip(' ')
    media_name = ''.join([i if (i not in ['_','.','-']) else ' ' for i in media_name])
    series = re.findall('(\\d+)',series)
  



def main():
  
  if not(is_connected("www.opensubtitles.org")):
          print("No Internet Connection.")
          return(1)
      
  ost = OpenSubtitles()

  if not(ost.login(config.username,config.password)):
          print("Bad Login, Please check credentials.")
          return(1)
          
  if not target.series:
        data = ost.search_subtitles([{'sublanguageid': 'en', 'moviehash': target.media_hash, 'moviebytesize': target.media_size }] )
  else:
        data = ost.search_subtitles([{'sublanguageid': 'en','moviebytesize': target.media_size ,'query': target.media_name,
                                      'season': target.series[0] , 'episode': target.series[1] }])
        
  ziplink = filter( None, [i.get('ZipDownloadLink') if (i.get('SubLanguageID')==config.default_language) else None for i in data] )
  
  if len(data) and not ziplink:
    
    from options_diag import *

    if question():

      available_subs = []

      for n,i in enumerate(data):

        available_subs.append((str(n),i.get('SubFileName')
        ,lang_name_from_lang_code(i.get('SubLanguageID')),str(i.get('Score')),i.get('ZipDownloadLink')))

      from selection_panel import *

      z = selection_panel_func(available_subs)

      if z is not None:
        ziplink = available_subs[int(z)][4]

        
  if not ziplink and len(data):
    print("No Subtitles found in your default language.")
    return(1)

  elif not len(data):
      print("No subtitles found for the given video in any language.")
      return(1)

  if ziplink:#Downloading and extracting the subtitle
      url = urlopen(ziplink[0] if type(ziplink) == list else ziplink)
      zip_ref = ZipFile(StringIO(url.read()))
      zip_ref.extractall('/'.join(target.media_path.split('/')[:-1]))
      zip_ref.close()
      print("Subtitle Download Complete.")
      ost.logout()
      return(0)
    
  return(1)

def apology():
    f = open('/'.join(target.media_path.split('/')[:-1])+'/Sorry, We can\'t find a Sub.txt','w')
    f.write(''' We are truely sorry for the inconvinience caused! \n
                \n We tried to get the subtitle for your movie/video:
                \n %s \n\n But had no Luck! \n This can happen due to some of the reasons below:
                \n * Sub dosen't exists on Opensubtitles.org
                \n * The movie is new and it's Hash isn't available or linked to the Subtitle.
                \n * Internet Connection problem.
                \n * The video is not popular (A recorded video or A music video).
                \n\n All of the above reasons could introduce this error!
                \n   Contact ubdussamad at_the_rate gmail _.com , To report any persistent Error.
                \n ||Thanks for using Subseeker ||'''%(target.media_path.split('/')[-1]))
    f.close()


if __name__ == "__main__":
  if main():
    apology()
