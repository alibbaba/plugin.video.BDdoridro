# uppit is possible post then play
import platform
print 'platform.python_version()',platform.python_version()
import sys
import xbmcgui
import xbmcplugin,xbmcvfs
import xbmcaddon,xbmc,os
import urllib
import urllib2,requests
import re
import settings
import time

try:
    import json
except:
    import simplejson as json
from urllib import FancyURLopener
from bs4 import BeautifulSoup
import httplib2
import cPickle as pickle
headers=dict({'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:32.0) Gecko/20100101 Firefox/32.0'})

addonID = 'plugin.video.BDdoridro'
addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
addon = xbmcaddon.Addon(id='plugin.video.BDdoridro')
handle = int(sys.argv[1])
logopath = os.path.join( addonUserDataFolder, 'logos')
cacheDir = os.path.join( addonUserDataFolder, 'cache')
clean_cache=os.path.join(cacheDir,'cleancacheafter1month')
logos = None
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
cookie_jar = settings.cookie_jar()
Doridro_USER = settings.doridro_user()
Doridro_PASSWORD = settings.doridro_pass()
#http://www.moviesfair24.com/category/natok-telefilm-bangla/
if not cacheDir.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')) and not os.path.isdir(cacheDir)== 1 :
    os.mkdir(cacheDir)


if not logopath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')) and not os.path.isdir(logopath)== 1 :
    os.mkdir(logopath)
if xbmcvfs.exists(clean_cache):
    if int(time.time()-os.path.getmtime(clean_cache)) >  300 :#300 is 1 month      #60*60*24*30):
        print 'time of creation of ff',str(time.time()-os.path.getmtime(clean_cache))
        import shutil
        shutil.rmtree(cacheDir)
        shutil.rmtree(logopath)
        #notification("Cache Cleared","old cache cleared")
        os.mkdir(logopath)
        os.mkdir(cacheDir)
else:
    with open(clean_cache,'w') as f:
        f.write('')
h = httplib2.Http(cacheDir)

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
        results = json.loads(data)
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
                        th= urllib.urlretrieve(thumb_url,l) # to download the file

                        return l
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

def _login():
    if os.path.exists(cookie_jar) and (time.time()-os.path.getmtime(cookie_jar) < 60*60*24) and os.path.getsize(cookie_jar) > 5:
        notification('Already Logged IN','Logged In to doridro.Com as %s ::.'%Doridro_USER,2000)
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
    addDir("Natok & Telefilms", 'http://doridro.com/forum/viewforum.php?f=155',155,'','')
    addDir("Bangla Movies", 'http://doridro.com/forum/viewforum.php?f=106',106,'','')
    addDir("Live TV", 'http://www.jagobd.com/category/bangla-tv',1,'','')
    #addDir("Drama Serials", 'http://doridro.com/forum/viewforum.php?f=99',99,'','')

    #addDir("Music", 'http://doridro.com/forum/viewforum.php?f=166',99,'','')



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
    content,new = cache(url,duration=3)
    soup = get_soup('',content=content)
    embed_url=soup('div', {'class':"stremb"})[0]('a')[0].get('href')
    #embed_url=soup('area', {'shape':"rect"}).get('href')
    print 'the embed_url',embed_url
    if addon.getSetting('typeofstream') == 0:
        final_url = 'http://' + livetv(embed_url,ref=url)
    else:
        final_url = livetv(embed_url,ref=url)
    #play_url = makeRequest(final_url,mobile=True,ref=url)
    if not final_url == 'None':
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo(type='Video', infoLabels={'Title':name})
        xbmc.Player().play(final_url,listitem)
