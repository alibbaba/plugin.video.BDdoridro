# uppit is possible post then play

import sys
import xbmcgui
import xbmcplugin
import xbmcaddon,xbmc,os
import urllib
import urllib2,requests
import re
import settings
import time
import simplejson
from urllib import FancyURLopener
from bs4 import BeautifulSoup,SoupStrainer
import httplib2
headers=dict({'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:32.0) Gecko/20100101 Firefox/32.0'})

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net = Net()  
addonID = 'plugin.video.BDdoridro'
addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
addon = xbmcaddon.Addon(id='plugin.video.BDdoridro') 
handle = int(sys.argv[1])
ADDON = settings.addon()
logopath = os.path.join( addonUserDataFolder, 'logos')
cacheDir = os.path.join( addonUserDataFolder, 'cache')
logos = None
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
cookie_jar = settings.cookie_jar()
Doridro_USER = settings.doridro_user()
Doridro_PASSWORD = settings.doridro_pass()
#http://www.moviesfair24.com/category/natok-telefilm-bangla/
if not cacheDir.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')) and not os.path.isdir(cacheDir)== 1:
    os.mkdir(cacheDir)
h = httplib2.Http(cacheDir)

xbmcplugin.setContent(handle, 'movies')
def ensure_dir():
    print 'creating dir'
    d = logopath
    print d
    if not os.path.isdir(d)== 1:
        print ' Nor logos exist 0creating one dir'
        os.mkdir(d)
        
def get_soup(url,ref=None,parse_type=None):
    if ref:
        headers.update({'Referer': '%s'%ref})
    else:
        headers.update({'Referer': '%s'%url})
    
    resp, content = h.request(url, "GET",headers=headers)
    try:
        soup = BeautifulSoup(content,'html.parser')
        print 'using html.parser'
    except:
        soup = BeautifulSoup(content)

    
    print len(soup)    
    
    return soup        
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

def google_image(title):
    #ensure_dir()
    searchTerm = title

    # Replace spaces ' ' in search term for '%20' in order to comply with request
    searchTerm = urllib.quote(searchTerm)
    # Start FancyURLopener with defined version 
    myopener = MyOpener()

    # Set count to 0
    count= 0

    for i in range(0,1):
        # Notice that the start changes for each iteration in order to request a new set of images for each loop as_filetype=png as_sitesearch=photobucket.com rsz=4 
        url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP&as_sitesearch=http://doridro.com/forum/')
        print url
        res, data = h.request(url,"GET",headers=headers)
        if not res.status == 200 :
            print 'No image found for :%s' %title
            return
        results = simplejson.loads(data)
        data = results['responseData']['results']
        t_results = results['responseData']['cursor']['estimatedResultCount']
        print t_results
        thum_list = []
        if not t_results == None:
            #print myUrl['unescapedUrl']
            for i in range(2):
                try:
                    
                    thumb_url= data[i]['unescapedUrl']
                    file_ext = ['jpg','jpeg','png','JPG','JPEG']
                    if any(x in thumb_url for x in file_ext):
                        print thumb_url
                        url_ext = thumb_url.rsplit('.',1)
                        print url_ext
                        title = title.encode('utf-8')
                        print title
                        #l=os.path.join(logopath, title  + str(count)+'.JPG')
                        l=os.path.join(logopath, title  +'.'+url_ext[1])
                        print l
                        #f = open(l,'wb')
                        #thum_list.append(thumb_url)
                        #th= urllib2.urlopen(thumb_url).read() # to download the file but 0 byte file come up
                        th= urllib.urlretrieve(thumb_url,l) # to download the file
                        
                        print th
                        return l
                    else:
                        count = count + 1
                        continue
                    
                    #f.write(th)
                    #f.close
                #print th
            # Sleep for one second to prevent IP blocking from Google
            #return th
                except Exception: pass
        else:
            print ('ignoring this title image : %s' %title)
    #return th
