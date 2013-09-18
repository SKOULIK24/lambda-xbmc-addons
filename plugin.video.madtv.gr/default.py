# -*- coding: utf-8 -*-

'''
    mad player XBMC Addon
    Copyright (C) 2013 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,threading,xbmc,xbmcplugin,xbmcgui,xbmcaddon
from operator import itemgetter
try:	import CommonFunctions
except:	import commonfunctionsdummy as CommonFunctions
try:	import StorageServer
except:	import storageserverdummy as StorageServer


language			= xbmcaddon.Addon().getLocalizedString
setSetting			= xbmcaddon.Addon().setSetting
getSetting			= xbmcaddon.Addon().getSetting
addonName			= xbmcaddon.Addon().getAddonInfo("name")
addonVersion		= xbmcaddon.Addon().getAddonInfo("version")
addonId				= xbmcaddon.Addon().getAddonInfo("id")
addonPath			= xbmcaddon.Addon().getAddonInfo("path")
addonDesc			= language(30450).encode("utf-8")
addonIcon			= os.path.join(addonPath,'icon.png')
addonFanart			= os.path.join(addonPath,'fanart.jpg')
addonArt			= os.path.join(addonPath,'resources/art')
dataPath			= xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData			= os.path.join(dataPath,'views.cfg')
favData				= os.path.join(dataPath,'favourites2.cfg')
cache				= StorageServer.StorageServer(addonName+addonVersion,24).cacheFunction
cache2				= StorageServer.StorageServer(addonName+addonVersion,240).cacheFunction
common				= CommonFunctions


class main:
    def __init__(self):
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:	value = splitparam[1].encode("utf-8")
                except:	value = splitparam[1]
                params[key] = value

        try:		action = urllib.unquote_plus(params["action"])
        except:		action = None
        try:		name = urllib.unquote_plus(params["name"])
        except:		name = None
        try:		show = urllib.unquote_plus(params["show"])
        except:		show = None
        try:		type = urllib.unquote_plus(params["type"])
        except:		type = None
        try:		url = urllib.unquote_plus(params["url"])
        except:		url = None
        try:		image = urllib.unquote_plus(params["image"])
        except:		image = None

        if action == None:							categories().get()
        elif action == 'item_play':					contextMenu().item_play()
        elif action == 'item_random_play':			contextMenu().item_random_play()
        elif action == 'item_queue':				contextMenu().item_queue()
        elif action == 'item_play_from_here':		contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':				contextMenu().favourite_add(name, url, image)
        elif action == 'favourite_delete':			contextMenu().favourite_delete(name, url, image)
        elif action == 'favourite_moveUp':			contextMenu().favourite_moveUp(name, url, image)
        elif action == 'favourite_moveDown':		contextMenu().favourite_moveDown(name, url, image)
        elif action == 'playlist_start':			contextMenu().playlist_start()
        elif action == 'playlist_open':				contextMenu().playlist_open()
        elif action == 'settings_open':				contextMenu().settings_open()
        elif action == 'global_view':				contextMenu().global_view()
        elif action == 'favourites':				favourites().get()
        elif action == 'channels':					channels().get()
        elif action == 'madtv_shows':				shows().madtv()
        elif action == 'madtvgreekz_shows':			shows().madtvgreekz()
        elif action == 'madtv_charts':				charts().get()
        elif action == 'episodes':					episodes().get(show, url)
        elif action == 'episodes_recent':			episodes().madtv_recent()
        elif action == 'episodes_songs':			charts().songs(url, type, image)
        elif action == 'live':						player().live(name)
        elif action == 'play':						player().run(url)

        viewDict = {
            'skin.confluence'	: 503,	'skin.aeon.nox'		: 518,	'skin.back-row'			: 529,
            'skin.bello'		: 50,	'skin.carmichael'	: 50,	'skin.diffuse'			: 55,
            'skin.droid'		: 50,	'skin.metropolis'	: 55,	'skin.pm3-hd'			: 58,
            'skin.rapier'		: 68,	'skin.re-touched'	: 550,	'skin.simplicity'		: 50,
            'skin.transparency'	: 51,	'skin.xeebo'		: 50,	'skin.xperience1080'	: 50
            }

        xbmcplugin.setContent(int(sys.argv[1]), 'Episodes')
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        index().container_view(viewDict)
        return

class getUrl(object):
    def __init__(self, url, fetch=True, mobile=False, proxy=None, post=None, referer=None, cookie=None):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if not cookie is None:
            from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
            import cookielib
            cj = cookielib.CookieJar()
            opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
            cookiereq = Request(cookie)
            response = opener.open(cookiereq)
            response.close()
            for cookie in cj:
                cookie = '%s=%s' % (cookie.name, cookie.value)
            request.add_header('Cookie', cookie)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer is None:
            request.add_header('Referer', referer)
        response = urllib2.urlopen(request, timeout=10)
        if fetch == True:
            result = response.read()
        else:
            result = response.geturl()
        response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class index:
    def infoDialog(self, str, header=addonName):
        xbmc.executebuiltin("Notification(%s,%s, 3000)" % (header, str))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName):
        answer = xbmcgui.Dialog().yesno(header, str1, str2)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin("Container.Refresh")

    def container_data(self):
        if not os.path.exists(dataPath):
            os.makedirs(dataPath)
        if not os.path.isfile(favData):
            file = open(favData, 'w')
            file.write('')
            file.close()
        if not os.path.isfile(viewData):
            file = open(viewData, 'w')
            file.write('')
            file.close()

    def container_view(self, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = open(viewData,'r')
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"(.+?)"' % (skin)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def favList(self, favList):
        total = len(favList)
        for i in favList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=episodes&show=%s&url=%s' % (sys.argv[0], sysname, sysurl)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def catList(self, catList):
        total = len(catList)
        for i in catList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                if action.startswith('episodes'):
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def chartList(self, chartList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        total = len(chartList)
        for i in chartList:
            try:
                name, url, type, image = i['name'], i['url'], i['type'], i['image']
                sysname, sysurl, systype, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(type), urllib.quote_plus(image)
                u = '%s?action=episodes_songs&url=%s&type=%s&image=%s' % (sys.argv[0], sysurl, systype, sysimage)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def channelList(self, channelList):
        total = len(channelList)
        for i in channelList:
            try:
                name = i['name']
                image = '%s/%s.png' % (addonArt, name)
                sysname = urllib.quote_plus(name)
                u = '%s?action=live&name=%s' % (sys.argv[0], sysname)

                cm = []
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Duration": "1440", "Plot": addonDesc } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Video", "true" )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

    def showList(self, showList):
        file = open(favData,'r')
        favRead = file.read()
        file.close()

        total = len(showList)
        for i in showList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=episodes&show=%s&url=%s' % (sys.argv[0], sysname, sysurl)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if not url in favRead:
                    cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                else:
                    cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        total = len(episodeList)
        for i in episodeList:
            try:
                name, show, url, image = i['name'], i['show'], i['url'], i['image']
                sysurl = urllib.quote_plus(url)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=playlist_start)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=global_view)' % (sys.argv[0])))
                #cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": show, "Plot": addonDesc } )
                item.setProperty("IsPlayable", "true")
                item.setProperty( "Video", "true" )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def item_play_from_here(self, url):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        total = xbmc.getInfoLabel('Container.NumItems')
        for i in range(0, int(total)):
            name = xbmc.getInfoLabel('ListItemNoWrap(%s).Label' % str(i))
            if name == '': break
            show = xbmc.getInfoLabel('ListItemNoWrap(%s).TVShowTitle' % str(i))
            image = xbmc.getInfoLabel('ListItemNoWrap(%s).Icon' % str(i))
            url = xbmc.getInfoLabel('ListItemNoWrap(%s).FileNameAndPath' % str(i))
            url = url.split('?url=')[-1].split('&url=')[-1]
            sysurl = urllib.quote_plus(url)
            u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)
            item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "TVShowTitle": show, "Plot": addonDesc } )
            item.setProperty("IsPlayable", "true")
            item.setProperty( "Video", "true" )
            item.setProperty("Fanart_Image", addonFanart)
            playlist.add(u, item)
        xbmc.Player().play(playlist)

    def playlist_start(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def global_view(self):
        try:
            skin = xbmc.getSkinDir()
            try:
                xml = xbmc.translatePath('special://xbmc/addons/%s/addon.xml' % (skin))
                file = open(xml,'r')
            except:
                xml = xbmc.translatePath('special://home/addons/%s/addon.xml' % (skin))
                file = open(xml,'r')
            read = file.read().replace('\n','')
            file.close()
            src = os.path.dirname(xml) + '/'
            try:
                src += re.compile('defaultresolution="(.+?)"').findall(read)[0] + '/'
            except:
                src += re.compile('<res.+?folder="(.+?)"').findall(read)[0] + '/'
            src += 'MyVideoNav.xml'
            file = open(src,'r')
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label is None): break
            file = open(viewData, 'r')
            read = file.read()
            file.close()
            file = open(viewData, 'w')
            for line in re.compile('(".+?\n)').findall(read):
                if not line.startswith('"%s"|"' % (skin)): file.write(line)
            file.write('"%s"|"%s"\n' % (skin, str(view)))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, name, url, image):
        try:
            index().container_refresh()
            file = open(favData, 'a+')
            file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"))
        except:
            return

    def favourite_delete(self, name, url, image):
        try:
            index().container_refresh()
            file = open(favData,'r')
            read = file.read()
            file.close()
            read = read.replace('"%s"|"%s"|"%s"' % (name, url, image),'')
            file = open(favData, 'w')
            for line in re.compile('(".+?\n)').findall(read):
                file.write(line)
            file.close()
            index().infoDialog(language(30304).encode("utf-8"))
        except:
            return

    def favourite_moveUp(self, name, url, image):
        try:
            index().container_refresh()
            list = []
            file = open(favData,'r')
            read = file.read()
            file.close()
            for line in re.compile('(".+?)\n').findall(read):
                list.append(line)
            i = list.index('"%s"|"%s"|"%s"' % (name, url, image))
            if i == 0 : return
            list[i], list[i-1] = list[i-1], list[i]
            file = open(favData, 'w')
            for line in list:
                file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"))
        except:
            return

    def favourite_moveDown(self, name, url, image):
        try:
            index().container_refresh()
            list = []
            file = open(favData,'r')
            read = file.read()
            file.close()
            for line in re.compile('(".+?)\n').findall(read):
                list.append(line)
            i = list.index('"%s"|"%s"|"%s"' % (name, url, image))
            if i+1 == len(list): return
            list[i], list[i+1] = list[i+1], list[i]
            file = open(favData, 'w')
            for line in list:
                file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"))
        except:
            return

class favourites:
    def get(self):
        favList = []
        file = open(favData, 'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            favList.append({'name': name, 'url': url, 'image': image})
        index().favList(favList)

class categories:
    def get(self):
        catList = []
        catList.append({'name': 30501, 'image': 'Favourites.png', 'action': 'favourites'})
        catList.append({'name': 30502, 'image': 'Live.png', 'action': 'channels'})
        catList.append({'name': 30503, 'image': 'Charts.png', 'action': 'madtv_charts'})
        catList.append({'name': 30504, 'image': 'MAD TV.png', 'action': 'madtv_shows'})
        catList.append({'name': 30505, 'image': 'MAD Greekz.png', 'action': 'madtvgreekz_shows'})
        catList.append({'name': 30506, 'image': 'Recent.png', 'action': 'episodes_recent'})
        index().catList(catList)

class channels:
    def __init__(self):
        self.list = []

    def get(self):
        self.list.append({'name': 'MAD TV'})
        self.list.append({'name': 'MAD RADIO'})
        index().channelList(self.list)

class charts:
    def __init__(self):
        self.list = []
        self.data = []
        self.chartUrl				= 'http://www.mad.tv/data/chart.php?service=chart&chid='
        self.oldchartUrl			= 'http://www.mad.tv/data/chart.php?service=oldchart&chdt='
        self.youtube_searchUrl		= 'http://gdata.youtube.com/feeds/api/videos?q='

    def get(self):
        #self.list = self.chart_list()
        self.list = cache(self.chart_list)
        index().chartList(self.list)

    def songs(self, url, type, image):
        self.list = self.songs_list(url, type, image)
        index().episodeList(self.list)

    def chart_list(self):
        try:
            try: import json
            except: import simplejson as json
            charts = ['MAD Top 50','US Chart','UK Chart','iTunes GR Chart','iTunes US Chart',
					 'iTunes UK Chart','WIND Plus top 10']
            result = getUrl(self.chartUrl + 'NaN').result
            result = '{' + result.split('{', 1)[1].rsplit('}', 1)[0] + '}'
            result = json.loads(result)
            result = result['chartmenu']
            self.data = [i for i in result if i['item'] in charts]

            threads = []
            for i in range(0, len(self.data)):
                url = self.data[i]['link']
                url = self.chartUrl + url.split("=")[-1]
                self.data[i]['link'] = url
                threads.append(Thread(self.chart_list2, url, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            for i in range(0, len(self.data)):
                item = self.data[i]['item']
                url = self.data[i]['link']
                image = '%s/%s.png' % (addonArt, item)
                result = self.data[i]['data']
                result = '{' + result.split('{', 1)[1].rsplit('}', 1)[0] + '}'
                result = json.loads(result)
                From = result['chart']['from']
                From = From.replace('/','.').strip()
                To = result['chart']['to']
                To = To.replace('/','.').strip()
                name = '%s // %s - %s' % (item, From, To)
                oldFrom = result['oldcharts'][:3][-1]
                oldFrom = oldFrom['dts'].split("-")[0]
                oldFrom = oldFrom.replace('/','.').strip()
                oldTo = result['chart']['to']
                oldTo = oldTo.replace('/','.').strip()
                oldname = '%s // %s - %s' % (item, oldFrom, oldTo)
                self.list.append({'name': name, 'url': url, 'type': 'week', 'image': image})
                self.list.append({'name': oldname, 'url': url, 'type': 'month', 'image': image})
        except:
            return

        return self.list

    def chart_list2(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i]['data'] = result
        except:
            return

    def songs_list(self, url, type, image):
        try:
            try: import json
            except: import simplejson as json
            result = getUrl(url).result
            result = '{' + result.split('{', 1)[1].rsplit('}', 1)[0] + '}'
            result = json.loads(result)
            songs = result['chart']['songs']

            if type == 'month':
                oldcharts = result['oldcharts']
                if len(str(oldcharts[0]['id'])) == 4:
                    songs = []
                    oldcharts = oldcharts[:4]
                    baseUrl = self.chartUrl
                else:
                    oldcharts = oldcharts[:3]
                    baseUrl = self.oldchartUrl

                threads = []
                for oldchart in oldcharts:
                    url = '%s%s' % (baseUrl, str(oldchart['id']))
                    threads.append(Thread(self.songs_list2, url))
                [i.start() for i in threads]
                [i.join() for i in threads]

                for data in self.data:
                    result = '{' + data.split('{', 1)[1].rsplit('}', 1)[0] + '}'
                    result = json.loads(result)
                    songs += result['chart']['songs']
        except:
            return

        for song in songs:
            try:
                name = '%s - %s' % (song['artist'].strip(), song['title'].strip())
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                show = song['artist'].strip()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')
                query = name.replace('=','').replace('&','').replace("'",'')
                url = self.youtube_searchUrl + query + ' official'
                url = common.replaceHTMLCodes(url)
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        if type == 'month':
            list = [x for i,x in enumerate(self.list) if x not in self.list[i+1:]]
            self.list = sorted(list, key=itemgetter('name'))
        else:
            for i in range(0, len(self.list)):
                self.list[i]['name'] = '%s. ' % str(i+1) + self.list[i]['name']

        return self.list

    def songs_list2(self, url):
        try:
            result = getUrl(url).result
            self.data.append(result)
        except:
            return

class shows:
    def __init__(self):
        self.list = []
        self.data = ''
        self.youtubeUrl				= 'http://gdata.youtube.com'
        self.youtube_showsUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.youtube_episodeUrl		= 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.youtube_recentUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/uploads'
        self.youtube_searchUrl		= 'http://gdata.youtube.com/feeds/api/videos?q='

    def madtv(self):
        channel =	'MADTVGREECE'
        filters =	["PL1RY_6CEqdtn1LWczvuHCfZ6KcCqsW4dl", #�ost Popular
					"PL1RY_6CEqdtnxJYgudDydiG4fKVoQouHf", #XmadWish #ote
					"PL1RY_6CEqdtlu30q6SyuNe6Tk5IYjAiks", #MoMad
					"PLE4B3F6B7F753D97C", #Mad Act Now
					"PL85C952EA930B9E90", #Mad TV Specials
					"PL46B9D152167BA727"] #MADGreek�
        #self.list = self.youtube_list(channel)
        self.list = cache(self.youtube_list, channel)
        filter = [i for i in self.list if not i['url'].split("/")[-1] in filters]
        index().showList(filter)

    def madtvgreekz(self):
        channel =	'madtvgreekz'
        filters =	["PL20iPi-qHKiyZGlOs5DTElzAK_YNCDJn0"] #Fun!
        #self.list = self.youtube_list(channel)
        self.list = cache(self.youtube_list, channel)
        filter = [i for i in self.list if not i['url'].split("/")[-1] in filters]
        index().showList(filter)

    def youtube_list(self, channel):
        try:
            threads = []
            for i in range(1, 250, 25):
                showsUrl = self.youtube_showsUrl % channel + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.youtube_list2, showsUrl))
            [i.start() for i in threads]
            [i.join() for i in threads]
            result = self.data
            shows = common.parseDOM(result, "entry")
        except:
            return
        for show in shows:
            try:
                name = common.parseDOM(show, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "id")[0]
                url = self.youtube_episodeUrl % url.split("/")[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = image.encode('utf-8')
                if image.endswith("/00000000000/0.jpg"): continue #empty playlist
                self.list.append({'name': name, 'channel': channel, 'url': url, 'image': image})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def youtube_list2(self, url):
        try:
            result = getUrl(url).result
            self.data += result
        except:
            return

class episodes:
    def __init__(self):
        self.list = []
        self.data = []
        self.youtubeUrl				= 'http://gdata.youtube.com'
        self.youtube_showsUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.youtube_episodeUrl		= 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.youtube_recentUrl		= 'http://gdata.youtube.com/feeds/api/users/%s/uploads'
        self.youtube_searchUrl		= 'http://gdata.youtube.com/feeds/api/videos?q='

    def get(self, show, url):
        self.list = self.youtube_list(show, url)
        index().episodeList(self.list)

    def madtv_recent(self):
        channel = 'MADTVGREECE'
        self.list = self.youtube_list('MAD TV', self.youtube_recentUrl % channel)
        index().episodeList(self.list[:100])

    def youtube_list(self, show, url):
        try:
            if not url.startswith(self.youtube_searchUrl):
                threads = []
                result = ""
                for i in range(1, 250, 25):
                    for x in range(1, 25): self.data.append('')
                    episodesUrl = url + '?max-results=25&start-index=%s' % str(i)
                    threads.append(Thread(self.youtube_list2, episodesUrl, i))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
                episodes = common.parseDOM(result, "entry")
            else:
                url = url.decode('iso-8859-7').encode('utf-8')
                params = url.split("?")[-1]
                params = dict(arg.split("=") for arg in params.split("&"))
                query = params["q"]
                match = urllib.quote_plus(query).replace('%','').replace('+','')
                url = url.replace(query, urllib.quote_plus(query))
                threads = []
                result = ""
                for i in range(1, 250, 25):
                    for x in range(1, 25): self.data.append('')
                    episodesUrl = url + '&max-results=25&start-index=%s' % str(i)
                    threads.append(Thread(self.youtube_list2, episodesUrl, i))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
                episodes = []
                filter = common.parseDOM(result, "entry")
                for episode in filter:
                    name = common.parseDOM(episode, "title")[0]
                    name = urllib.quote_plus(name.encode('utf-8')).replace('%','').replace('+','')
                    if match in name: episodes.append(episode)
        except:
            return
        for episode in episodes:
            try:
                name = common.parseDOM(episode, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "media:player", ret="url")[0]
                url = url.split("&amp;")[0].split("=")[-1]
                url = 'http://www.youtube.com/watch?v=%s' % url
                url = url.encode('utf-8')
                image = common.parseDOM(episode, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'show': show, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def youtube_list2(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class player:
    def __init__(self):
        self.youtube_searchUrl		= 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtubeUrl				= 'http://www.youtube.com'

    def run(self, url):
        if url.startswith(self.youtube_searchUrl):
            url = self.youtube_search(url)
        elif url.startswith(self.youtubeUrl):
            url = self.youtube(url)

        if url is None: return
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def live(self, channel):
        channelDict = {
            'MAD TV'			:	[{'type': 'youtubelive', 'url': 'http://www.youtube.com/user/MADTVGREECE/', 'type2': 'False', 'url2': 'False'}],
            'MAD RADIO'			:	[{'type': 'youtubelive', 'url': 'http://www.youtube.com/user/1062madradio/', 'type2': 'False', 'url2': 'False'}]
        }

        playerDict = {
            ''					:	self.direct,
            'youtube'			:	self.youtube,
            'youtubelive'		:	self.youtubelive
        }

        i = channelDict[channel][0]
        type, url, type2, url2 = i['type'], i['url'], i['type2'], i['url2']
        url = playerDict[type](url)
        if url is None and not type2 == "False": url = playerDict[type2](url2)
        if url is None: return

        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        return url

    def direct(self, url):
        return url

    def youtube_search(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
                return
            params = url.split("?")[-1]
            params = dict(arg.split("=") for arg in params.split("&"))
            query = params["q"]
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url).result
            result = common.parseDOM(result, "entry")[0]
            url = common.parseDOM(result, "id")[0]
            url = url.split("/")[-1]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
                return
            url = url.split("?v=")[-1]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

    def youtubelive(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
                return
            url += '/videos?view=2&flow=grid'
            result = getUrl(url).result
            url = re.compile('"/watch[?]v=(.+?)"').findall(result)[0]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

main()