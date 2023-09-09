import os, re, mode_data
from os import path
from json import dump as json_dump, load as json_load

try:
    
    import xbmc
    
except ModuleNotFoundError:
    
    pass

keys_path = re.sub('\\\\sources\\\\source_three', '\\\\modules\\\\keys', os.path.dirname(os.path.abspath(__file__)))
key_join = os.path.join

def dump_data(filename, data):

    with open(filename, 'w') as fh:

        json_dump(data, fh)

def search_query():
    """Open dialog and wait for user input."""

    user_str = ''
    
    keyboard = xbmc.Keyboard(user_str, 'Enter Search Term')
    keyboard.doModal()

    if keyboard.isConfirmed():
        
        entry  = keyboard.getText().lower()

        return entry
    
    else:
        
        return
       
def data_keysJson(arg=0, key='alothome'):
    """Write keylist and modelist to path.
  
        Param Key: only included to determine which condition to execute.
                   It is only essential when requesting json filepath for update.

        param arg 0: write data into json object file path
        param arg 1: obtaining key's json filepath
        param arg 2: write modelist data into json object file path
    """

    key_list =  [
                 (mode_data.data['page_data'][elem], mode_data.data['path_keys'][item])
                 for elem in sorted(mode_data.data['page_data'])for item in sorted(mode_data.data['path_keys'])
                 if elem.split('_')[1] == item.split('_')[0]
                 ]
    
    if arg == 0:

        for item in key_list: dump_data(item[1], item[0])

    elif arg == 1:

       for item in key_list:

           if key in item[0]: key_ = item[1]
                
           else: continue

           return key_

    elif arg == 2:

        dump_data(key_join(keys_path, 'modelist.json'), mode_data.data['path_data'])
    
  

def load_keys(data_key=0, dataKey=None, arg_option=0):
    """"""

    content_ = ''
    
    if data_key == 0:# load page keys
        
        return mode_data.data['path_data']

    elif data_key == 1:# load json key path

        data = mode_data.data['path_keys']

        for item in data:

            if dataKey:

                if dataKey == item:

                    content_ = mode_data.data['path_keys'][dataKey]

                else:

                    continue

            elif not dataKey:

                if 'xf_path' == item:

                    content_ = mode_data.data['path_keys']['xf_path']

                else:

                    continue

        
        with open(content_) as fh:

            content = json_load(fh)
                    
            return content

    elif data_key == 2:# load page data
        
        page_data = mode_data.data['page_data']

        for item in page_data:

            if dataKey:

                if dataKey == item:

                    content_ = mode_data.data['page_data'][dataKey]

                else:

                    continue

            elif not dataKey:

                if 'data_xf' == item:

                    content_ = mode_data.data['page_data']['data_xf']

                else:
                    
                    continue
                
        return content_

    elif data_key == 3:# load modelist from page data
        
        if arg_option == 0:

            mode_list = [item[0] for item in mode_data.data['path_data'][1]]

            return sorted(mode_list)

        elif arg_option == 1:

            mode_list = mode_data.data['path_data'][0],mode_data.data['path_data'][1]

            return mode_list

def readWrite_search(arg_str = None, write=False):
    """Return saved content to memory."""

    path_sub = re.sub('\\\\modules\\\\keys','\\\\sources\\\\source_three',keys_path)

    path = key_join(path_sub,"mysearch.txt")

    if arg_str and write:

        with open(path,'w') as file_handle:
        
            file_handle.write(arg_str)

    elif not arg_str and not write:

        with open(path,'r') as fh:
            
            content = fh.read()
            
            return content

    
def view_keys(filename, load=False):
    """Load and assign number to json object."""
    d_data = dict(); count = 0

    if load:# load json object

        with open(filename) as fh:

            return json_load(fh)

    else:# assign number to json object

        with open(filename) as fh:

            content = json_load(fh)

            for item in content:

                if count > 1:

                    d_data[count] = item

                count += 1
        
        return d_data

def load_homeDir(check_name):

     data = view_keys(key_join(keys_path, 'modelist.json'))

     data_ = list(zip(data.keys(), data.values()))
    
     try:

        for item in data_:

            if item[1][0][0] == check_name:

                 name = item[0]
                 
        return data[name]
            
     except UnboundLocalError:

        print('Name not found..............')
        #xbmc.log('Name not found..............')
        return