def login():
    login_url='http://doridro.com/forum/ucp.php?mode=login' #%sid

    req = urllib2.Request(login_url)
    payload = {'username' : '%s' %Doridro_USER,
            'password' : '%s' %Doridro_PASSWORD,
            'autologin' : '1',
            #'sid' : ('%s' %sid),
            #'redirect' : 'index.php',
            'login' : 'login'
        }
    
    # Use urllib to encode the payload
    data = urllib.urlencode(payload)   
    net.set_cookies(cookie_jar)
    # Build our Request object (supplying 'data' makes it a POST)
    req = urllib2.Request(login_url, data) 
    resp = urllib2.urlopen(req)
    net.save_cookies(cookie_jar)
    contents = resp.read()
    resp.close()
def get_soup(url,ref=None,parse_type=None):
    if ref:
        headers.update({'Referer': '%s'%ref})
    else:
        headers.update({'Referer': '%s'%url})
    
    resp, content = h.request(url, "GET",headers=headers)
    try:
        soup = BeautifulSoup(content,'html.parser')
        print 'using html.parser'
    except:
        soup = BeautifulSoup(content)

    
    print len(soup)    
    
    return soup
def CATEGORIES(name):
    addDir("Natok & Telefilms", 'http://doridro.com/forum/viewforum.php?f=155',155,'','')
    addDir("Bangla Movies", 'http://doridro.com/forum/viewforum.php?f=106',106,'','')
    addDir("Live TV", 'http://www.jagobd.com/list/bangla.php',1,'','')
    #addDir("Drama Serials", 'http://doridro.com/forum/viewforum.php?f=99',99,'','')
    
    #addDir("Music", 'http://doridro.com/forum/viewforum.php?f=166',99,'','')
    
    
    
def LiveBanglaTV(url):
    soup = get_soup(url)
    l= soup('a' ,{'rel':"bookmark"})
    print len(l)
    for data in l:
        name = data.get('title')
        url = data.get('href')
        #print url
        img = data('img')[0]['src']
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
    soup = get_soup(url)
    embed_url=soup('div', {'class':"stremb"})[0]('a')[0].get('href')
    final_url = livetv(embed_url,ref=url)
    if not final_url == 'None':
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo(type='Video', infoLabels={'Title':name})
        xbmc.Player().play(final_url,listitem)
       
def livetv(embed_url,ref=None):
    soup = get_soup(embed_url,ref)
    l=soup('script', {'type':'text/javascript'})
    #l= soup('a' ,target=re.compile('ifra'))
    print len(l)
    for data in l:
        if 'SWFObject' in data.text:
            #print data.text
            m = re.compile(r'''SWFObject[\(',"]+(.*?)[\(',"]+.*?[\(',"]+file[\(',"]+(.*?)[\(',"]+.*?'streamer[\(',"]+(.*?)[\(',"]+''',re.DOTALL).findall(data.text)
            print m
            if  not m[0][2] == 'None' :
                rtmp = m[0][2].encode('utf-8')
                playpath = m[0][1].encode('utf-8')
                swfurl = m[0][0].encode('utf-8')
                play_url = rtmp + ' timeout=15 token=%xrdrwq(nKa@#. live=1 playpath=' + playpath +' swfUrl='+swfurl+' pageurl='+embed_url

                return play_url
            else:
                return None
    
            
    
def BMovies(url):
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Getting Natok', 'Downloading Natok with image ...')
        net.set_cookies(cookie_jar)
        req = urllib2.Request(url)
        req.add_headers = [('Host','doridro.com'),
                    ('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'),
                    ('Accept-Encoding','gzip, deflate'),
                    ('Accept','text/html, application/xhtml+xml, */*'),
                    ('Content-Type','application/x-www-form-urlencoded')]
                    #('Referer','http://doridro.com/forum/ucp.php?mode=login')]
        resp = urllib2.urlopen(req)
        content = resp.read()
        resp.close()
        soup = BeautifulSoup(content,'html.parser')
        l = soup('a' ,{'class':'topictitle'})[8:70]
        print len(l)
        match=[] 
        count = 0
        for i in l:
            href = i.get('href')
            name = i.text
            tab= href.replace('&amp;','&').replace('./','')
            url= 'http://doridro.com/forum/' + tab
            thumb_from_folderjpg = os.path.join(logopath,name+'.JPG')
            thumb_from_folderpng = os.path.join(logopath,name+'.png')
            try:
                
                if os.path.isfile(thumb_from_folderjpg):
                    thumb_from_folder = thumb_from_folderjpg
                    print 'thumb found from folder'
                
                elif os.path.isfile(thumb_from_folderpng):
                    thumb_from_folder = thumb_from_folderpng
                    
                else:
                    print ('getting image from folder using google image search')
                    thumb_from_folder = google_image(name)                
            except:
                print 'No image'
            pDialog.update(int(count*1.6), 'Downloading: %s  ...' %name)
            count += 1
            liz=xbmcgui.ListItem(name)
            liz.setInfo( type="Video", infoLabels={ "Title": name})
            liz.setArt({ 'thumb': thumb_from_folder, 'fanart' : thumb_from_folder })
            liz.setIconImage(thumb_from_folder)
            u = sys.argv[0] + '?mode=5' + '&url=' + urllib.quote_plus(url)\
                + '&name=' + urllib.quote_plus(name)
            #print u
            xbmcplugin.addDirectoryItem(handle, u, liz, True)    
    
    
