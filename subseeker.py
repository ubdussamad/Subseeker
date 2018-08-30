#!/usr/bin/env python
import os,sys,re,traceback
from time import sleep
from utils import *
from comparison_statics import compare
from urllib import urlopen
from zipfile import ZipFile
from StringIO import StringIO


class config(object):
  config_file_object = open(os.path.expanduser('~/.subseeker/usr_config.ini'),'r')
  config_file = config_file_object.read()
  config_file_object.close()
  config_data = config_file.strip('\n').split('|')
  log_file_object = open(os.path.expanduser('~/.subseeker/sub_log.txt'),'r')
  log_file = log_file_object.read()
  log_file_object.close()
  log = ['.'.join(i.split('|')[0].strip(' ').split('.')[:-1]) for i in log_file.split('\n') if i]
  username,password,default_language = config_data




class target(object):
  if len(sys.argv) >= 2: media_path = sys.argv[1]

  else: media_path = '/home/samad/Videos/Movies/The.Imitation.Game.2014.720p.BluRay.x264.YIFY.mp4' #Change it to your local file to run tests

  series = re.findall('(\w\d\d\w\d\d)',media_path) or re.findall('(\\d+[x]\\d+)',media_path)
  media_hash  = str(hashFile(media_path))
  media_size  = str(os.path.getsize(media_path))
  media_name  = media_path.split('/')[-1].split('.')
  media_name  = '.'.join(media_name[:-1])

  if series:
    media_name  = ' '.join(media_path.split('/')[-1].replace(series[0],' ').split('.')[:-1]).strip(' ')
    media_name  = ''.join([i if (i not in ['_','.','-']) else ' ' for i in media_name])
    series = re.findall('(\\d+)',series[0])
  



def main(ost):
  
  if not(is_connected("www.opensubtitles.org")):
          print("No Internet Connection.")
          return(1)
  else: print("Internet Connectivity: OK!")
  fresh = 1
  if target.media_name in  config.log:
  	fresh = 0


  if not(ost.login(config.username,config.password)):
          print("Bad Login, Please re-install with correct credentials.")
          return(1)
  else: print("Login Credentials: Passed!")
  sleep(1)
  
  ''' LAYER - I '''
  if not target.series:
        data = ost.search_subtitles([{'sublanguageid': 'en', 'moviehash': target.media_hash, 'moviebytesize': target.media_size}] )
        data = data + ost.search_subtitles([{'sublanguageid': 'en','moviebytesize': target.media_size ,'query': target.media_name}])
  else:
        data = ost.search_subtitles([{'sublanguageid': 'en','moviebytesize': target.media_size ,'query': target.media_name,
                                      'season': target.series[0] , 'episode': target.series[1] }])
        data = data + ost.search_subtitles([{'sublanguageid': 'en','moviehash': target.media_hash,'moviebytesize': target.media_size}])
  ''' LAYER - I ENDS '''

  ''' LAYER - II '''
  ziplink = filter( None, [i.get('ZipDownloadLink') if (i.get('SubLanguageID')==config.default_language) else None for i in data] )
  chosen = False
  if len(data) and (not ziplink or not fresh):
  	from options_diag import question
  	if question(["You are downloading the same sub second time.","Would you like to select Subtitle manually?"] if not fresh else ["No Subtitles found in your Language.","Would you like to check other languages?"] ):
  		available_subs = []

        for n,i in enumerate(data):

          available_subs.append((str(n),i.get('SubFileName')
          ,lang_name_from_lang_code(i.get('SubLanguageID')),str(i.get('Score')),i.get('ZipDownloadLink')))

        from selection_panel import selection_panel_func

        z = selection_panel_func(available_subs)
        if z is not None:
          ziplink = available_subs[int(z)][4]
          chosen = True

          
  if not ziplink and len(data):
    print("No Subtitles found in your default language.")
    return(1)

  elif not len(data):
      print("No subtitles found for the given video in any language.")
      return(1)
  ''' LAYER - III (Comapring SubFileName)'''
  scores = []
  for i in data:
  	lang = i['SubLanguageID'] == config.default_language
  	scores.append( compare( '.'.join(i['SubFileName'].split('.')[:-1]) ,target.media_name) if lang else 0 )
  m =  max(scores)
  index = scores.index(m)
  ziplink = data[index]['ZipDownloadLink'] if not chosen else ziplink

  print('No. of Subs found: %d'%len(data))
  print("Best Sub Score is: %s"%(str(m) if m!=1.0 else 'Point Blank HIT!'))
  print('Sub language: %s'%lang_name_from_lang_code(data[index]['SubLanguageID']))
  print('Movie Imdb rating: %s'%str(data[index]['MovieImdbRating']))
  print('Subname: %s\nMedia name: %s'%(data[index]['SubFileName'], target.media_name))
  print('Subtitles service powered by www.OpenSubtitles.org')

  ''' LAYER III ENDS'''
  
  if ziplink:#Downloading and extracting the subtitle
      url = urlopen(ziplink[index] if type(ziplink) == list else ziplink)
      zip_ref = ZipFile(StringIO(url.read()))
      zip_ref.extractall('/'.join(target.media_path.split('/')[:-1]))
      zip_ref.close()
      
      print("Subtitle Download Complete.")
      ost.logout()
      import time
      try:
        log = open(os.path.expanduser('~/.subseeker/sub_log.txt'),'a')
        log.write(str(target.media_path.split('/')[-1]+' | '+time.ctime() +  ' | ' + config.username +'\n\n'))
        log.flush()
        log.close()
      except:
        log = open(os.path.expanduser('~/.subseeker/sub_log.txt'),'w')
        log.write(str(target.media_path.split('/')[-1]+' | '+time.ctime() +  ' | ' + config.username +'\n\n'))
        log.flush()
        log.close()
      del time
      return(0)
  return(1)

def apology():
    f = open('/'.join(target.media_path.split('/')[:-1])+'/Sorry, We didn\'t find any Subtitle.txt','w')
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
	ost = OpenSubtitles()
	try:
		if main(ost):
			apology()
			ost.logout()
		else:
			ost.logout()
	except: #Even in the worst case scenario it'll atleast logout.
		traceback.print_exc()
		try:
			print 'Logging Out after faliure.'
			ost.logout()
			print 'Logged out'
		except:
			print ' Failed to even log out'