def livetv(embed_url,ref=None):
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
                play_url = rtmp + ' timeout=15 token=%xqdrde(nKa@#. live=1 playpath=' + playpath +' swfUrl='+swfurl+' pageurl='+embed_url

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
    #l=soup('script', {'type':'text/javascript'})
    ##l= soup('a' ,target=re.compile('ifra'))
    #print l
    #for data in l:
    #    if 'SWFObject' in data.text:
    #        #print data.text
    #        m = re.compile(r'''SWFObject[\(',"]+(.*?)[\(',"]+.*?[\(',"]+file[\(',"]+(.*?)[\(',"]+.*?'streamer[\(',"]+(.*?)[\(',"]+''',re.DOTALL).findall(data.text)
    #        print m
    #        if  not m[0][2] == 'None' :
    #            rtmp = m[0][2].encode('utf-8')
    #            playpath = m[0][1].encode('utf-8')
    #            swfurl = m[0][0].encode('utf-8')
    #            play_url = rtmp + ' timeout=15 token=%bedcsd(nKa@#. flashVer=WIN\\2015,0,0,167 live=1 playpath=' + playpath +' swfUrl='+swfurl+' pageurl='+embed_url
    #
    #            return play_url
    #        else:
    #            return None


def BMovies(url):
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Getting Bangla Movies', 'Wait While getting info ...')
        #pDialog.close()
        content,new = cache(url, duration=2)
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
                try:

                    if os.path.isfile(thumb_from_folderjpg):
                        thumb_from_folder = thumb_from_folderjpg
                        #print 'thumb found from folder'

                    elif os.path.isfile(thumb_from_folderpng):
                        thumb_from_folder = thumb_from_folderpng

                    else:
                        #print ('getting image from folder using google image search')
                        thumb_from_folder = google_image(name)
                except:
                    print 'No image'
                    thumb_from_folder = ''
            else:
                thumb_from_folder = ''
            count += 1
            pDialog.update(int(count*1.6), 'Downloading: %s  ...' %name)

            liz=xbmcgui.ListItem(name)
            liz.setInfo( type="Video", infoLabels={ "Title": name})
            liz.setMimeType('mkv')
            liz.setArt({ 'thumb': thumb_from_folder, 'fanart' : thumb_from_folder })
            liz.setIconImage(thumb_from_folder)
            #print 'name to pass to videolinks', name
            u = sys.argv[0] + '?mode=5' + '&url=' + urllib.quote_plus(url)\
                + '&name=' + urllib.quote_plus(name)
            #print u
            xbmcplugin.addDirectoryItem(handle, u, liz, True)

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def natok(url):
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Getting Natok', 'Downloading Natok with image ...')
        #pDialog.close()
        content,new = cache(url, duration=2)
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
                try:

                    if os.path.isfile(thumb_from_folderjpg):
                        thumb_from_folder = thumb_from_folderjpg
                        #print 'thumb found from folder'

                    elif os.path.isfile(thumb_from_folderpng):
                        thumb_from_folder = thumb_from_folderpng

                    else:
                        #print ('getting image from folder using google image search')
                        thumb_from_folder = google_image(name)
                except:
                    print 'No image'
            else:
                thumb_from_folder = ''
            count += 1
            pDialog.update(int(count*1.6), 'Downloading: %s  ...' %name)

            liz=xbmcgui.ListItem(name)
            liz.setInfo( type="Video", infoLabels={ "Title": name})
            liz.setMimeType('mkv')
            liz.setArt({ 'thumb': thumb_from_folder, 'fanart' : thumb_from_folder })
            liz.setIconImage(thumb_from_folder)
            #print 'name to pass to videolinks', name
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
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Getting Videos link', 'Please wait ...')
    content,new = cache(url,duration=3,need_cookie='login')
    l = re.compile(r'''a\s*class="postlink"\s*href="([^"]+)''',re.DOTALL).findall(content)
    #soup = BeautifulSoup(content,'html.parser')
    #l = soup('a',{'class': 'postlink'})
    print len(l)
    print l
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    domains = ['seenupload','uptobox','share.jong.li','indishare','uppit','bdupload']
    final_url = []
    if len(l) >0:
        for link in l:
            #link = href.get('href')
            print link
            if any (s in link for s in domains):
                #link = href
                #if 'arabload' in link:
                #    print 'NOOOOOOOOO Arabload support'
                #    continue
                if 'jong' in link:
                    extracted_url = jongli(link,ref=url)
                elif 'indishare' in link or 'bdupload' in link:
                    extracted_url = indishare(link)
                elif 'uptobox' in link:
                    extracted_url = uptobox(link)
                elif 'seenupload' in link:
                    extracted_url = seenupload(link,url)
                elif 'uppit' in link:
                    extracted_url = uppit(link,url)
                if extracted_url:
                    final_url.append(extracted_url)
                    break

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

    else:
        notification("NO Link found", "[COLOR yellow]There is no video for this link[/COLOR]", sleep=1000)
