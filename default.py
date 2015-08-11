# uppit is possible post then play
import platform
print 'platform.python_version()',platform.python_version()
import sys
import xbmcgui
import xbmcplugin,xbmcvfs
import xbmcaddon,xbmc,os
import urllib
import urllib2
import requests
import re
import settings
import time

try:
    import json
except:
    import simplejson as json
from urllib import FancyURLopener
from bs4 import BeautifulSoup
#import httplib2
import cPickle as pickle
headers=dict({'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:32.0) Gecko/20100101 Firefox/32.0'})

addonID = 'plugin.video.BDdoridro'
addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
addon = xbmcaddon.Addon(id='plugin.video.BDdoridro')
handle = int(sys.argv[1])
logopath = os.path.join( addonUserDataFolder, 'logos')
cacheDir = os.path.join( addonUserDataFolder, 'cache')
clean_cache=os.path.join(cacheDir,'cleancacheafter1month')
metadata_uls=os.path.join(cacheDir,'metadata_uls.txt')
logos = None
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
Doridro_USER = settings.doridro_user()
Doridro_PASSWORD = settings.doridro_pass()
cookie_jar = settings.cookie_jar()
#http://www.moviesfair24.com/category/natok-telefilm-bangla/
if not cacheDir.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')) and not os.path.isdir(cacheDir)== 1 :
    os.mkdir(cacheDir)


if not logopath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')) and not os.path.isdir(logopath)== 1 :
    os.mkdir(logopath)
#if xbmcvfs.exists(clean_cache):
#    if int(time.time()-os.path.getmtime(clean_cache)) >  300 :#300 is 1 month      #60*60*24*30):
#        print 'time of creation of ff',str(time.time()-os.path.getmtime(clean_cache))
#        import shutil
#        shutil.rmtree(cacheDir)
#        shutil.rmtree(logopath)
#        #notification("Cache Cleared","old cache cleared")
#        os.mkdir(logopath)
#        os.mkdir(cacheDir)
#else:
#    with open(clean_cache,'w') as f:
#        f.write('')
#h = httplib2.Http(cacheDir)
forum_url = "http://doridro.com/forum/viewforum.php?f={0}"
xbmcplugin.setContent(handle, 'movies')
def ensure_dir():
    print 'creating dir'
    d = logopath
    print d
    if not os.path.isdir(d)== 1:
        print ' Nor logos exist 0creating one dir'
        os.mkdir(d)


def get_match(data, regex) :
    match = "";
    m = re.search(regex, data)
    if m != None :
        match = m.group(1) #.group() method to extract specific parts of the match
    else:
        match = ''
    return match

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
def getCookieJar(cookie_jar):
    import cookielib
    cookieJar=None
    if COOKIEFILE:
        try:
            cookieJar = cookielib.LWPCookieJar()
            cookieJar.load(cookie_jar,ignore_discard=True)
        except:
            cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()

    return cookieJar
    
def get_thumb(title):
    
    
    if os.path.exists(metadata_uls):
        content = open(metadata_uls).read()
        #print content
        pat = r'%s:(\S+)' %re.escape(title)
        print pat
        if title in content:
            print '{0} ::title found in the file '.format(title)
            match = re.compile(pat,re.DOTALL).findall(content)
            print match
            return match[0]
        #thumb = re.search(metadataurl,content)
        else:
            imgurl = google_image(title)
            
            if imgurl :
                metadataurl = title +':' + imgurl + '\n'
                with open (metadata_uls, 'a') as f :
                   f.write(metadataurl)
                return imgurl
            else:
                return 'ignore'
    else:
        print 'making new metadata file'
        imgurl = google_image(title)
        if imgurl :
            metadataurl = title +':' + imgurl + '\n'
            with open (metadata_uls, 'w') as f :
               f.write(metadataurl)
            return imgurl
        else:
            return 'ignore'
