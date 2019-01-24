#!/usr/bin/env python
import os,sys,re,traceback
from utils import *
from comparison_statics import compare
from selection_panel import selection_panel_func
from options_diag import question
from urllib import urlopen
from zipfile import ZipFile
from StringIO import StringIO

class config(object):
    
    #Suite for reading user credential config file.
    config_file_object = open(os.path.expanduser('~/.subseeker/usr_config.ini'),'r')
    config_file = config_file_object.read()
    config_file_object.close()
    config_data = config_file.strip('\n').split('|')
    username,password,default_language = config_data

    #Suite for reading logfile used to check for re-downloading of sub.
    log_file_path = os.path.expanduser('~/.subseeker/sub_log.txt')

    if os.path.isfile ( log_file_path ): #If the file exists.
        log_file_object = open( log_file_path ,'r')
        log_file = log_file_object.read()
        log_file_object.close()
        log = ['.'.join(i.split('|')[0].strip(' ').split('.')[:-1]) for i in log_file.split('\n') if i]
    else: # If the installation is new and file dosen't exist.
        log = []



class target(object):
    if len(sys.argv) >= 2: media_path = sys.argv[1].strip('\n')

    #The media path defaults to succeeding path for debugging.
    else: media_path = '/media/samad/01CDE561CCAC6150/Movies/The.Imitation.Game.2014.720p.BluRay.x264.YIFY.mp4'

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
        print("Subtitle Download Failed. :(")
        print("No Internet Connection.")
        return(1)
    else: print("Internet Connectivity: OK!")

    #Checks if user is downloading the sub or not.
    fresh = False if target.media_name in  config.log else True

    if not(ost.login(config.username,config.password)):
        print("Subtitle Download Failed. :(")
        print("Bad Login, Please re-install with correct credentials.")
        return(1)
    else: print("Login Credentials: Passed!")

    #Checks if given media is a series or not and genrates the query accordingly
    if not target.series:
        data = ost.search_subtitles([{'sublanguageid': 'en', 'moviehash': target.media_hash, 'moviebytesize': target.media_size}] )
        data = data + ost.search_subtitles([{'sublanguageid': 'en','moviebytesize': target.media_size ,'query': target.media_name}])
    else:
        data = ost.search_subtitles([{'sublanguageid': 'en','moviebytesize': target.media_size ,'query': target.media_name,
                                      'season': target.series[0] , 'episode': target.series[1] }])
        data = data + ost.search_subtitles([{'sublanguageid': 'en','moviehash': target.media_hash,'moviebytesize': target.media_size}])

    # If there are no Subs available.
    if not(len(data)):
        print("Subtitle Download Failed. :(")
        print("No Subtitle found in any Language for the Media.")
        return(1)

    # Filters out the Subs which aren't in default language 
    potential_subs = filter( None, [i if (i.get('SubLanguageID')==config.default_language) else None for i in data] )
    chosen = False

    # If the Subtitle has been downloaded before.
    if not fresh:
        if question(["You are downloading the same sub second time.","Would you like to select Subtitle manually?"]):
  		available_subs = []
                for n,i in enumerate(data):
                    available_subs.append((str(n),i.get('SubFileName'),i.get('LanguageName'),
                                           str(i.get('Score')),i.get('ZipDownloadLink')))
                z = selection_panel_func(available_subs)
                if z is not None:
                        potential_subs = [data[int(z)]] # Now ziplink has only one selected value
                        chosen = True
                else:
                    print("Subtitle Download Failed. :(")
                    print("An Unexpected Error Occured, Code: 0x1")
                    return(1)
        else:
            print("Subtitle Download Failed. :(")
            print("Sorry, nothing can be done from this end now.")
            return(1)
        
    # If there are no Subs available in the defalut language    
    elif not len(potential_subs):
        if question(["No Subtitles found in your Language.","Would you like to check other languages?"]):
  		available_subs = []
                for n,i in enumerate(data):
                    available_subs.append((str(n),i.get('SubFileName'),i.get('LanguageName'),
                                           str(i.get('Score')),i.get('ZipDownloadLink')))
                z = selection_panel_func(available_subs)
                if z is not None:
                        potential_subs = [data[int(z)]] # Now ziplink has only one selected value
                        chosen = True
                else:
                    print("Subtitle Download Failed. :(")
                    print("An Unexpected Error Occured, Code: 0x2")
                    return(1)
        else:
            print("Subtitle Download Failed. :(")
            print("Sorry, nothing can be done from this end now.")
            return(1)

    # Processing and downloading data
    scores = []
    for i in potential_subs:
  	scores.append( compare( '.'.join(i.get('SubFileName').split('.')[:-1]) ,target.media_name)) #problem
    m =  max(scores)
    index = scores.index(m)
    ziplink = potential_subs[index]['ZipDownloadLink']

    if ziplink:#Downloading and extracting the subtitle
          url = urlopen(ziplink[index] if type(ziplink) == list else ziplink)
          zip_ref = ZipFile(StringIO(url.read()))
          zip_ref.extractall('/'.join(target.media_path.split('/')[:-1]))
          zip_ref.close()
          print("No. of Subs found: %d"%len(data))
          print("Best Sub Score is: %s"%  (str(m) if m!=1.0 else 'Point Blank HIT!') if not chosen else ("Manually Selected.") )
          print('Sub language: %s'%lang_name_from_lang_code( potential_subs[index]['SubLanguageID'] ) )
          print('Movie Name: %s | Year: %s'%(str( potential_subs[index]['MovieName']) , potential_subs[index]['MovieYear'] ))
          print('Movie Imdb rating: %s'%str( potential_subs[index]['MovieImdbRating']))
          print('Subname: %s\nMedia name: %s'%( potential_subs[index]['SubFileName'], target.media_name))
          print('Subtitles service powered by www.OpenSubtitles.org')
          print("\nSubtitle Download Complete.!\n")
          ost.logout()
          import time
          try:
              log = open(os.path.expanduser('~/.subseeker/sub_log.txt'),'a')
              log.write(str(target.media_path.split('/')[-1]+' | '+time.ctime() +  ' | ' + config.username +'\n\n'))
              log.flush()
              log.close()
              return(0)
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
