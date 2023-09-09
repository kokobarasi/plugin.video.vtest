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
search_path_hq = 'addons' + '/' + re.search('://(.*)/', base_url_).group(1) + '/' + 'resources' + '/' + 'lib' + '/' + 'sources' + '/' + 'source_three' + '/'

dict_keys   = os.path.join(xbmc.translatePath('special://home/'), keys_path + "keys_hq.json")
mode_key  = os.path.join(xbmc.translatePath('special://home/'), keys_path + "modelist.json")
search_file_hq = os.path.join(xbmc.translatePath('special://home/'), search_path_hq + "mysearch.txt")

def load_keys():

        with open(dict_keys) as fjson:

                content = json.load(fjson)

                return content

def mode_keys():
    '''Return json object as python list object.'''
    with open(mode_key) as fjson:

        content = json.load(fjson)

        return content

path_dicts, mode_hq_list = mode_keys()[0], mode_keys()[number.assign_num(number.mode_keys, 'hqhome')]
path_dict = load_keys()

def hq_entry():
    """Open dialog and wait for user input."""

    user_str = ''
    
    keyboard = xbmc.Keyboard(user_str, 'Enter Search Term')
    keyboard.doModal()

    if keyboard.isConfirmed():
        
        entry  = keyboard.getText().lower()

        return entry
    
    else:
        
        return

def readWrite_hq(arg_str = None, write=False):
    """Return saved content to memory."""

    if arg_str and write:

        with open(search_file_hq,'w') as file_handle:
        
            file_handle.write(arg_str)


    elif not arg_str and not write:

        with open(search_file_hq, 'r') as fh:
            
            content = fh.read()
            
            return content


def url_link(m_part, num):

    params = {}

    if m_part.endswith('.com/') and not '/search/' in m_part:

        if num <= 1:

            initial_url = m_part

        elif num > 1:

            nitial_url = m_part + '?from=' + str(num)
  
    elif not m_part.endswith('.com/') and not 'search' in m_part:
        
        if num <= 1:

            initial_url = m_part

        elif num > 1:

            nitial_url = m_part + '?from=' + str(num)

    elif  m_part.endswith('/search/') and num <= 1:

        name = hq_entry()

        params['q'] = name

        readWrite_hq(arg_str = '-'.join(name.title().split()), write=True)

        initial_url = m_part, params

    elif m_part.endswith('/search/') and num > 1:
        
        name = m_part + readWrite_hq() + '/' + '?from=' + str(num)

        initial_url = name
    
    else:
        
        initial_url = m_part

    return initial_url

def fetch_links(m_part, min_search = 1, max_search = 2):
    
    page_number = min_search

    f_url = url_link(m_part, page_number)

    if len(f_url) == 2: 

            page_download = WebCrawler(f_url[0], payload=f_url[1])
            
    elif len(f_url) != 2:

            page_download = WebCrawler(f_url)

    movie_src = page_download.playable_links_tup(
                                 selector_list = '.item a',

                                 search_pattern = '\s+-\s',
                                 replace_string = '',
                                 element = 'h1',

                                 img_selector = 'meta[property="og:image"]',
                                 img_attr_single = 'content',


                                 attr_option =  '/videos/',

                                            
                                 sieve_str = True,
                                 sieve_pattern = "video_url:\s+'(.*?\.mp4)"
                                )

    return movie_src,page_number + 1

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

    for item in mode_hq_list:

        key = item[0]
        inner_name = item[1]

        add_dir("folder", key, '',
            '[B][COLOR silver]'+inner_name+'[/COLOR][/B]',
            path_dicts["icon_image"], path_dicts["icon_image"],info=None)

def cat_site(): 
    """""" 
    page_download = WebCrawler('https://hqbang.com/categories/')

    cat_dict = page_download.fetch_list(
                                  selector='#list_categories_categories_list_items .item',
                                  attr='href',
                                  attr_option = '/categories/',
                                  title_split= True,
                                  title_split_pos = -2,
                                  img = 'https://hqbang.com/contents/categories/2/2.jpg',
                                  group_dict = True
                                  
                                  
            )
    
    k_update = page_download.UpdateKey(dict_keys)
    k_update.update_dict(cat_dict)

    return cat_dict
    
def cat_name(arg):
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
    
    if mode   == "hqcat":    cat_name(cat_site)