def google_image(title):
    #ensure_dir()
    searchTerm = title

    # Replace spaces ' ' in search term for '%20' in order to comply with request
    searchTerm = urllib.quote(searchTerm).replace('%20','+')
    # Start FancyURLopener with defined version
    myopener = MyOpener()

    # Set count to 0
    count= 0

    for i in range(0,1):
        # Notice that the start changes for each iteration in order to request a new set of images for each loop as_filetype=png as_sitesearch=photobucket.com rsz=4
        url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP&as_sitesearch=http://doridro.com/forum/')
        print url
        res,new = cache(url,duration=1)
        
        if not res :
            print 'No image found for :%s' %title
            return
        results = json.loads(res)
        data = results['responseData']['results']
        if data:
        #t_results = results['responseData']['cursor']['estimatedResultCount']
        #print t_results
        #thum_list = []
        #if not t_results == None:
            #print myUrl['unescapedUrl']
            for i in range(2):
                try:

                    thumb_url= data[i]['unescapedUrl']
                    file_ext = ['jpg','jpeg','png','JPG','JPEG']
                    if any(x in thumb_url for x in file_ext):
                        print thumb_url
                        
                        #url_ext = thumb_url.rsplit('.',1)
                        #print url_ext
                        #title = title.encode('utf-8')
                        #print title
                        ##l=os.path.join(logopath, title  + str(count)+'.JPG')
                        #l=os.path.join(logopath, title  +'.'+url_ext[1])
                        #th= urllib.urlretrieve(thumb_url,l) # to download the file

                        return thumb_url
                    else:
                        count = count + 1
                        continue
                except Exception: pass
        else:
            print ('ignoring this title image : %s' %title)
    #return th
def check_login(source,username):

    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = username

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False
def down_url(url,filename=None):
    print 'found download path::', addon.getSetting('download_path')
    if addon.getSetting('download_path') == '':
            addon.openSettings()
    get_file_name = url.split('/')[-1]
    file_name = os.path.join(addon.getSetting('download_path').encode('utf-8'),get_file_name)
    pDialog = xbmcgui.DialogProgress()
    #pDialog = xbmcgui.DialogProgressBG()
    pDialog.create('Downloading ......', 'File to download: %s ...' %get_file_name)
    size = 0
    block_sz = 8192
    req = urllib2.Request(url,None,headers)
    song = urllib2.urlopen(req)
    meta = song.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    with open(file_name, 'wb') as f:    
        while True:
            buffer = song.read(block_sz)
            if not buffer:
                break

            size += len(buffer)
            f.write(buffer)
            #status = r"%10d  [%3.2f%%]" % (size, size * 100. / file_size)
            #status = r"%3.2f%%" % (size * 100. / file_size)
            #status = status + chr(8)*(len(status)+1)
            #print status
            pDialog.update(int(size * 100. / file_size),'Download progressing...Will be SaveTo:\n%s' %file_name)
    pDialog.close()
def _login():
    if Doridro_USER == '' :
        return
    

    if os.path.exists(cookie_jar) and (time.time()-os.path.getmtime(cookie_jar) < 60*60*24) and os.path.getsize(cookie_jar) > 5:
        #notification('Already Logged IN','Logged In to doridro.Com as %s ::.'%Doridro_USER,2000)
        print 'Logged in for A day'
    else:
        session = requests.Session()
        login_url='http://doridro.com/forum/ucp.php?mode=login'
        body = {'username' : '%s' %Doridro_USER,'password' : '%s' %Doridro_PASSWORD,'autologin' : '1','login' : 'login'}
        r = session.post(login_url,data = body,headers=headers)

        Cookie =  session.cookies.get_dict()      #str(r.headers['set-cookie'])
        #print r.cookies
        loged_in = check_login(r.text,'alibaba011')
        if loged_in == True:
            notification('Login Succes','Succesfully loged_in to doridro.Com as %s ::.'%Doridro_USER,2000)
            #return r.cookies
            pickle.dump( Cookie, open( cookie_jar, "wb" ) )
        #with open(cookie_jar,'w') as f:
           #f.write(str(Cookie))

