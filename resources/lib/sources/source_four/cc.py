# -*- coding: utf-8 -*-
import sys, os, re, json, urllib 
import xbmc,xbmcgui,xbmcplugin

from resources.lib.sources.source_three.webpage_crawler import (WebCrawler)
from resources.lib.sources.source_three import (number)

base_url_ = sys.argv[0]                                                             
addon_handle = int(sys.argv[1])
args = sys.argv[2]
mode = None

keys_path = 'addons' + '/' + re.search('://(.*)/', base_url_).group(1) + '/' + 'resources' + '/' + 'lib' + '/' + 'modules' + '/' + 'keys' + '/' 

dict_keys   = os.path.join(xbmc.translatePath('special://home/'), keys_path + "keys_cc.json")
mode_key  = os.path.join(xbmc.translatePath('special://home/'), keys_path + "modelist.json")

def load_keys():

        with open(dict_keys) as fjson:

                content = json.load(fjson)

                return content

def mode_keys():
    '''Return json object as python list object.'''
    with open(mode_key) as fjson:

        content = json.load(fjson)

        return content

path_dicts, mode_cc_list = mode_keys()[0], mode_keys()[number.assign_num(number.mode_keys, 'cchome')]
path_dict = load_keys()

def url_link(m_path, num):

    if num <= 1 and m_path.endswith('/'): initial_url = m_path

    elif num > 1 and m_path.endswith('/'): 

        initial_url = m_path + 'page' + str(num) + '.html'

    else: 

        if num <= 1: initial_url = m_path

        elif num > 1: initial_url = m_path + 'page' + str(num) + '.html'

    return initial_url

def fetch_links(m_part, min_search = 1, max_search = 2):
    
    page_number = min_search

    f_url = url_link(m_part, page_number)

    page_download = WebCrawler(f_url)

    movie_src = page_download.playable_links_tup(selector_list = '.col .item-inner-col a',

                                             search_pattern = '(\s+-\s+)',
                                             replace_string = '',
                                             element = 'title',

                                             img_selector = 'video',
                                             img_attr_single = 'poster',

                                             attr_option = 'video'
                                             )

    return movie_src,page_number+1

def video_links(url_list):
    """Return playable link, title and image source."""

    sources = [] 
    
    for link in url_list:

        html = SiteCrawler(link[0])
        
        sources.append((
                        html.fetch_single('video source', 'src'),
                        link[1],
                        html.fetch_single('video', 'poster'),
                       {
                        'title': link[1],        
                       }

                      ))

    return sources

def play_movie(key, min_ = 1, max_ = 2):
    """Update add_dir object."""

    sources, page_num  = fetch_links(path_dict[key][0], min_, max_)
    if not sources == []:
        for link in sources:
            add_dir("", "",
                    url=link[0],
                    name = link[1],
                    iconimage=path_dict[key][1],
                    fanart=link[2],
                    info = link[3]
                    )
        add_dir("folder", "next_page" + '_' + key + '_'+ str(page_num),
                '', '[B][COLOR darkgoldenrod]Next Page [/COLOR][/B]' + '( '+ str(page_num) + ' )'
                ,path_dict[key][1], path_dict[key][1],info=None)
    else:
        add_dir("folder", "end_page", '',
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
    
    listitem.setInfo( type="Video", infoLabels=info)
    
    listitem.setProperty("Fanart_Image", fanart)
    
    if url == "": 
        link = xbmcplugin.addDirectoryItem(handle=addon_handle, 
                                            url=base_url, 
                                            listitem = listitem, 
                                           isFolder=True)
    else:
        link = xbmcplugin.addDirectoryItem(handle=addon_handle, 
                                           url=url, listitem = listitem)

def menu():
    """Create folders in kodi."""

    for item in mode_cc_list:

        key = item[0]
        inner_name = item[1]

        add_dir("folder", key, '',
            '[B][COLOR silver]'+inner_name+'[/COLOR][/B]',
            path_dicts["icon_image"], path_dicts["icon_image"],info=None)


def cat_site():
    """""" 
    page_download = WebCrawler('https://adult-movies.cc/channels/')

    cat_dict = page_download.fetch_list(selector='.item--channel .inner-col a',
                                   attr='href',
                                   title = 'title',
                                   img='src',
                                   attr_option = 'channels',
                                   group_dict=True
                                    )
    
    k_update = page_download.UpdateKey(dict_keys)
    k_update.update_dict(cat_dict)

    return cat_dict
        
def site_cat(arg):
    """""" 
    
    name_dict = arg()
    title = [(name, ' '.join(name.split('_')).title()) 
             for name in list(name_dict.keys())]

    for elem in sorted(title):

        try:

            add_dir("folder", elem[0], '',
                '[B][COLOR orange]'+ elem[1] +'[/COLOR][/B]',
                name_dict[elem[0]][1],
                name_dict[elem[0]][1],info=None)

        except (UnicodeEncodeError,KeyError) as e:

            continue

def name_site(): 
    """""" 
    page_download = WebCrawler('https://adult-movies.cc/pornstars/')

    cat_dict = page_download.fetch_list(selector='.item--pornstar .inner-col a',
                                   attr='href',
                                   title = 'title',
                                   img='src',
                                   attr_option = 'pornstars',
                                   group_dict=True
                                    )
    
    k_update = page_download.UpdateKey(dict_keys)
    k_update.update_dict(cat_dict)

    return cat_dict
    
    
def site_name(arg):
    """""" 
    name_dict = arg()
    title = [(name, ' '.join(name.split('_')).title()) 
             for name in list(name_dict.keys())]

    for elem in sorted(title):

        try:

            add_dir("folder", elem[0], '',
                '[B][COLOR orange]'+ elem[1] +'[/COLOR][/B]',
                name_dict[elem[0]][1],
                name_dict[elem[0]][1],info=None)

        except (UnicodeEncodeError,KeyError) as e:

            continue
      
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

    if   mode   == "cccat":     site_cat(cat_site)
    elif mode   == "cc_name":   site_name(name_site)