def natok(url):
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Getting Natok', 'Downloading Natok with image ...')
        #pDialog.close()
        net.set_cookies(cookie_jar)
        req = urllib2.Request(url)
        req.add_headers = [('Host','doridro.com'),
                    ('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'),
                    ('Accept-Encoding','gzip, deflate'),
                    ('Accept','text/html, application/xhtml+xml, */*'),
                    ('Content-Type','application/x-www-form-urlencoded')]
                    #('Referer','http://doridro.com/forum/ucp.php?mode=login')]
        resp = urllib2.urlopen(req)
        content = resp.read()
        resp.close()
        soup = BeautifulSoup(content,'html.parser')
        l = soup('a' ,{'class':'topictitle'})[8:70]
        print len(l)
        match=[] 
        count = 0
        for i in l:
            href = i.get('href')
            name = i.text
            tab= href.replace('&amp;','&').replace('./','')
            url= 'http://doridro.com/forum/' + tab
            thumb_from_folderjpg = os.path.join(logopath,name+'.JPG')
            thumb_from_folderpng = os.path.join(logopath,name+'.png')
            try:
                
                if os.path.isfile(thumb_from_folderjpg):
                    thumb_from_folder = thumb_from_folderjpg
                    print 'thumb found from folder'
                
                elif os.path.isfile(thumb_from_folderpng):
                    thumb_from_folder = thumb_from_folderpng
                    
                else:
                    print ('getting image from folder using google image search')
                    thumb_from_folder = google_image(name)                
            except:
                print 'No image'
            count += 1
            pDialog.update(int(count*1.6), 'Downloading: %s  ...' %name)
            
            liz=xbmcgui.ListItem(name)
            liz.setInfo( type="Video", infoLabels={ "Title": name})
            liz.setMimeType('mkv')
            liz.setArt({ 'thumb': thumb_from_folder, 'fanart' : thumb_from_folder })
            liz.setIconImage(thumb_from_folder)
            print 'name to pass to videolinks', name
            u = sys.argv[0] + '?mode=5' + '&url=' + urllib.quote_plus(url)\
                + '&name=' + urllib.quote_plus(name)
            #print u
            xbmcplugin.addDirectoryItem(handle, u, liz, True)
        
        #xbmcplugin.endOfDirectory(handle)

            #xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True )
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
    print 'getVideolinks name',name
    print ('Building videolinks')
    print url
    net.set_cookies(cookie_jar)
    req = urllib2.Request(url)
    req.add_headers = [('Host','doridro.com'),
                ('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'),
                ('Accept-Encoding','gzip, deflate'),
                ('Accept','text/html, application/xhtml+xml, */*'),
                ('Content-Type','application/x-www-form-urlencoded')]
                #('Referer','http://doridro.com/forum/ucp.php?mode=login')]
    resp = urllib2.urlopen(req)
    contents = resp.read()
    resp.close()
    soup = BeautifulSoup(contents,'html.parser')
    l = soup('a',{'class': 'postlink'})
    print len(l)
    print l
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    domains = ['seenupload','uptobox','share.jong.li','indishare','uppit']
    final_url = []
    if len(l) >0:
        for href in l:
            link = href.get('href')
            print link
            if any (s in link for s in domains):
            
                #if 'arabload' in link:
                #    print 'NOOOOOOOOO Arabload support'
                #    continue
                if 'jong' in link:
                    extracted_url = jongli(link,ref=url)
                elif 'indishare' in link:
                    extracted_url = indishare(link)
                elif 'uptobox' in link:
                    extracted_url = uptobox(link)
                elif 'seenupload' in link:
                    extracted_url = seenupload(link,url)
                elif 'uppit' in link:
                    extracted_url = uppit(link,url)
                if extracted_url:
                    final_url.append(extracted_url)
            
            else:
                continue            
        print 'final_url',final_url
        if len(final_url) >0:
            for stream in final_url:
                if not 'rar' in stream:
                    info = xbmcgui.ListItem('%s' %name)
                    playlist.add(stream, info)
            xbmc.Player().play(playlist)
        else:
            notification("failed to Play", "[COLOR yellow]Failed to extract video links[/COLOR]", sleep=1000)
            #xbmc.Player().play(final_url)
            #xbmc.sleep(1000)
            #if int(sys.argv[1]) < 0:
            #    
            #    xbmc.Player().play(final_url)
            #    xbmc.sleep(300)
           # if  xbmc.Player().isPlaying() :
            #    print 'stop playinnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnngg'
             #   break

                #xbmc.Player().stop()                
                #item = xbmcgui.ListItem(path=final_url)
                #print 'now doing set resolved',item
                #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
                
    else:
        notification("NO Link found", "[COLOR yellow]There is no video for this link[/COLOR]", sleep=1000)
