# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Addon: First 
# Author: "Kokobarasi"

# -*- coding: utf-8 -*-
import sys, re, urllib, os
import xbmc, xbmcgui, xbmcplugin, xbmcaddon


#=======global variables setting paths==================================
addon_handle = int(sys.argv[1])
home  = xbmc.translatePath('special://home/')
#=======================================================================
path_dicts = {
            "icon_image":"DefaultMovies.png",       
}

#=======================================================================
def add_dir(dir_type, mode, url, name, iconimage, fanart):

    base_url = sys.argv[0]
    base_url += "?url="          +urllib.quote_plus(url.encode('utf8'))
    base_url += "&mode="         +str(mode)
    base_url += "&name="         +urllib.quote_plus(name.encode('utf8'))
    base_url += "&fanart="       +urllib.quote_plus(fanart)

    listitem = xbmcgui.ListItem(name, iconImage=iconimage,
                                thumbnailImage=fanart)
    
    listitem.setInfo( type="Video", infoLabels={ "Title": name })
    
    listitem.setProperty("Fanart_Image", fanart)

    if url == "": 
        link = xbmcplugin.addDirectoryItem(handle=addon_handle, 
                                            url=base_url, 
                                            listitem = listitem, 
                                            isFolder=True)
    else:
        link = xbmcplugin.addDirectoryItem(handle=addon_handle, 
                                           url=url, listitem = listitem)
#============================================================================

#========================================================================
mode = None
args = sys.argv[2]

if re.compile(r"mode=(\w+)?&").search(args):

    mode = re.compile(r"mode=(\w+)?&").search(args).group(1)

#========================================================================
# if mode is None, call main menu function and create folder structures
if mode == None:                 menu()
xbmcplugin.endOfDirectory(addon_handle)
#-----------------------------------------------------------------------        