def cat_site(obj, url, filePath,selector, attr, attr_option,
             title, title_split, title_split_pos, img,
             group, group_dict):

    page_download = obj(url)

    cat_dict = page_download.fetch_list(

                                  selector=selector,
                                  attr=attr,
                                  attr_option = attr_option,
                                  title = title,
                                  title_split = title_split,
                                  title_split_pos = title_split_pos,
                                  img = img,
                                  group = group,
                                  group_dict = group_dict

            )
    
    k_update = page_download.UpdateKey(filePath)
    k_update.update_dict(cat_dict)

    return cat_dict


def cat_name(func, obj, url, filePath,selector, info = None, attr=None, attr_option=None,
             title=None, title_split=False, title_split_pos = 0, img=None,
             group=False, group_dict=False):

    name_dict = cat_site(obj=obj, url=url, filePath=filePath,selector=selector, attr=attr, attr_option=attr_option,
                title=title, title_split=title_split, title_split_pos = title_split_pos, img=img,
                group=group, group_dict=group_dict)

    
    title_ = [(name, ' '.join(name.split('_')).title()) for name in list(name_dict.keys())]

    for elem in sorted(title_):

        try:

            func("folder", elem[0], '',
                '[B][COLOR orange]'+ elem[1] +'[/COLOR][/B]',
                name_dict[elem[0]][1],
                name_dict[elem[0]][1],info=info)

        except (UnicodeEncodeError,KeyError) as e:

            continue

def name_site(obj, url, filePath,selector, attr_option, image, image_alt,
             title, title_split, arg, arg_num, query_string, link, index, start
             ):

    page_download = obj(url)

    name_dict = page_download.fetch_names(

                                          selector=selector,
                                          attr_option=attr_option,
                                          image = image,
                                          image_alt = image_alt,
                                          title = title,
                                          title_split = title_split,
                                          arg = arg,
                                          arg_num = arg_num,
                                          query_string = query_string,
                                          link = link,
                                          index = index,
                                          start = start
                                          )
    
    k_update = page_download.UpdateKey(filePath)
    k_update.update_dict(name_dict)

    return name_dict

def nameSite(func, obj, url, filePath, selector, attr_option=None, image='src', image_alt=None,
             title=None, title_split=None, arg=0, arg_num=0, query_string=None, link='href', index=False, start=1, info=None, name_filter=None):

    name_dict = name_site(obj=obj,url=url, filePath=filePath,selector=selector, attr_option=attr_option, image=image,
                          image_alt=image_alt,title=title, title_split=title_split, arg=arg, arg_num=arg_num,
                          query_string=query_string, link=link, index=index, start=start
                          )

    
    title_ = [(name, ' '.join(name.split('_')).title()) for name in list(name_dict.keys())]

    for elem in sorted(title_):

        if not name_filter:

            try:

                func("folder", elem[0], '',
                    '[B][COLOR orange]'+ elem[1] +'[/COLOR][/B]',
                     name_dict[elem[0]][1],
                     name_dict[elem[0]][1],info=info
                     )

            except (UnicodeEncodeError,KeyError) as e:

                continue

        elif name_filter:

            if elem[1].lower() not in name_filter:

                    continue

            elif elem[1].lower() in name_filter:

                    try:
                            func("folder", elem[0], '',
                                 '[B][COLOR orange]'+ elem[1] +'[/COLOR][/B]',
                                  name_dict[elem[0]][1],
                                  name_dict[elem[0]][1],info=None
                                 )

                    except (UnicodeEncodeError,KeyError) as e:

                            continue
                        

def fetch_url(obj, key_data, key_home, url_pattern, attr_pattern):


    url = load_keys(2, key_data)[key_home][0] # fetching home url
    
    page_download = obj(url)

    cat_url = [re.search(attr_pattern,item).group() for item in page_download.fetch_list(url_pattern,'href') if not item is None if re.search(attr_pattern,item)][0]

    attr_option = re.search('/\w+?/',cat_url).group(0)

    return cat_url, attr_option
        
if __name__ == "__main__":


    #data_keysJson(2)
    #data_keysJson()

    print(load_keys(data_key=3))