def jongli(link,ref=None):
    soup = get_soup(link,ref=url)
    #print soup
    l= soup('a',{'href': True})[0].get('href')
    print len(l),l
    return l
    #if l:
        #xbmc.Player().play(l)
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
def indishare(url): #limit of 120 minutes/day
    id = url.split('/')
    id = id[-1]
    soup = get_soup(url)
    print 'indishare soup',len(soup)
    ran_value= soup('input',{'name': 'rand'})[0].get('value') 
    #print 'indishare soup::l::',len(l)

    #for i in l:
    #    ran_value = i.get('value')
    print ran_value
    body = dict(op="download2",id=id,rand=ran_value,down_script='1')
    r = requests.post(url,data=body,headers=headers,verify=False)
    print r.request.headers
    #resp, content = h.request(url, "POST", body=urllib.urlencode(data))
    content = r.text
    soup = BeautifulSoup(content,'html.parser')
    l = soup(href=re.compile('http://server'))
    print l
    for i in l:
        url = urllib.quote(i.get('href'))
        url = url.replace('%3A',':')
        print 'playing:indishare:',url
    return url
def uptobox(url):
    url2 = url.replace('uptobox','uptostream')
    soup = get_soup(url2,ref=url)
    l= soup('source',{'src': True})
    #print l
    for i in l:
        #print i
        url = i.get('src')
        print 'playing:uptobox:',url
    return url

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
        login() 
        CATEGORIES(name)
        xbmcplugin.endOfDirectory(handle)
elif mode==155:
    print ('gettting Natok')
    natok(url)
    xbmcplugin.endOfDirectory(handle)
elif mode==106:
    print ('gettting Movies')
    BMovies(url)
    xbmcplugin.endOfDirectory(handle)
elif mode==99:
    print ('gettting Dramaserials')
    Dramaserials(url)
    xbmcplugin.endOfDirectory(handle)
elif mode==6:
    print ('gettting multiplelinks')
    getmultiplelinks(url)
    xbmcplugin.endOfDirectory(handle)
    
elif mode==5:
    print ('gettting videolinkssssssssssss')
    getVideolinks(name,url)
    #xbmcplugin.endOfDirectory(handle)    
elif mode==7:
    print ('playinnnnnnnnnnnnnnngggggggggg')
    morelinks(name,url)
elif mode==1:
    print ('LiveBanglaTV')
    LiveBanglaTV(url)
    xbmcplugin.endOfDirectory(handle)

elif mode==2:
    print ('LiveBanglaTV')
    playlive(url,name)
   