# -*- coding: utf-8 -*-
import sys, os, re, json, urllib, time 
import xbmc,xbmcgui,xbmcplugin

from resources.lib.sources.source_three.webpage_crawler import WebCrawler
from resources.lib.sources.source_three import mode_update

base_url_ = sys.argv[0]                                                             
addon_handle = int(sys.argv[1])
args = sys.argv[2]
mode = None


# update modelist 
mode_update.data_keysJson(2)
pageDialog = xbmcgui.DialogProgress()

#icon image, pathDict, homeDir and jsonPath file
path_dicts, path_dict, mode_alot_list, file_update = (mode_update.load_keys()[0],
                                                               mode_update.load_keys(1, 'alot_path'),
                                                               mode_update.load_homeDir('alothome'),
                                                               mode_update.data_keysJson(key='alothome', arg=1),
                                                               )
cat_url, cat_attr = mode_update.fetch_url(obj=WebCrawler, key_data='data_alot',key_home='alothome',
                                          url_pattern='a',attr_pattern='.*/(c.{8}s)/'
                                          )

def url_link(m_part, num):

    params = {}

    if m_part.endswith('.com/'):

        if num <= 1: initial_url = m_part

        elif num > 1: initial_url = m_part + '?from=' + str(num)

    elif m_part.endswith('/search/'):

        if num <= 1:

            name = mode_update.search_query(); params['q'] = name
                
            mode_update.readWrite_search(arg_str = '-'.join(name.lower().split()), write=True)
                
            initial_url = m_part, params

        elif num > 1:

            name = m_part + mode_update.readWrite_search() + '/?from_videos='  + str(num)

            initial_url = name
    else:

        if num <= 1: initial_url = m_part

        elif num > 1: initial_url = m_part + '?from=' + str(num)

    return initial_url

def fetch_links(m_part, min_search = 1, max_search = 2):
    
    pageDialog.create('Kodi', 'Fetching Playable Links...')

    page_number = min_search
    f_url = url_link(m_part, page_number)

    if len(f_url) == 2: 

        page_download = WebCrawler(f_url[0], payload=f_url[1])
                    
    elif len(f_url) != 2:

        page_download = WebCrawler(f_url)
                    
    pageDialog.update(25, 'Fetching Playable Links...')
    movie_src = page_download.playable_links_tup(
                                                  selector_list = '.item a',

                                                  search_pattern = '\s+-\s',
                                                  replace_string = '',
                                                  element = 'h1',

                                                  img_selector = 'meta[property="og:image"]',
                                                  img_attr_single = 'content',

                                                  attr_list = 'href',
                                                    
                                                  sieve_str = True,
                                                  sieve_pattern = '"contentUrl":\s+"(.*?\.mp4)/'
                                                  )
    pageDialog.update(100, 'Fetch Completed: Wrting Playable Links To Screen...')
    time.sleep(5)# sleep for 5 seconds to update progress report before return
          
    return movie_src,page_number + 1

def play_movie(key, min_ = 1, max_ = 2):
    """Update add_dir object."""

    sources, page_num  = fetch_links(path_dict[key][0], min_, max_)
    
    if len(sources) > 0:
        
        for link in sources:

            add_dir("", "",
                    url=link[0],
                    name = link[1],
                    iconimage=path_dict[key][1],
                    fanart=link[2],
                    info = link[3]
                    )
            
        add_dir("folder", "next_page" + '_' + key + '_'+ str(page_num), '',
                '[B][COLOR darkgoldenrod]Next Page [/COLOR][/B]' + '( '+ str(page_num) + ' )'
                ,path_dict[key][1], path_dict[key][1],info=None)
    else:

        add_dir("folder", "No Stream Found: Check Source Code", '',
                '[B][COLOR darkgoldenrod]End of Page [/COLOR][/B]',
                path_dict[key][1], path_dict[key][1],info=None)

def add_dir(dir_type, mode, url, name, iconimage, fanart,info):

    base_url = base_url_
    base_url += "?url="          +urllib.quote_plus(url.encode('utf8'))
    base_url += "&mode="         +str(mode)
    base_url += "&name="         +urllib.quote_plus(name.encode('utf8'))
    base_url += "&fanart="       +urllib.quote_plus(fanart)

    listitem = xbmcgui.ListItem(name, iconImage=iconimage,
                                thumbnailImage=fanart)
    
    listitem.setInfo(type="Video", infoLabels=info)
    listitem.setProperty("Fanart_Image", fanart)
    
    if dir_type == 'folder':

        link = xbmcplugin.addDirectoryItem(
                                            handle=addon_handle, 
                                            url=base_url, 
                                            listitem = listitem, 
                                            isFolder=True
                                           )
    else:
        
        link = xbmcplugin.addDirectoryItem(
                                           handle=addon_handle, 
                                           url=url,
                                           listitem = listitem,
                                           isFolder=False
                                           )
    return link

def menu():
    """Create folders in kodi."""

    for item in mode_alot_list:

        key = item[0]
        inner_name = item[1]

        add_dir("folder", key, '',
            '[B][COLOR silver]'+inner_name+'[/COLOR][/B]',
            path_dicts["icon_image"], path_dicts["icon_image"],info=None)
   
if re.compile(r"mode=(\w+)?&").search(args):

    mode = re.compile(r"mode=(\w+)?&").search(args).group(1)

    if mode in path_dict:
            
        key_mode = mode

        play_movie(key_mode)

    elif not mode in path_dict:
        
        pass

if re.compile(r"(next_page)\w+?&").search(args):

    mode = re.compile(r"(next_page)\w+?&").search(args).group(1)
    src  = re.compile(r"(next_page)\w+?&").search(args).group()

    if mode   == "next_page":

        if src.split("_")[2] in path_dict:

            play_movie(
                       src.split("_")[2],
                       min_ = int(src.replace("&"," ").split("_")[3]),
                       max_ = int(src.replace("&","").split("_")[3]) + 1
                    )

if re.compile(r"mode=(\w+)?&").search(args):

    mode = re.compile(r"mode=(\w+)?&").search(args).group(1)
    
    if mode   == "alotcat" : mode_update.cat_name(func=add_dir, obj=WebCrawler, url=cat_url, filePath=file_update,selector='.item',
                                              attr='href', attr_option = cat_attr, title = 'title', img = 'src', group_dict = 'True'
                                             )