def jongli(link,ref=None):
    soup = get_soup(link,ref=url)
    #print soup
    l= soup('a',{'href': True})[0].get('href')
    #print len(l),l
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

def cache(url, duration=0,post=None,body={},need_cookie=None):
    if addon.getSetting('nocache') == 'true':
        duration = 0
    new = 'true'
    url = url.encode('utf-8')
    if len(body) > 1:
        f_name_posturl = url + json.dumps(body)
        cacheFile = os.path.join(cacheDir, (''.join(c for c in unicode(f_name_posturl, 'utf-8') if c not in '/\\:?"*|<>')).strip())
    else:
        cacheFile = os.path.join(cacheDir, (''.join(c for c in unicode(url, 'utf-8') if c not in '/\\:?"*|<>')).strip())
    if need_cookie:
        #getcookiefile = os.path.join(cookie_jar, '%s' %need_cookie)
        with open( cookie_jar, "rb") as f:
            cookiess = pickle.load(f)
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
    id = url.split('/')
    id = id[-1]
    content,new = cache(url, duration=1) #cache(url, duration=0,post=None,body={},need_login=None)
    soup = get_soup('',content=content)
    print 'indishare soup',len(soup)
    ran_value= soup('input',{'name': 'rand'})[0].get('value')

    print ran_value
    body = dict(op="download2",id=id,rand=ran_value,down_script='1')
    if new =='true' :

        #soup = get_soup(url)

        pDialog = xbmcgui.DialogProgress()

        if 'bdupload' in url:
            pDialog.create('Bdupload', 'Need to wait 15s ...')
            xbmc.sleep(15000)
            q= '''http://.*?\.indifiles\.com'''
        else:
            pDialog.create('Indishare', 'Need to wait 10s ...')
            xbmc.sleep(5000)
            q= '''http://.*?\.indiworlds\.com'''
        pDialog.close()
    content,new = cache(url,1,'post',body)
    #r = requests.post(url,data=body,headers=headers,verify=False)
    #print r.request.headers
    #resp, content = h.request(url, "POST", body=urllib.urlencode(data))
    if 'bdupload' in url:
        q= '''http://.*?\.indifiles\.com'''
    else:
        q= '''http://.*?\.indiworlds\.com'''
    soup = get_soup('',content=content)


    #soup = BeautifulSoup(content)
    href = urllib.quote(soup(href=re.compile(q))[0].get('href'),':/')
    print len(href),href
    return href
def uptobox(url): #limit of 120 minutes/day # Not every link uptostream
    content,new = cache(url,duration=1)
    #url2 = url.replace('uptobox','uptostream')
    print len(content)
    form_values = {}
    for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)">', content):
        form_values[i.group(1)] = i.group(2)
    #resp, content = h.request(url,"POST",headers=headers,body=form_values)   #print l
    headers.update({'Referer':url})
    content = requests.post(url,data=form_values,headers=headers)
    streamurl = re.compile('''align="center">.*?<a\s*href="([^"]+)"''',re.DOTALL).findall(content.text)[0]

    print 'playing:uptobox:',streamurl
    streamurl = urllib.quote(streamurl)

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
        _login()
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
    print ('gettting videolinks')
    getVideolinks(name,url)
    #xbmcplugin.endOfDirectory(handle)
elif mode==7:
    print ('playin')
    morelinks(name,url)
elif mode==1:
    LiveBanglaTV(url)
    xbmcplugin.endOfDirectory(handle)

elif mode==2:
    playlive(url,name)