def get_soup(url,content=None,ref=None,post=None,mobile=False):
    if not url == '' :
        if ref:
            print 'we got ref',ref
            headers.update({'Referer': '%s'%ref})
        else:
            headers.update({'Referer': '%s'%url})
        if mobile:
            headers.update({'User-Agent' : 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'})
        req = urllib2.Request(url,None,headers)
        resp = urllib2.urlopen(req)
        content = resp.read()
        resp.close()
    try:
        soup = BeautifulSoup(content,'html.parser')
        print 'using html.parser'
    except:
        soup = BeautifulSoup(content)


    print len(soup)

    return soup



def CATEGORIES(name):
    if not Doridro_USER == '' :
        _login()
        addDir("Natok & Telefilms", '155',3,'','')
        addDir("Bangla Movies", '106',3,'','')
        addDir("Music[Download ONLY]", '166',3,'','')
        addDir("Kolkutta Music[Download ONLY]", '192',3,'','')
    addDir("Live TV", 'http://www.jagobd.com/category/bangla-tv',1,'','')
    #addDir("Drama Serials", 'http://doridro.com/forum/viewforum.php?f=99',99,'','')

    



def LiveBanglaTV(url):
    content,new = cache(url,duration=6)
    soup = get_soup('',content=content)
    l= soup('a' ,{'rel':"bookmark"})
    print len(l)
    for data in l:
        name = data.get('title')
        url = data.get('href')
        #print url
        try:
            img = data('img')[0]['src']
        except Exception:
            img = ''
        #print img
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setArt({ 'thumb': img, 'fanart' : img })
        liz.setIconImage(img)
        u = sys.argv[0] + '?mode=2' + '&url=' + urllib.quote_plus(url)\
            + '&name=' + urllib.quote_plus(name)
        #print u
        xbmcplugin.addDirectoryItem(handle, u, liz, True)
def playlive(url,name):
    embed_url_pat = 'http://www.tv.jagobd.com/embed.php?u={0}&amp;vw=100%&amp;vh=400'

    content,new = cache(url,duration=3)
    
    match = re.compile(r'''jagobd\.com/embed\.php\?u=([^&]+)''',re.DOTALL).findall(content)
    print match
    if len(match) > 1 :
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose a video source', match)
        if index >= 0:
            print 'index choosen', str(index),match[1]
            
            final_url = livetv(embed_url_pat.format(match[index]),ref=url)
        else:
            return
    else :
        final_url = livetv(embed_url_pat.format(match[0]),ref=url)
    #soup = get_soup('',content=content)
    #embed_url=soup('div', {'class':"stremb"})[0]('a')[0].get('href')
    ##embed_url=soup('area', {'shape':"rect"}).get('href')
    #print 'the embed_url',embed_url
    #if addon.getSetting('typeofstream') == 0:
    #    final_url = 'http://' + livetv(embed_url,ref=url)
    #else:
    #    final_url = livetv(embed_url,ref=url)
    #play_url = makeRequest(final_url,mobile=True,ref=url)
    if not final_url == 'None':
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo(type='Video', infoLabels={'Title':name})
        xbmc.Player().play(final_url,listitem)
def livetv(embed_url,ref=None):
    token1 = '%xqdrde(nKa@#.'
    token2 = '%pwrter(nKa@#.'
    soup = get_soup(embed_url,ref=ref)
    l=soup('script', {'type':'text/javascript'})
    #l= soup('a' ,target=re.compile('ifra'))
    print l
    for data in l:
        if 'SWFObject' in data.text:
            #print data.text #%xqdrde(nKa@#. %xrtrpq(nKa@#.
            m = re.compile(r'''SWFObject[\(',"]+(.*?)[\(',"]+.*?[\(',"]+file[\(',"]+(.*?)[\(',"]+.*?'streamer[\(',"]+(.*?)[\(',"]+''',re.DOTALL).findall(data.text)
            print m
            if  not m[0][2] == 'None' :
                rtmp = m[0][2].encode('utf-8')
                playpath = m[0][1].encode('utf-8')
                swfurl = m[0][0].encode('utf-8')
                play_url = rtmp + ' timeout=15 token=%pwrter(nKa@#. live=1 playpath=' + playpath +' swfUrl='+swfurl+' pageurl='+embed_url

                return play_url
            else:
                return None
def _______livetv(embed_url,ref=None):
    headers.update({'User-Agent' : 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'})
    headers.update({'Referer' : ref})
    soup = requests.get(embed_url,headers=headers)
    #embed_url=soup('area', {'shape':"rect"})[0].get('href')
    final_url = re.compile('http://(.*)',re.DOTALL).findall(soup.text)[0]
    print final_url
    return final_url



def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def natok(url):
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Getting Natok', 'Downloading Natok with image ...')
        #pDialog.close()
        uurl = forum_url.format(url)
        content,new = cache(uurl, duration=2)
        print len(content)
        soup = get_soup('',content=content)
        #soup = get_soup(url)
        l = soup('a' ,{'class':'topictitle'})[9:70]
        print len(l)
        match=[]
        count = 0
        for i in l:
            href1 = i.get('href').split('&sid=')[0]
            #print href1
            #href = re.compile(r'''(.*?)&amp;sid=''',re.DOTALL).findall(href1)
            #print href
            name = removeNonAscii(i.text).encode('utf-8','ignore')
            tab= href1.replace('&amp;','&').replace('./','')
            url= 'http://doridro.com/forum/' + tab
            thumb_from_folderjpg = os.path.join(logopath,name+'.JPG')
            thumb_from_folderpng = os.path.join(logopath,name+'.png')
            if addon.getSetting('metadata') == 'true' :
                #try:
                    thumb_from_folder = get_thumb(name)
                    #if os.path.isfile(thumb_from_folderjpg):
                    #    thumb_from_folder = thumb_from_folderjpg
                    #    #print 'thumb found from folder'
                    #
                    #elif os.path.isfile(thumb_from_folderpng):
                    #    thumb_from_folder = thumb_from_folderpng
                    #
                    #else:
                    #    #print ('getting image from folder using google image search')
                    #    thumb_from_folder = google_image(name)
                #except:
                    #print 'No image'
            else:
                thumb_from_folder = ''
            count += 1
            pDialog.update(int(count*1.6), 'Downloading: %s  ...' %name)

            liz=xbmcgui.ListItem(name)
            liz.setInfo( type="Video", infoLabels={ "Title": name})
            #liz.setMimeType('mkv')
            liz.setArt({ 'thumb': thumb_from_folder, 'fanart' : thumb_from_folder })
            liz.setIconImage(thumb_from_folder)
            #print 'name to pass to videolinks', name
            u = sys.argv[0] + '?mode=5' + '&url=' + urllib.quote_plus(url)\
                + '&name=' + urllib.quote_plus(name)
            #print u
            xbmcplugin.addDirectoryItem(handle, u, liz, True)

        #xbmcplugin.endOfDirectory(handle)

            #xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True )
def solve_fileshare_url(link):

    extracted_url = ''
    if 'indishare' in link or 'bdupload' in link:
        extracted_url = indishare(link)
    elif 'uptobox' in link:
        extracted_url = uptobox(link)
    elif 'seenupload' in link:
        extracted_url = seenupload(link,url)
    elif 'uppit' in link:
        extracted_url = uppit(link,url)
    print 'extracted_url for :', link,extracted_url
    return extracted_url
def get_response(url):
    print url
    #net.set_cookies(cookie_jar)
    req = urllib2.Request(url)
    req.add_header('Host','doridro.com')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Accept','text/html, application/xhtml+xml, */*')
    req.add_header('Content-Type','application/x-www-form-urlencoded')
    req.add_header('Referer','http://doridro.com/forum/')
    resp = urllib2.urlopen(req)
    data = resp.read()
    resp.close()
    return data
def morelinks(name,url):
    print ('Building morevideolinks')
    print url
    #net.set_cookies(cookie_jar)
    req = urllib2.Request(url)
    req.add_header('Host','doridro.com')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Accept','text/html, application/xhtml+xml, */*')
    req.add_header('Content-Type','application/x-www-form-urlencoded')
    req.add_header('Referer','http://doridro.com/forum/')
    resp = urllib2.urlopen(req)
    contents = resp.read()
    resp.close()

    playurl = get_match(contents,'<a href="(.*?)"')
    print playurl
    item = xbmcgui.ListItem(name)
    item.setInfo(type="Video", infoLabels={"Title": name})
    #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    playlist.add(url=playurl, listitem=item)
    if not xbmc.Player().isPlayingVideo():
         xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)

def getVideolinks(name,url):
    music = False
    if 'f=166' in url or 'f=192' in url:
        music = True
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Getting Music links', 'Please wait ...')
    else:
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Getting Video links', 'Please wait ...')    
    content,new = cache(url,duration=1,need_cookie='login') 
    #allsources = re.compile(r'''class="postlink"\s*[href=]?.*?(https?://[^<"]+)''',re.DOTALL).findall(content)
    allsources = re.compile(r'''class="postlink"\s*[href=]?.*?[<|"](https?://[^<"]+)''',re.DOTALL).findall(content)
    #l = re.compile(r'''a\s*class="postlink"\s*href="([^"]+)''',re.DOTALL).findall(content)
    #l = re.compile(r'''rel="nofollow"\s*onclick="this\.target='_blank';">(.*?)</a>''',re.DOTALL).findall(content)
    #soup = BeautifulSoup(content,'html.parser')
    #l = soup('a',{'class': 'postlink'})
    print len(allsources)
    print allsources
    #return
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    domains = ['seenupload','uptobox','share.jong.li','indishare','uppit','bdupload']
    final_url = []
    tracks=[]
    if len(allsources) >1:
        for i in allsources:
            if music :
                import urlparse
                d_name= '[' + urlparse.urlparse(i).netloc + '] ' +   urllib.unquote_plus(i.split('/')[-1])
                #if d_name == '':
                #if d_name == '':
                #    tracks.append(name)
                #else:
                tracks.append(d_name)            
            elif 'share.jong.li' in i :
                print 'share.jong.li found'
                extracted_url = jongli(i,ref=url)
                print extracted_url
                if extracted_url :
                    final_url.append(extracted_url)
                else:
                    continue
            elif not any(x in i for x in domains):
                
                allsources.remove(i)
                #import urlparse
                #
                #
                #d_name=urlparse.urlparse(i).netloc
                #if d_name == '':
                #    names.append(name)
                #else:
                #    names.append(d_name)
            else:
                
                continue
        print 'url list now:::',allsources
        if len(final_url) >0:
            print final_url
            for stream in final_url:
                if not 'rar' in stream or not 'zip' in stream:
                    info = xbmcgui.ListItem('%s' %name)
                    playlist.add(stream, info)
            xbmc.Player().play(playlist)        
        
        elif len(tracks) >0 :
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose a video source', tracks)
            if index >= 0:
                if 'share.jong.li' in tracks[index] :
                #print 'share.jong.li found'
                    extracted_url = jongli(allsources[index],ref=url)
                else:
                    extracted_url = solve_fileshare_url(allsources[index])
                if len(extracted_url) >0:
                    down_url(extracted_url)
                
                #xbmc.Player().play(extracted_url)            
        
        else:
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose a video source', allsources)
            if index >= 0:
                extracted_url = solve_fileshare_url(allsources[index])
                #if len(extracted_url) >0:
                xbmc.Player().play(extracted_url)
        #    notification("failed to Play", "[COLOR yellow]Failed to extract video links[/COLOR]", sleep=1000)

    else:
        notification("NO Link found", "[COLOR yellow]There is no video for this link[/COLOR]", sleep=1000)
def jongli(link,ref=None):
    content,new = cache(link,duration=2,ref=url)
    #print soup
    print new
    match = re.compile(r'''<a\s*href="(\S+)">Click here to download''',re.DOTALL).findall(content)   
    print 'match found for jongli',match
    if match :
    #print len(l),l
        return match[0]
    else:
        return

def uppit(link,ref=None): #http://uppit.com/53lbeaylge7m/Bojhena_Se_Bojhena_&
    idd = link.rsplit('/',2)
    print idd
    id = idd[1]
    body = dict(method_free=' ',op="download1",usr_login=' ',id=id,fname='',referer='http://uppit.com')
    headers.update({'Referer':link,'Content-Type': 'application/x-www-form-urlencoded','Accept-Encoding': 'gzip, deflate','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    rr = requests.post(link,data=body,headers=headers)
    soup = BeautifulSoup(rr.text,'html.parser')
    print 'uppit soup',len(soup)
    l = soup('a',{'class':'m-btn big blue'})[0].get('href')
    print len(l),l
    url = urllib.quote(l,':/')
    return url

def seenupload(link,ref=None):
    main_url = 'http://seenupload.com/seenupload.html'
    s = requests.Session()

    r = s.get(link,headers=headers,verify=False,allow_redirects=True)
    #headers.update({'Cookie': r.headers['set-cookie']})

    soup = BeautifulSoup(r.text)
    #print len(soup)
    fname= soup('input',{'name': 'fname'})[0].get('value')
    #print fname
    id = link.split('/')
    id = id[-1].replace('.html','')
    body = dict(method_free=' ',op="download1",usr_login='',id=id,fname=fname,referer='')
    s.headers.update({'Referer':main_url,'Accept-Encoding': 'gzip, deflate','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    rr = s.post(main_url,data=body,headers=headers)
    soup = BeautifulSoup(rr.text,'html.parser')
    print 'seenupload soup',len(soup)
    ran_value= soup('input',{'name': 'rand'})[0].get('value')
    print ran_value
    if ran_value:
        body = dict(op="download2",id=id,down_direct='1',rand=ran_value,referer=ref)
        rrr = s.post(main_url,data=body,headers=headers,verify=False)
        soup = BeautifulSoup(rrr.text,'html.parser')
        l = soup(href=re.compile('http://88'))
        print l
        for i in l:
            url = urllib.quote(i.get('href'))
            url = url.replace('%3A',':')
            print 'playing:seenupload:',url
        return url


def makeRequest(url,referer=None,post=None,body={},mobile=False):
    if mobile:
        headers.update({'User-Agent' : 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'})
        #req = urllib2.Request(url,None,headers)
                #('Referer','http://doridro.com/forum/ucp.php?mode=login')]
    if referer:
        headers.update=({'Referer':referer})
    if post:
        r = requests.post(url,data=body,headers=headers,verify=False)
        return r.text
    else:
        print 'makeRequest set cookies'
        #net.set_cookies(cookie_jar)
        req = urllib2.Request(url) # dont add header here, otherwise login cookies won't sent.
        req.add_headers = [('Host','doridro.com'),
                    ('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'),
                    ('Accept-Encoding','gzip, deflate'),
                    ('Accept','text/html, application/xhtml+xml, */*'),
                    ('Content-Type','application/x-www-form-urlencoded')]

        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data
'''def cache(url, duration=0,post=None,other_head='',body={},ref=None,getcookie=None,need_cookie=None,save_cookie=None,build_soup=None,debug=False,repeat=1,mobile='',content_type=''):
    UAhead=dict({'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:32.0) Gecko/20100101 Firefox/32.0'})
    headers=dict({'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:32.0) Gecko/20100101 Firefox/32.0'})
    print 'caching url ___ for ___',url,str(duration)

    #if addon.getSetting('nocache') == 'true':
    #    duration = 0
    new = 'true'
    #url = url.encode('utf-8')  DONOT DONOT ENCODE
    if mobile:
        #if len(mobile) >5 :
        #    headers.update({'User-Agent': mobile})
        #else:
        if mobile == "Android":
            headers.update({'User-Agent': Android_UA})
            UAhead.update({'User-Agent': Android_UA})
        else:
            headers.update({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A405 Safari/8536.25'})
            UAhead.update({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A405 Safari/8536.25'})

    if other_head :
        import ast

        other_head = ast.literal_eval(other_head)
        headers2 ={}
        headers2= dict(merge_2_dict(UAhead,other_head))
        headers = headers2
    if ref:
        headers.update({'Referer': '%s'%ref})
    #else:
    #    headers.update({'Referer': '%s'%url})
    if len(body) > 1:
        f_name_posturl = url + json.dumps(body)
        cacheFile = os.path.join(cacheDir,''.join(c for c in unicode(f_name_posturl, 'utf-8') if c not in '/\\:?"*|<>')[:150].strip())
    else:
        cacheFile = os.path.join(cacheDir,''.join(c for c in unicode(url.encode('utf-8'), 'utf-8') if c not in '/\\:?"*|<>')[:150].strip())
    if need_cookie:
        cookie_jar = os.path.join(cookie_file, '%s' %need_cookie) #need cookie is cookie file name that had
        if xbmcvfs.exists(cookie_jar):                                                        # had saved befor
            with open( cookie_jar, "rb") as f:
                cookiess = pickle.load(f)
        else:
            cookiess = need_cookie
            # if xbmcvfs.exists(xbmc.translatePath(DL_DonorPath))
    #if xbmcvfs.exists(cacheFile): #and duration!=0 and (time.time()-os.path.getmtime(cacheFile) < 60*60*24*duration):
     #  print 'getting from Caaaaaaaaaaaache duration' , str(duration)

    #for i in range(repeat): # if range is 1 loop through once #
    #if xbmcvfs.exists(os.path.join(cacheDir,cacheFile)):
     #   print get_file_age(duration,cacheFile)
    if os.path.isfile(cacheFile) and duration!=0  and  (time.time()-os.path.getmtime(cacheFile) < 60*60*24*duration) and addon.getSetting('disableallcache') == 'false':
        print 'getting from Cache duration:There are no new content' #, str(get_file_age(duration,cacheFile))
        fh = xbmcvfs.File(cacheFile, 'r')
        content = fh.read()
        fh.close()
        new = 'false'
        return content,new
    elif post and need_cookie:

        r = requests.post(url,data=body,cookies=cookiess,headers=headers,verify=False)
    elif post:

        r = requests.post(url,data=body,headers=headers,verify=False)
    elif need_cookie:
        r = requests.get(url,cookies=cookiess,headers=headers,verify=False)

    else:
        #print headers
        r = requests.get(url,headers=headers,verify=False)

    #if not r.raise_for_status() :
    try:
        #if r.headers['Content-Type'] == 'application/json':
        #    print 'Json type content found'
        #    content = r.json()
        #else:
            content = r.text
    except Exception:
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print 'debug for the url:%s' %url
        print 'status_code:',r.status_code
        print 'Response Headers server sent::',r.headers
        print 'Header sent to server:',r.request.headers
        print 'The cookies are:',r.headers['set-cookie']
        print '========================================================='
        return None
    if duration != 0:
        fh = xbmcvfs.File(os.path.join(cacheDir,cacheFile), 'w')
        fh.write(str(removeNonAscii(content))) #problem to save ilive : add str
        fh.close()
    if save_cookie:
        #print r
        Cookie =  r.cookies.get_dict()      #str(r.headers['set-cookie'])
        if len(Cookie) < 1:
            print 'Saving cookie failed, see debug below'
            debug = True
        print 'saving cookies for iiiiiiiiiiiiiii',Cookie
            #notification('Login Succes','Succesfully loged_in to doridro.Com as %s ::.'%Doridro_USER,2000)
            #return r.cookies
        cookie_jar = os.path.join(cookie_file, '%s' %save_cookie)
        with open( cookie_jar, "wb" ) as ff:
            pickle.dump( Cookie, ff )
            ff.close()
        new = Cookie
    if debug:
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print 'debug for the url:%s' %url
        print 'status_code:',r.status_code
        print 'Response Headers server sent::',r.headers
        print 'Header sent to server:',r.request.headers
        print 'The cookies are:',r.headers['set-cookie']
        print '========================================================='
    if build_soup:
        content = get_soup('',content)
    if getcookie:
        new = r.headers['set-cookie']
    return content,new'''
def cache(url, duration=0,ref=None,post=None,body={},need_cookie=None):
    if addon.getSetting('nocache') == 'true':
        duration = 0
    new = 'true'
    #url = url.encode('utf-8')
    if len(body) > 1:
        f_name_posturl = url + json.dumps(body)
        cacheFile = os.path.join(cacheDir,''.join(c for c in unicode(f_name_posturl.encode('utf-8','ignore'), 'utf-8') if c not in '/\\:?"*|<>')[:150].strip())
    else:
        cacheFile = os.path.join(cacheDir,''.join(c for c in unicode(url.encode('utf-8'), 'utf-8') if c not in '/\\:?"*|<>')[:150].strip())
    if need_cookie:
        #getcookiefile = os.path.join(cookie_jar, '%s' %need_cookie)
        with open( cookie_jar, "rb") as f:
            cookiess = pickle.load(f)
    if ref:
        headers.update({'Referer': '%s'%ref})
    if os.path.exists(cacheFile) and duration!=0 and (time.time()-os.path.getmtime(cacheFile) < 60*60*24*duration):
        fh = xbmcvfs.File(cacheFile, 'r')
        content = fh.read()
        fh.close()
        new = 'false'
        return content,new
    elif post and need_cookie:

        r = requests.post(url,data=body,cookies=cookiess,headers=headers,verify=False)
        content = r.text
    elif post:

        r = requests.post(url,data=body,headers=headers,verify=False)
        content = r.text
    elif need_cookie:
        r = requests.get(url,cookies=cookiess,headers=headers,verify=False)
        content =r.text

    else:
        #print headers
        r = requests.get(url,headers=headers,verify=False)
        content =r.text

    fh = xbmcvfs.File(cacheFile, 'w')
    fh.write(removeNonAscii(content).encode('utf-8'))
    fh.close()
    return content,new
def indishare(url): #limit of 120 minutes/day
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Extracting Idishare Link ......', 'Pleas wait:  ...' )
    id = url.split('/')
    id = id[-1]
    content,new = cache(url, duration=1) #cache(url, duration=0,post=None,body={},need_login=None)
    soup = get_soup('',content=content)
    WAIT_PAT = r'>(\d+)</span> seconds<'
    match = re.search(WAIT_PAT,content)
    if match:
        wait_for = match.group(1)
        pDialog.create('Extracting Idishare Link ......', 'Pleas wait for %s:  ...' %wait_for )
        xbmc.sleep(int(wait_for)*1000)
    #id="countdown_str">Wait.*?>(\d+).*?seconds
    print 'indishare soup',len(soup)
    ran_value= soup('input',{'name': 'rand'})[0].get('value')

    body = dict(op="download2",id=id,rand=ran_value,down_script='1')
    content,new = cache(url,1,post = 'post',body=body)

    href = re.compile(r'<a\s*href="(http://[\w]+\.indi(?:file|world)s\.com[^">]+)',re.DOTALL).findall(content)[0]
    #print len(href),href
    pDialog.close()
    return href.replace(' ','%20')
def uptobox(url): #limit of 120 minutes/day # Not every link uptostream
    content,new = cache(url,duration=0.5)
    #url2 = url.replace('uptobox','uptostream')
    print len(content)
    form_values = {}
    for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)">', content):
        form_values[i.group(1)] = i.group(2)
    headers.update({'Referer':url})
    WAIT_PAT = r'>(\d+)</span> seconds<'
    content = requests.post(url,data=form_values,headers=headers)
    streamurl = re.compile(r'''DOWNLOAD\s*BUTTON.*?(https?://\w+\.uptobox\.com/d/.*?)">''',re.DOTALL).findall(content.text)[0]

    print 'playing:uptobox:',streamurl
    #streamurl = urllib.quote_plus(streamurl)
    return streamurl.replace(' ','%20')

def notification(header="", message="", sleep=3000):
    """ Will display a notification dialog with the specified header and message,
    in addition you can set the length of time it displays in milliseconds and a icon image.
    """
    xbmc.executebuiltin("XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ))
def addDir(name,url,mode,iconimage,date):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name , "Year": date, "Genre": date} )
    ok=xbmcplugin.addDirectoryItem(handle,url=u,listitem=liz,isFolder=True)
    return ok
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param
params=get_params()

url=None
name=None
mode=None
iconimage=None

try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        start=urllib.unquote_plus(params["start"])
except:
        pass
try:
        ch_fanart=urllib.unquote_plus(params["ch_fanart"])
except:
        pass


if mode==None:
        #_login()
        CATEGORIES(name)
        xbmcplugin.endOfDirectory(handle)
elif mode==1:
    LiveBanglaTV(url)
    xbmcplugin.endOfDirectory(handle)

elif mode==2:
    playlive(url,name)      
elif mode==3:
    print ('gettting Natok')
    natok(url)
    xbmcplugin.endOfDirectory(handle)
elif mode==4:
    print ('gettting musiclinks')
    getVideolinks(name,url,'music')
elif mode==5:
    print ('gettting videolinks')
    getVideolinks(name,url)
    #xbmcplugin.endOfDirectory(handle)
elif mode==7:
    print ('playin')
    morelinks(name,url)    
#elif mode==106:
#    print ('gettting Movies')
#    BMovies(url)
#    xbmcplugin.endOfDirectory(handle)
elif mode==99:
    print ('gettting Dramaserials')
    Dramaserials(url)
    xbmcplugin.endOfDirectory(handle)
elif mode==6:
    print ('gettting multiplelinks')
    getmultiplelinks(url)
    xbmcplugin.endOfDirectory(handle)



