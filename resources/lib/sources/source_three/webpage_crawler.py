# -*- coding: utf-8 -*-

import re
import os
import time
import string
import warnings
import requests
import threading
import contextlib
from os import path
from bs4 import BeautifulSoup as Soup
from urllib3.exceptions import InsecureRequestWarning
from json import dump as json_dump, load as json_load

try:
    
    import xbmc,xbmcgui,xbmcplugin

except ImportError:
    
    pass

PATH            = '/'
NETWORK_PATH    = '//'
MATCH_START     = '^'
MATCH_ZERO_MORE = '.*'
MATCH_ONE_MORE  = '.+'
WHITE_SPACE     = ' '
SUB_WHITE_SPACE = '_'
PROTOCOL        = '(https?:)//'
URL_HOME        = '(https?://.*?)/'
CLEAN_STR       = "[-.:;\s,()@\\\\&[\]#!$%/+^*=<>?{}|`~]"
CLEAN_ALL       = "[-_.:;\s,()@\\\\&[\]#!$%/+^*=<>?{}|`~]"
MIN_CHECK = (0, 2, 'min_check')
MIDDLE_CHECK = (1, 3, 'middle_check')
MAX_CHECK = (2, 3, 'max_check')
OLD_MERGE_ENV_SETTINGS = requests.Session.merge_environment_settings



@contextlib.contextmanager
def no_ssl_verification():

    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):

        # Verification happens only once per connection;
        # so, we need to close all the opened adapters once we're done.
        # Otherwise, the effects of verify=False persist beyond the end of this context manager.

        opened_adapters.add(self.get_adapter(url))

        settings = OLD_MERGE_ENV_SETTINGS(self, url, proxies, stream, verify, cert)

        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:

        with warnings.catch_warnings():

            warnings.simplefilter('ignore', InsecureRequestWarning)

            yield

    finally:

        requests.Session.merge_environment_settings = OLD_MERGE_ENV_SETTINGS

        for adapter in opened_adapters:

            try:

                adapter.close()

            except:

                pass

class WebPageCrawler:

    # making request behaves like a browser
    fake_agent = {"headers": {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 "
                              "(KHTML, like Gecko)Chrome/50.0.2661.102 Safari/537.36"}}

    def __init__(self, url, payload = None):
        """ A simple object for web page crawling."""

        self.url_ = url
        self.payload = payload
        self.error = ''
        self.web_url = ''                                                           # web url attribute
        self.html_ = ''                                                             # empty str attribute
        self.regex = re                                                             # regular expression attribute
        self.flags = self.regex.S | self.regex.I | self.regex.M                     # regular expression flags
        self.soup = Soup                                                            # beautiful soup attribute
        self.req = requests                                                         # requests attribute
        self.web_thread = threading                                                 # threading attribute
        self.urls_list = []                                                         # empty list attribute
        self.req_session = self.req.Session()                                       # retain same session request accross multiple request
        self.headers = WebPageCrawler.fake_agent["headers"]                         # create fake agent attribute: type(self) == WebPageCrawler
        self.req_session.headers.update(self.headers)                               # update request header

        self.no_verification = no_ssl_verification                                  # no verification attribute

        # making request within this context manager, silent all Secure Sockets Layer (ssl) verification
        with self.no_verification():

            try:
                if not self.payload:
                    self.html_ = self.req_session.get(self.url_, timeout=10)

                elif self.payload:
                    self.html_ = self.req_session.get(self.url_, params=self.payload, timeout=10)

            except requests.exceptions.RequestException:

                pass


    def html(self, prettify=False, page_info=False, url=False):
        """Return unstructured webpage content."""

        try:

            if self.html_.raise_for_status() is None and self.html_.status_code == 200:

                response = self.html_

        except (AttributeError, requests.exceptions.HTTPError) as e:

            try:

                self.error = e.args[0].split("'")[1]

            except IndexError:

                self.error = e.args[0].split(":", maxsplit=1)[0]

            finally:

                return '{}: Unable to fetch web page.'.format(self.error)

        else:

            if prettify: content = self.soup(response.text, 'html.parser').prettify()
            elif page_info: content = {'Response': response, 'URL': response.url, 'Redirect': response.history,
                                       'Header info client': response.headers, 'Status_code': response.status_code,
                                       'Header info server':response.request.headers}
            elif url: content = response.url
            else: content = response.text

            return content

    @property
    def scheme_domain(self):
        """Return url."""
        try:
            
            domain = self.regex.search(URL_HOME, self.html(url=True)).group(1)

        except TypeError:
            
            pass

        else:

            return domain

    @staticmethod
    def arg_range(arg, start):
        """Return list object starting from 1 including end of list."""

        return list(range(arg + 1))[start:]

    @staticmethod
    def alpha():
        """Return ascii lower case alphabet [a-z]."""

        return list(string.ascii_lowercase)

    @staticmethod
    def alpha_num():
        """Return ascii lower case alphabet [a-z] and integer [0-9]."""

        return [1, 2, 3, 4, 5, 6, 7, 8, 9] + list(string.ascii_lowercase)


    @staticmethod
    def view_tag_attributes(element):
        """Return element attributes."""

        elements = element if isinstance(element, (list, tuple)) else [element]
         
        return [element.attrs for element in elements] # return element attribute


    @staticmethod  
    def fetch_string(element, single=False):
        """Return InnerHtml of a selected element."""

        element_string = []
        elements = element if isinstance(element, list) else [element]

        if single: # if single is set to True

            try:

                return element.string.strip()

            except AttributeError:

                pass

        elif not single:

            for elem in elements:

                try:

                    element_string.append(elem.string.strip())

                except AttributeError:

                    continue

            return element_string

    @staticmethod  
    def check_attr_option(element, attr_option):
        """Return tag attribute according to attr_option filter restriction."""

        elements = []
        
        for elem in element:

            if elem.get('href') is None: continue

            if attr_option not in elem.get('href'): continue

            elements.append(elem)

        return elements

    @staticmethod
    def urls(url, arg, arg_num, query_string, index, start):
        """Return properly structured ur in a webpage using BeautifulSoap css selector.

                    Arguments:
                    url: url to be properly structured 
                    arg: default = 0 - signifies which if clause to perform
                    arg_num: default = 0 - signifies which range to create
                    query_string: default = None - signifies addition path string
        """

        web_urls      = []
        arg_alpha     = WebCrawler.alpha()
        arg_alpha_num = WebCrawler.alpha_num()  

        arg_list = WebCrawler.arg_range(arg_num, start) if arg_num > 0 else WebCrawler.arg_range(1, 1) # always 1 except specified otherwise (range 0 and 1) start(1)
        
        # url starts with http or https
        if re.search(MATCH_START + PROTOCOL + MATCH_ZERO_MORE, url):

            if arg == 0: web_urls = [url] # arg set to 0 return first page

            elif arg == 1: 

                if url.endswith(PATH): web_urls = [url + elem for elem in arg_alpha] # arg set to 1 return alphabet

                elif not url.endswith(PATH): web_urls = [url + PATH + elem for elem in arg_alpha]

            elif arg == 2: 

                if url.endswith(PATH): web_urls = [url + str(elem) for elem in arg_alpha_num] # arg set to 2 return alpha numeric

                elif not url.endswith(PATH): web_urls = [url + PATH + str(elem) for elem in arg_alpha_num]

            elif arg == 3: 

                if not query_string:

                    if url.endswith(PATH): web_urls = [url + str(elem) for elem in arg_list] # arg set to 3 return arg_num range

                    elif not url.endswith(PATH): web_urls = [url + PATH + str(elem) for elem in arg_list]

                elif query_string:

                    if isinstance(query_string, (list, tuple)):

                        web_urls_1, web_urls_2 = query_string

                        web_urls = [url + web_urls_1 + str(elem) + web_urls_2 for elem in arg_list]

                    elif not isinstance(query_string, (list, tuple)):

                        if url.endswith(PATH):#page22.html

                            if not index:

                                if '=' in query_string:
                                    web_urls = [url + query_string + str(elem) for elem in arg_list]

                                elif 'page' in query_string: web_urls = [url + query_string + str(elem) for elem in arg_list]

                                elif not '=' in query_string: web_urls = [url + str(elem) + query_string for elem in arg_list]

                            elif index:

                                if '=' in query_string: web_urls = [url + query_string + str(elem) for elem in arg_list]; web_urls.insert(0, url)

                                elif 'page' in query_string: web_urls = [url + query_string + str(elem) for elem in arg_list]; web_urls.insert(0, url)

                                elif not '=' in query_string: web_urls = [url + str(elem) + query_string for elem in arg_list]; web_urls.insert(0, url)

                        elif not url.endswith(PATH):

                            if not index:

                                if '=' in query_string: web_urls = [url + PATH + query_string + str(elem) for elem in arg_list]

                                elif 'page' in query_string: web_urls = [url + query_string + str(elem) for elem in arg_list]

                                elif not '=' in query_string: web_urls = [url + PATH + str(elem) + query_string for elem in arg_list]

                            elif index:

                                if '=' in query_string: web_urls = [url + PATH + query_string + str(elem) for elem in arg_list]; web_urls.insert(0, url)

                                elif 'page' in query_string: web_urls = [url + query_string + str(elem) for elem in arg_list]; web_urls.insert(0, url)

                                elif not '=' in query_string: web_urls = [url + PATH + str(elem) + query_string for elem in arg_list]; web_urls.insert(0, url)
                   
        return web_urls

    @staticmethod
    def decode_url(vu, lc, hr='16'):
        """Return playable reconstructed url 

              Arguments:
              video_url: absolute url containing starting function to be reconstructed 
              licenceCode: video licence to be reformated
              hashRange: interested to hash range to be recalculated
            
         """

        def calcseed(lc, hr):

            f = lc.replace('$', '').replace('0', '1')
            j = int(len(f) / 2)
            k = int(f[0:j + 1])
            el = int(f[j:])
            fi = abs(el - k) * 4
            s = str(fi)
            i = int(int(hr) / 2) + 2
            m = ''

            for g2 in range(j + 1):

                for h in range(1, 5):
                    n = int(lc[g2 + h]) + int(s[g2])
                    if n >= i:
                        n -= i
                    m += str(n)

            return m

        if vu.startswith('function/'):
            vup = vu.split('/')
            uhash = vup[7][0: 2 * int(hr)]
            nchash = vup[7][2 * int(hr):]
            seed = calcseed(lc, hr)
            if seed and uhash:
                for k in range(len(uhash) - 1, -1, -1):
                    el = k
                    for m in range(k, len(seed)):
                        el += int(seed[m])
                    while el >= len(uhash):
                        el -= len(uhash)
                    n = ''
                    for o in range(len(uhash)):
                        n += uhash[el] if o == k else uhash[k] if o == el else uhash[o]
                    uhash = n
                vup[7] = uhash + nchash

            vu = '/'.join(vup[2:]) + '&rnd={}'.format(int(time.time() * 1000))

        return vu

class WebCrawler(WebPageCrawler):   

    def absolute_link(self, url_list):
        """Takes list of urls and return their absolute path."""

        urls = url_list if isinstance(url_list, (list, tuple)) else [url_list]  # create url list object

        url_ = self.scheme_domain                                               # return web domain

        scheme = self.regex.search(PROTOCOL, url_)                              # return http or https


        def absolute_links(self, urls=urls):

            global NETWORK_PATH, PATH

            urls = urls

            if len(urls) > 0:

                url = urls.pop(0)

                if self.regex.search(MATCH_START + NETWORK_PATH + MATCH_ZERO_MORE, url): self.urls_list.append(scheme.group(1) + url) # start with //  

                elif self.regex.search(MATCH_START + PATH + MATCH_ZERO_MORE, url): self.urls_list.append(url_ + url)                  # start with /

                elif self.regex.search(MATCH_START + scheme.group(), url): self.urls_list.append(url)                                 # start with http:// or https:// 

                elif re.search('\w.*?/', url): self.urls_list.append(url_ + '/' + url)                                                # start with char add domain and /

                elif len(urls) <= 0:

                    pass

        while True:

            try:

                absolute_links(self)

                if not urls:

                    break   # if list is empty break out of while loop

            except AttributeError:

                continue

        return self.urls_list


    def absolute_link_single(self, url):
            """Takes url and return its absolute path."""
            
            url_ = self.scheme_domain

            scheme = self.regex.search(PROTOCOL, url_)

            try:

                if self.regex.search(MATCH_START + NETWORK_PATH + MATCH_ZERO_MORE, url):

                    self.web_url = scheme.group(1) + url                                            

                elif self.regex.search(MATCH_START + PATH + MATCH_ZERO_MORE, url):

                    self.web_url = url_ + url

                elif self.regex.search(MATCH_START + scheme.group(), url):

                    self.web_url = url                          

                else:

                    if self.regex.search(PROTOCOL, url):

                        self.web_url = url

                    else:

                        self.web_url = url_ + PATH + url

            except (TypeError,UnicodeEncodeError):

                pass

            else:

                return self.web_url 


    def fetch_single(self, selector, attr=None):
        """Return specific css selector."""

        try:

            match_single = self.soup(self.html(), 'html.parser').select_one(selector)

        except AttributeError:

            return 'No match found'

        else:

            if match_single and not attr: return match_single

            elif match_single and attr: return match_single.attrs[attr]

    @property
    def form(self):
        """"""

        form_dict = {}
        
        form_data = self.fetch_single('form'); form_dict.update(form_data.attrs); form_dict.update(form_data.input.attrs) 

        for item in form_dict.copy():# shallow copy created during iteration to avoid a RuntimeError - dictionary changed size during iteration

            if item.lower() == 'action' and not form_dict['action'].startswith('http'):
     
                form_dict['action'] = self.scheme_domain + form_dict[item]
                    
        return form_dict


    def title_validation(self, title_element, title, title_split, index_pos):
        """Return downloaded page title

        param: title_element: list of downloaded page titles fetch using css selector
        param: title: string provided to be fetch that points to the location of title attribute value on the page
        param: title_split: if set to True href attibuite value is split by '/' into list item
        param: index_pos: title_split index position to be return as title

         """

        if title_split and not title:

             return [element.get('href').split('/')[index_pos] for element in title_element]   
        
        elif title and not title_split:

            if title.lower() == 'title':
                title = [element.get(title) for element in title_element]

            elif title.lower() == 'alt':
                title =  [element.img.get(title) for element in title_element]

            elif title.lower() == 'span':
                title =  [element.span.string for element in title_element]

            elif title.lower() == 'h2':
                title =  [element.h2.string for element in title_element]

            return title


    def image_filter(self, img_match, image_src, attr_option):
        """Return downloaded page img

        param: img_match: list of match css selector fetched from image tag  
        param: image_src: text value provided with or without comma seperation to be fetched from image tag attribute 
        param: attr_option: indicates the specificity of an image tag to be fetched depending on the expected href attribute value

        """
        
        image_list = []
        image_src_ = image_src.split(',')
        
        for element in img_match:

            try:

                if not attr_option:

                    if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
                           
                        image_list.append(self.absolute_link_single(element.img.get(image_src_[0])))

                    elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
                        
                        if element.img.get(image_src_[0]).endswith('.jpg'):

                            image_list.append(self.absolute_link_single(element.img.get(image_src_[0])))

                        elif element.img.get(image_src_[1]).endswith('.jpg'):

                            image_list.append(self.absolute_link_single(element.img.get(image_src_[1])))

                    elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
                        
                        # default back to single selection to avoid out of index error
                        image_list.append(self.absolute_link_single(element.img.get(image_src_[0])))

                elif attr_option:

                    if attr_option in element.get('href'):

                        if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
  
                            image_list.append(self.absolute_link_single(element.img.get(image_src_[0])))

                        elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
                           
                            if element.img.get(image_src_[0]).endswith('.jpg'):

                                image_list.append(self.absolute_link_single(element.img.get(image_src_[0])))

                            elif element.img.get(image_src_[1]).endswith('.jpg'):

                                image_list.append(self.absolute_link_single(element.img.get(image_src_[1])))

                        elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
                           
                            # default back to single selection to avoid out of index error
                            image_list.append(self.absolute_link_single(element.img.get(image_src_[0])))  

            except AttributeError:

                continue

        return image_list

                        
    def fetch_list(self,
                   selector,
                   attr=None,
                   attr_option=None,
                   title=None,
                   title_split=False,
                   title_split_pos = 0,
                   img=None,
                   group=False,
                   group_dict=False):
        """Return list of match attributes in a webpage using BeautifulSoap css selector.

                Arguments:
                selector: css selector parse to beautifulsoup object
                attr: tag key attribute to be selected. if comma seprated string is parse it split into list item else href is parse
                attr_option: if clause condition to be set on the attribute selected
                title: title attribute in link tag <a title='' ></a>
                img: attribute to be selected within the img tag <img />
                group: default False - when set return title attribute, image attribute and href attribute as tuple
                group: default False - when set return title attribute, image attribute and href attribute as dictionary
                
        """

        links = []
        dict_object = dict()
        match = self.soup(self.html(), 'html.parser').select(selector)

        if attr:

            if len(attr.split(',')) > 1:

                    attr_href, attr_regex = tuple(attr.split(','))
                
            elif len(attr.split(',')) == 1:

                    attr_href, attr_regex = attr, None
        
        if match and attr:

            if not attr_option:

                if title and not img and not group and not group_dict: # return link titles

                    return self.title_validation(match, title=title, title_split=title_split, index_pos=title_split_pos)

                elif title_split and not img and not group and not group_dict: # return link titles

                    return self.title_validation(match, title=title, title_split=title_split, index_pos=title_split_pos)

                elif img and not group and not group_dict and not title and not title_split: # return link images

                    if not self.regex.search(PROTOCOL, img): return self.image_filter(img_match = match, image_src = img, attr_option=attr_option)

                    elif self.regex.search(PROTOCOL, img): return img              

                elif title or title_split and img: # return links dict

                    if attr_regex is None:

                        link = [self.absolute_link_single(element.get(attr_href)) for element in match]

                    elif attr_regex:

                        links = [element.get(attr_href) for element in match]

                        link = [self.absolute_link_single(self.regex.search(attr_regex, link).group(1)) for link in links if self.regex.search(attr_regex, link)]

                    title = self.title_validation(match, title=title, title_split=title_split, index_pos=title_split_pos)

                    if not self.regex.search(PROTOCOL, img): image = self.image_filter(img_match = match, image_src = img, attr_option=attr_option)
                
                    elif self.regex.search(PROTOCOL, img): image = [img for item in range(len(link))]

                    if group:

                        return list(zip(link,image,title))

                    elif group_dict:

                        obj_tuple = list(zip(link,image,title))

                        for item in obj_tuple:

                            try:

                                dict_object[self.regex.sub(CLEAN_STR, SUB_WHITE_SPACE, item[2].lower())] = item

                            except AttributeError:
                                                     
                                continue

                        return dict_object

                else:

                    if attr_regex is None:

                        return [self.absolute_link_single(element.get(attr_href)) for element in match]

                    elif attr_regex:

                        links = [element.get(attr_href) for element in match]

                        return [self.absolute_link_single(self.regex.search(attr_regex, link).group(1)) for link in links if self.regex.search(attr_regex, link)]

            elif  attr_option:

                if title and not img and not group and not group_dict:

                    return self.title_validation(match, title=title, title_split=title_split, index_pos=title_split_pos)

                elif title_split and not img and not group and not group_dict:

                    return self.title_validation(match, title=title, title_split=title_split, index_pos=title_split_pos)

                elif img and not group and not group_dict and not title and not title_split:

                    if not self.regex.search(PROTOCOL, img): return self.image_filter(img_match = match, image_src = img, attr_option=attr_option)

                    elif self.regex.search(PROTOCOL, img): return img

                elif title or title_split and img:

                    if attr_regex is None:

                        link = [self.absolute_link_single(element.get(attr_href)) for element in match if attr_option in element.get(attr_href)]

                    elif attr_regex:

                        links = [element.get(attr_href) for element in match if attr_option in element.get(attr_href)]

                        link = [self.absolute_link_single(self.regex.search(attr_regex, link).group(1)) for link in links if self.regex.search(attr_regex, link)]

                    title = self.title_validation(match, title=title, title_split=title_split, index_pos=title_split_pos)

                    if not self.regex.search(PROTOCOL, img): image = self.image_filter(img_match = match, image_src = img, attr_option=attr_option)

                    elif self.regex.search(PROTOCOL, img): image = [img for item in range(len(link))]

                    if group: return list(zip(link,image,title))

                    elif group_dict:

                        obj_tuple = list(zip(link,image,title))

                        for item in obj_tuple:

                            try:

                                dict_object[self.regex.sub(CLEAN_STR, SUB_WHITE_SPACE, item[2].lower())] = item

                            except AttributeError:
                                                     
                                continue

                        return dict_object
                
                else:

                    match_ = []

                    if attr_regex is None:

                        for element in match:

                            try:

                                if attr_option in element.get(attr_href):

                                    match_.append(element.get(attr_href))

                            except TypeError:

                                continue

                        return match_

                    elif attr_regex:

                        for element in match:

                            try:

                                if attr_option in element.get(attr_href):

                                    match_.append(element.get(attr_href))

                            except TypeError:

                                continue

                        links = match_

                        return [self.absolute_link_single(self.regex.search(attr_regex, link).group(1)) for link in links if self.regex.search(attr_regex, link)]


        elif match and not attr:
            
            return match

        else:

            return 'No match found'

    def sieve_fetch(self, text, search_string, group=0):
        """Return match from element according to its attribute selection.
        param: text: page download or matched tag inner html
        param: search_string: regular expression search pattern for fetching text from downloaded page or match tag inner html
        param: group: parenthesised match to be returned default = 0
        """

        single_match = self.regex.compile(search_string, self.flags).search(text)

        if single_match: return single_match.group(group)

        elif not single_match:  return 'No match found'


    class Flattern:

        def __init__(self):
            """An object that combine nested list into single list."""

            self.recursive_list = []

        def recursive(self, iteration):
            """Return list object or flattern a nested list object. For example:

                    var = [[1,2,3],[4,5]] nested
                    var = [1,2,3]         non-nested
                    >>> var
                    [1,2,3,4,5]
                    >>> var
                    [1,2,3]
            """

            store_tup = ()

            for item in iteration:

                if isinstance(item, (list, tuple)): store_tup += self.recursive(item)

                elif not isinstance(item, (list, tuple)): store_tup += (item,)

            return store_tup


    class UpdateKey:
        """A class that validates and update json file contents."""

        def __init__(self, filename):
            """Initialising WriteKey instance variables."""

            self.filename = filename
            self.writejson = json_dump
            self.readjson = json_load
            
        def loadfile(self):
            """Return contents from read json file."""

            with open(self.filename,'r') as fh:

                content = self.readjson(fh)

                return content

        def update_dict(self, kwargs):
            """Read json object into memory then check for keys.

               if key exist,ignore key; otherwise,
               updates key in json file contents.

            """
            if not path.isfile(self.filename):

                with open(path.join('.',self.filename), 'w') as fh:

                    if not isinstance(kwargs, dict): self.writejson(dict(kwargs), fh)

                    elif isinstance(kwargs, dict): self.writejson(kwargs, fh)

            elif path.isfile(self.filename):

                content = self.loadfile()# content is dict object then all dict attribute is available to the object

                with open(self.filename, 'w') as fh:

                    if not isinstance(kwargs, dict): modify_kwargs = dict(kwargs)

                    elif isinstance(kwargs, dict): modify_kwargs = kwargs

                    content.update(modify_kwargs)

                    self.writejson(content, fh)


    def cat_string(self,  link_selector, iteration = None, str_selector=None, img_selector=None, src=None):
        """Return element attributes according to match found.

          param: link_selector: css selector parse to beautifulsoup object ('.thumb-category a')
          param: iteration: integer - indicates number of pages to be scrapped (list(range(1, 4)))
          param: str_selector: css selector to scrapped inner html from match element ('.thumb-category a .title')
          param: img_selector: css selector to scrapped image tag attribute from match element ('.thumb-category a img')
          param: src: image tag attribute to be scrapped (src)

        """

        url = self.html(page_info=True)['URL']

        link_selector = link_selector
        img_selector = img_selector
        src = src
        iteration = iteration
        str_selector = str_selector
        

        def page_url(url=url,  link_selector= link_selector, iteration = iteration, str_selector = str_selector, img_selector=img_selector, src= src):
            """"""

            instance = WebCrawler(url)
            img_src = src if src is not None else 'data-src'
            url_list = []
            link_list = []
            inner_html = []
            img_list = []

            if iteration:

                while True:

                    url_con = iteration.pop(0)

                    # creating sepearate instances for each page because of different page information
                    link_list.append(
                                     WebCrawler(url + str(url_con) + '/').absolute_link(
                                         WebCrawler(url + str(url_con) + '/').fetch_list(selector=link_selector, attr='href')# fetching list href links
                                         )
                        )

                    if str_selector:

                        inner_html.append(
                                          WebCrawler(url + str(url_con) + '/').fetch_text(str_selector)
                                          )

                    if img_selector:

                        img_list.append(
                                        WebCrawler(url + str(url_con) + '/').absolute_link(
                                            WebCrawler(url + str(url_con) + '/').fetch_list(img_selector, img_src) # fetching list image links
                                            )
                                        )

                    if not iteration:

                        break

            elif not iteration:

                link_list.append(
                                 WebCrawler(url).absolute_link(
                                     WebCrawler(url).fetch_list(selector=link_selector, attr='href')
                                     )
                                 )

                if str_selector:

                    inner_html.append(
                                      WebCrawler(url).fetch_text(str_selector)
                                      )

                if img_selector:

                    img_list.append(
                                    WebCrawler(url).absolute_link(
                                        WebCrawler(url).fetch_list(img_selector, img_src)
                                        )
                                    )

            return list(
                        zip(instance.Flattern().recursive(link_list),
                            instance.Flattern().recursive(img_list),
                            instance.Flattern().recursive(inner_html)
                            )
                        )

        return page_url()

    def fetch_cat(self, link_selector, iteration = None, str_selector=None, img_selector=None, src=None):

        """Return element attributes according to match found.

          param: link_selector: css selector parse to beautifulsoup object ('.thumb-category a')
          param: iteration: integer - indicates number of pages to be scrapped (list(range(1, 4)))
          param: str_selector: css selector to scrapped inner html from match element ('.thumb-category a .title')
          param: img_selector: css selector to scrapped image tag attribute from match element ('.thumb-category a img')
          param: src: image tag attribute to be scrapped (src)

        """

        cat_tup = self.cat_string(
                                  link_selector=link_selector,
                                  iteration = iteration,
                                  str_selector=str_selector,
                                  img_selector=img_selector,
                                  src=src
                                  )

        cat_dict = {self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,elem[2]).lower(): [elem[0], elem[1], elem[2].title()] for elem in cat_tup}

        return cat_dict  


    def fetch_text(self, selector):
        """Return element text string (Inner html) from css selector list object returned.
        param: selector: css selector to match element from page download .links, #links, [href*=links]

       """

        source = self.fetch_list(selector=selector)

        return WebCrawler.fetch_string(source)


    def replace_text(self, search_pattern, replace_string, text = None, element = None):
        """Replace text according regex pattern and match found.

            search_pattern syntax according regular expression documentation <https://docs.python.org/3/library/re.html>
            sub(pattern, repl, string, count=0, flags=0)
            sub(repl, string, count=0)

            param: search_pattern: regular expression pattern to fetched match text from page download
            param: replace_string: matched text to be replaced by provided text
            param: text: fetching interested text from webpage download <html>all content<html/>
            param: element: fetching interested text from match tag inner html
        """

        if element and not text:

            try:

                match_from_elem =  WebCrawler.fetch_string(self.fetch_single(element), single=True)

                match = self.regex.compile(search_pattern, self.flags).sub(replace_string, match_from_elem)

            except TypeError:

                pass

        elif text and not element:

            try:

                match = self.regex.compile(search_pattern, self.flags).sub(replace_string, text)

            except TypeError:

                pass

        return match


    def playable_links_tup(self,
                           selector_list,
                           search_pattern,
                           replace_string,
                           element,
                           img_selector,
                           img_attr_single,
                           attr_option = None,
                           selector_link = 'video source',
                           attr_link = 'src',
                           attr_list = 'href',
                           meta_desc = 'meta[name="description"]',
                           sieve_str = False,
                           sieve_pattern = 'video_url:\s+(.*?\.mp4)',
                           replace_str = None,
                           filter_list = None
                           ):
        """Return all playable within a page as tuple.

           param: selector_list: css selector to match all links in a webpage ('.thumb-video a')
           param: search_pattern: regex pattern to extract match from title tag inner html (\s+\|\s+\w+?)
           param: replace_string: replace text if search pattern return match ('')
           param: element: tag element to be match  ('title' or h1)
           param: img_selector:  either image tag element to be matched ('video' or meta[og=image]) or regex pattern to be match when img_attr_single is 'sieve'
           param: img_attr_single: either image tag attribute to be fetched ('poster') or regex pattern to be matched when 'sieve' is parsed as argument
           param: attr_option: to ensure all element fetch contains video links ('/videos/')
           param: selector_link: element link containing .mp4 to be fetched
           param: attr_link: all playable links attribute to be fetch from match selector_link ('src') default 'src'
           param: attr_list: links tag attribute to be fetch ('href') default 'href'
           param: attr_list_regex:
           param: attr_regex_group: 
           param: meta_desc: meta data tag to be fetched using content attribute lookup
           param: sieve_str: default = False
           param: sieve_pattern: fetch playable link using regex within html text instead of tag reference first before fetching: default = 'video_url:\s+(.*\.mp4)'
           param: replace_str: replace playable link text using regex re.sub: default = None

           Change log 21/03/2023
           param: filter_list: to fetch list playable links instead of single - when tuple is parse as argument assign or convert split str to tuple: default = None

           This allows playable links to be fetched as list item then sleeze, split and fetch = (3, '?', 0) or [3, '?', 0]. note - argument must be tuple or list 
        """

        # link list arguments
        attr_list = attr_list
        attr_option = attr_option
        selector_list = selector_list

        # playable link selector
        selector_link = selector_link
        attr_link = attr_link

        # title argument
        search_pattern = search_pattern
        replace_string = replace_string
        element = element

        # tag image argument 
        img_selector =  img_selector
        img_attr_single = img_attr_single

        # plot argument
        meta_desc = meta_desc

        # list links argument only used when .mp4 is hidden further down 
        filter_list = filter_list 

        # if playable links is found outside a tag reference
        sieve_str = sieve_str
        sieve_pattern = sieve_pattern
        replace_str = replace_str


        url_list = list(
                        set(
                             self.absolute_link(
                                               self.fetch_list(selector = selector_list, attr=attr_list, attr_option = attr_option)
                                               )
                             )
                        )

        def playable_source(
                            url_list,
                            selector_link,
                            attr_link,
                            search_pattern,
                            replace_string,
                            element,
                            img_selector,
                            img_attr_single,
                            meta_desc,
                            sieve_str=sieve_str,
                            sieve_pattern = sieve_pattern,
                            replace_str = replace_str,
                            filter_list = filter_list 
                            ):

            urls = url_list

            playable_list = []
            attr_link = attr_link
            selector_link = selector_link
            search_pattern = search_pattern
            replace_string = replace_string
            element = element
            img_selector = img_selector
            img_attr_single = img_attr_single
            meta_desc = meta_desc
            sieve_str=sieve_str
            sieve_pattern = sieve_pattern
            replace_str = replace_str
            filter_list = filter_list 
        
            while urls: 

                url_pop = urls.pop(0)
                obj_instance = WebCrawler(url_pop) # creating new object because each object have different playable link

                if not sieve_str:

                    if not filter_list:

                        try:
                            
                            play_link = obj_instance.absolute_link_single(obj_instance.fetch_single(selector=selector_link, attr=attr_link))

                        except Exception:

                            continue

                    elif filter_list: 

                        try:
                            
                            link_pos, split_with, link_return = tuple(filter_list)
                            
                        except ValueError as error:

                            return '{}: Value must be tuple and not str or dict'.format(error)

                        try:
                            
                            play_link = obj_instance.absolute_link_single(
                                obj_instance.fetch_list(selector=selector_link, attr=attr_link)[int(link_pos)].split(split_with, 1)[int(link_return)]
                                )

                        except Exception:

                            continue

                elif sieve_str and not replace_str:

                    try:
                        # creates a temporary match for error checks
                        _play_link = obj_instance.sieve_fetch(obj_instance.html(), sieve_pattern, 1)

                    except Exception:

                        continue

                    else:

                        if _play_link != 'No match found':
                            
                            # creates a permanent match
                            if not _play_link.startswith('function'):

                                play_link = obj_instance.sieve_fetch(obj_instance.html(), sieve_pattern, 1)

                            elif _play_link.startswith('function'):

                                vid_url     = obj_instance.sieve_fetch(obj_instance.html(), sieve_pattern, 1)
                                vid_licence = obj_instance.sieve_fetch(obj_instance.html(), "license_code:\s+'(.+?)'", 1)
                                play_link   = obj_instance.decode_url(vu=vid_url, lc=vid_licence)

                        elif _play_link == 'No match found':

                            continue

                elif replace_str:
                    
                    try:

                        _play_link = obj_instance.sieve_fetch(obj_instance.html(), sieve_pattern, 1)

                    except Exception:

                        continue

                    else:

                        if _play_link != 'No match found':

                            text = _play_link
                                
                            if isinstance(replace_str, dict):

                                play_link = obj_instance.replace_text(
                                                                      search_pattern = replace_str['search_pattern'],
                                                                      replace_string = replace_str['search_string'],
                                                                      text = text
                                                                      )

                            elif isinstance(replace_str, (list, tuple)):
                                 
                                play_link = obj_instance.replace_text(
                                                                      search_pattern = replace_str[0],
                                                                      replace_string = replace_str[1],
                                                                      text = text
                                                                      )

                            elif isinstance(replace_str, str):

                                split_str = replace_str.split(',')

                                play_link = obj_instance.replace_text(
                                                                      search_pattern = split_str[0],
                                                                      replace_string = split_str[1],
                                                                      text = text
                                                                      )

                        elif _play_link == 'No match found':


                            continue

                try:
                    
                    '.mp4' in play_link or 'http' in play_link
                
                except Exception:

                    continue

                else:
                    
                    if 'meta' in meta_desc:

                        plot = obj_instance.fetch_single(selector=meta_desc, attr='content')
                        
                    elif 'meta' not in meta_desc:

                        plot = obj_instance.replace_text(search_pattern, replace_string, element = element)

                    title = obj_instance.replace_text(search_pattern, replace_string, element = element)

                    # make this optional to select from main page
                    if img_attr_single != 'sieve':

                        image = obj_instance.absolute_link_single(obj_instance.fetch_single(selector = img_selector, attr = img_attr_single))

                    elif img_attr_single == 'sieve':

                        image = obj_instance.sieve_fetch(obj_instance.html(), img_selector, 1)

                    elif img_attr_single == 'sieve prettify':

                        image = obj_instance.sieve_fetch(obj_instance.html(prettify=True), img_selector, 1)

                    playable_list.append((play_link,title,image,{'title': title,'plot' : plot}))
            

                if not urls:

                    break

            return playable_list

        return playable_source(url_list, selector_link, attr_link, search_pattern, replace_string,element,
                               img_selector, img_attr_single, meta_desc, sieve_str, sieve_pattern)

   
    def make_playable_links(self,
                            link_list_selector,

                            title_search_pattern,
                            title_replace_string,
                            title_tag_match,

                            img_selector,
                            img_attr_single,

                            attr_list_option = None,

                            attr_link_selector = 'href',

                            meta_desc = 'meta[name="description"]',

                            sieve_pattern = '/movies/.*?\.mp4',
                            match_url_tag = 'iframe',
                            match_url_src = 'src',
                            make_url_path = 'https://video.xxxa.net'
                            ):
        """Return all playable links within a page as tuple.

           param: link_list_selector: css selector to fetch all links in a webpage ('.thumb-video a')
           param: title_search_pattern: regex pattern to fetch title tag inner html (\s+\|\s+\w+?)
           param: title_replace_string: replace text if search pattern return match ('')
           param: title_tag_match: tag to be fetch  (title or h1)
           param: img_selector:  image tag to be fetched ('video' or meta[og=image])
           param: img_attr_single: image tag attribute to be fetched ('poster')
           param: attr_list_option: this ensure all tag fetch contains video links ('/videos/')
           param: attr_link_selector: element link containing .mp4 to be fetched
           param: meta_desc: element fetched from meta data tag using content atrr lookup
           param: sieve_pattern: fetch playable link using regex within html text instead of tag reference first before fetching: default = 'video_url:\s+(.*\.mp4)'
           param: match_url_tag: locational tag of the playable link to be fetched - default - iframe
           param: match_url_src: attribute to be fetched from all links match from match_url_src: default ='src'
           param: make_url_path: home url to be added to playable path fetched - default - 'https://video.xxxa.net'
           
        """
        
        # link list arguments
        link_list_selector = link_list_selector
        attr_link_selector = attr_link_selector
        attr_list_option = attr_list_option

        # title argument
        title_search_pattern = title_search_pattern
        title_replace_string = title_replace_string
        title_tag_match = title_tag_match

        # tag image argument 
        img_selector =  img_selector
        img_attr_single = img_attr_single

        # plot argument
        meta_desc = meta_desc

        # make playable path sieve_pattern = sieve_pattern must be used with this construct
        sieve_pattern = sieve_pattern
        make_url_path = make_url_path
        match_url_tag = match_url_tag
        match_url_src = match_url_src


        url_list = list(
                        set(
                             self.absolute_link(
                                               self.fetch_list(selector = link_list_selector, attr=attr_link_selector, attr_option = attr_list_option)
                                               )
                             )
                        )

        def playable_source(
                            url_list,
                            
                            title_search_pattern,
                            title_replace_string,
                            title_tag_match,
                            
                            img_selector,
                            img_attr_single,

                            meta_desc,

                            sieve_pattern,
                            make_url_path,
                            match_url_tag,
                            match_url_src
                            ):

            urls = url_list
            playable_list = []

            title_search_pattern = title_search_pattern
            title_replace_string = title_replace_string
            title_tag_match = title_tag_match
                            
            img_selector = img_selector
            img_attr_single = img_attr_single

            meta_desc = meta_desc

            sieve_pattern = sieve_pattern
            make_url_path = make_url_path
            match_url_tag = match_url_tag
            match_url_src = match_url_src
        
            while urls:

                url_pop = urls.pop(0)
                obj_instance = WebCrawler(url_pop)

                _make_url_text = obj_instance.fetch_single(match_url_tag, match_url_src)

                if _make_url_text != 'No match found':
                
                    make_url_text = obj_instance.fetch_single(match_url_tag, match_url_src)

                elif _make_url_text == 'No match found':

                    continue

                try:

                    '.mp4' in make_url_text

                except TypeError:

                    continue

                else:

                    try:

                        #playable links
                        make_url_text = obj_instance.fetch_single(match_url_tag, match_url_src)
                        playable = make_url_path + obj_instance.sieve_fetch(make_url_text, sieve_pattern)

                        # links title
                        playable_title = obj_instance.replace_text(title_search_pattern, title_replace_string, element = title_tag_match)

                        # links images
                        source_image = obj_instance.absolute_link_single(obj_instance.fetch_single(selector = img_selector, attr = img_attr_single))

                        if 'meta' in meta_desc: plot = obj_instance.fetch_single(selector=meta_desc, attr='content')
                        elif 'meta' not in meta_desc: plot = obj_instance.replace_text(title_search_pattern, title_replace_string, element = title_tag_match)

                        playable_list.append((
                                             playable,
                                             playable_title,
                                             source_image,
                                             {
                                              'title': playable_title,
                                              'plot' : plot   
                                             }
                                             ))
                    
                    except Exception: continue

                    if not urls:

                        break

            return playable_list

        return playable_source(url_list, title_search_pattern, title_replace_string, title_tag_match, img_selector,
                               img_attr_single, meta_desc, sieve_pattern, make_url_path, match_url_tag,  match_url_src)
    

    def play_links_tup(self,
                           selector_list,
                           img_selector,
                           
                           title = None,
                           title_split = False,
                           title_split_pos = 0,
                           attr_option = None,

                           selector_link = 'video source',
                           attr_link = 'src',

                           attr_list = 'href',

                           meta_desc = 'meta[name="description"]',

                           sieve_str = False,
                           sieve_pattern = 'video_url:\s+(.*?\.mp4)'
                           ):
        """Return all playable within a page as tuple.

           param: selector_list: css selector to match all links in a webpage such as ('.thumb-video a')
           param: img_selector:  image tag element to be matched such as ('video') or meta[og=image]
           param: title: tag element to be match  such as 'title' or h1
           param: title_split: replace text if search pattern return match ('')
           param: title_split_pos: regex pattern to match title tag inner html such as \s+\|\s+\w+?
           param: attr_option: to ensure all element fetch contains video links such as '/videos/'
           param: selector_link: element link to be matched containing .mp4
           param: attr_link: attribute to be fetched from matched selector_link default 'src'
           param: attr_list: all links matched containing 'href' default 'href'
           param: meta_desc:meta data tag to be fetched using content atrr lookup
           param: sieve_str: default = False
           param: sieve_pattern: fetch playable link using regex within html text instead of tag reference first before fetching: default = 'video_url:\s+(.*\.mp4)'
        """

        # link list arguments
        attr_list = attr_list
        attr_option = attr_option
        selector_list = selector_list

        # playable link selector
        selector_link = selector_link
        attr_link = attr_link

        # title argument
        title = title
        title_split = title_split
        title_split_pos = title_split_pos

        # tag image argument 
        img_selector =  img_selector

        # plot argument
        meta_desc = meta_desc

        # if playable links is found outside a tag reference
        sieve_str = sieve_str
        sieve_pattern = sieve_pattern

        #fetch_list(self, selector, attr=None, attr_option=None, title=None, title_split=False, title_split_pos = 0, img=None, group=False, group_dict=False)
        links_tup = self.fetch_list(selector = selector_list,
                                    attr=attr_list,
                                    attr_option = attr_option,
                                    title = title,
                                    img=img_selector,
                                    title_split = title_split,
                                    title_split_pos = title_split_pos,
                                    group=True
                                    )


        def playable_source(
                            links_tup,
                            selector_link,
                            attr_link,
                            meta_desc,
                            sieve_str=sieve_str,
                            sieve_pattern = sieve_pattern
                            ):

            playable_list = []
            
            urls = links_tup
            attr_link = attr_link
            selector_link = selector_link
            meta_desc = meta_desc
            sieve_str=sieve_str
            sieve_pattern = sieve_pattern
        
            while urls:

                xbmc.log('*'*100)
                xbmc.log(str(urls))
                xbmc.log('*'*100)

                link_, image_, title_ = urls.pop(0)

                obj_instance = WebCrawler(link_) # creating new object because each object have different playable link


                if not sieve_str:

                    try:

                        play_link = obj_instance.fetch_single(selector=selector_link, attr=attr_link)

                    except Exception:

                        continue

                elif sieve_str:

                    _play_link = obj_instance.fetch_single(selector=selector_link, attr=attr_link)

                    if _play_link != 'No match found':

                        try:

                            play_link = obj_instance.sieve_fetch(obj_instance.html(), sieve_pattern, 1)

                        except Exception:

                            continue

                    elif _play_link == 'No match found':

                        continue

                try:

                    '.mp4' in play_link

                except TypeError:

                    continue

                else:

                    if 'meta' in meta_desc:

                        plot = obj_instance.fetch_single(selector=meta_desc, attr='content')
                        
                    elif 'meta' not in meta_desc:

                        plot = title_

                    title = title_
                    image = image_
                    
                    playable_list.append((play_link,title,image,{'title': title,'plot' : plot}))
            

                if not urls:

                    break

            return playable_list

        return playable_source(links_tup, selector_link, attr_link, meta_desc, sieve_str, sieve_pattern)
    

    def playable_link_regex(self, pattern, group=None):
        """Return playable link according to regex pattern.

        param: pattern: regular expression pattern to be fetched such s\w*? or \w{3,}
        param: group: parenthesised match to be returned such as 0 or 1

        """

        text = self.html()

        if group:

            return self.sieve_fetch(text=text, search_string=pattern, group=group)

        else:

            return self.sieve_fetch(text=text, search_string=pattern)


    def fetch_names(self,
                    selector,
                    attr_option = None,
                    image='src',
                    image_alt = None, 
                    title = None,
                    title_split = None,
                    arg = 0,
                    arg_num = 0,
                    query_string = None,
                    link='href',
                    index=False,
                    start = 1
                    ):
        """Return names in webpage.

            Arguments:

            param: selector: css selector parse to beautifulsoup object for tag/element matching such as .name, #name, a[href=] or [href*=]
            param: attr_option: to ensure all element fetch contains video links such as '/videos/'
            param: image: image attribute to be matched in image tag/element such src, src_data
            param: title: title attribute to be returned
            param: title_split: list index position to be returned - mostly used to split title from end of href attribute such as -2 or 2
            param: image_alt: image attribute to be returned - only use if title attribute is not found within the <a> tag/element such alt
            param: arg: assigned integer value between 0 - 3 range - default is 0  such as arg = 1, arg = 2 or arg = 3
            param: arg_num: assigned range and return list object from 1 including end point such as arg_num = 95 or arg_num = 200
            param: query_string: absolute url path to be scraped - often use to indicate absolute path specificity such as query_string='/' or uery_string='?s='.
                   query_string can also be parse as tuple such as ('page', '.html') which will be assigned to var_1 and var_2 respectively
            param: link: only assigned a different value if link tag <a> specifies otherwise rather than href
            param: index: only to be set to True if URL page start from page forcing first page to exist without page number attached (/1)
            param: start: only to be set when starting do not have first page as valid URL (http://host:port/2) - default = 1

            change log 14/03/2023

            Introduction of attr_option allows attribute href to be filter like the filter in fetch list.
            Introduction of query_string tuple type allows tuple value query string to be parse as argument.
            
        """
        
        element_dict = {}
        image_src_ = image.split(',')

        url = self.html(page_info=True)['URL']

        if attr_option:
                

            element_list = [WebCrawler.check_attr_option(WebCrawler(url_).fetch_list(selector=selector),attr_option)
                            for url_ in WebCrawler.urls(url, arg, arg_num, query_string, index, start)]

        elif not attr_option:

            element_list = [WebCrawler(url_).fetch_list(selector) for url_ in WebCrawler.urls(url, arg, arg_num, query_string, index, start)]

        elements = self.Flattern().recursive(element_list)
       

        if title:

            if not self.regex.search(PROTOCOL, image):

                for name in elements:

                    if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
                        
                        try:

                            image_ = name.img.attrs[image_src_[0]]

                        except AttributeError:continue

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
                                    ]

                        except (AttributeError, KeyError):

                            continue

                    elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
                        
                        if name.img.attrs[image_src_[0]].endswith('.jpg'):

                            image_ = name.img.attrs[image_src_[0]]

                        elif name.img.attrs[image_src_[1]].endswith('.jpg'):

                            image_ = name.img.attrs[image_src_[1]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
                                    ]

                        except (AttributeError, KeyError):

                            continue

                    elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
                        
                        image_ = name.img.attrs[image_src_[0]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
                                    ]

                        except (AttributeError, KeyError):

                            continue
                  

            elif self.regex.search(PROTOCOL, image):

                for name in elements:
              
                    try:

                        element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), image,
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
                            ]

                    except (AttributeError, KeyError):   

                        continue

        elif image_alt and not title and not title_split:

            if self.regex.search(PROTOCOL, image):

                   for name in elements:  

                       try:

                           element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), image,
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
                            ]

                       except (AttributeError, KeyError):

                          continue

            elif not self.regex.search(PROTOCOL, image):
                
                for name in elements:

                    if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
                        
                        image_ = name.img.attrs[image_src_[0]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.img.attrs[image_alt]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]),  self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
                                      ]

                        except (AttributeError, KeyError):

                            continue

                    elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
                        
                        if name.img.attrs[image_src_[0]].endswith('.jpg'):

                            image_ = name.img.attrs[image_src_[0]]

                        elif name.img.attrs[image_src_[1]].endswith('.jpg'):

                            image_ = name.img.attrs[image_src_[1]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.img.attrs[image_alt]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]),  self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
                                      ]

                        except (AttributeError, KeyError):

                            continue

                    elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
                        
                        image_ = name.img.attrs[image_src_[0]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.img.attrs[image_alt]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]),  self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
                                      ]

                        except (AttributeError, KeyError):

                            continue


        elif title_split and not title and not image_alt:

            if self.regex.search(PROTOCOL, image): 

                   for name in elements:

                       try:

                           element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), image,
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[link].split('/')[title_split]).title()
                            ]

                       except (AttributeError, KeyError):

                          continue

            elif not self.regex.search(PROTOCOL, image):

                for name in elements:

                    if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
                        
                        image_ = name.img.attrs[image_src_[0]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE,name.attrs[link].split('/')[title_split]).title()
                                      ]

                        except (AttributeError, KeyError):

                            continue

                    elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
                       
                        if name.img.attrs[image_src_[0]].endswith('.jpg'):

                            image_ = name.img.attrs[image_src_[0]]

                        elif name.img.attrs[image_src_[1]].endswith('.jpg'):

                            image_ = name.img.attrs[image_src_[1]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE,name.attrs[link].split('/')[title_split]).title()
                                      ]

                        except (AttributeError, KeyError):

                            continue

                    elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
                        
                        image_ = name.img.attrs[image_src_[0]]

                        try:

                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE,name.attrs[link].split('/')[title_split]).title()
                                      ]

                        except (AttributeError, KeyError):

                            continue


        return element_dict

#========================================================================
##    def fetch_names(self,
##                    selector,
##                    attr_option = None,
##                    image='src',
##                    image_alt = None, 
##                    title = None,
##                    title_split = None,
##                    arg = 0,
##                    arg_num = 0,
##                    query_string = None,
##                    link='href',
##                    index=False,
##                    start = 1
##                    ):
##        """Return names in webpage.
##
##            Arguments:
##
##            param: selector: css selector parse to beautifulsoup object for tag/element matching such as .name, #name, a[href=] or [href*=]
##            param: attr_option: to ensure all element fetch contains video links such as '/videos/'
##            param: image: image attribute to be matched in image tag/element such src, src_data
##            param: title: title attribute to be returned
##            param: title_split: list index position to be returned - mostly used to split title from end of href attribute such as -2 or 2
##            param: image_alt: image attribute to be returned - only use if title attribute is not found within the <a> tag/element such alt
##            param: arg: assigned integer value between 0 - 3 range - default is 0  such as arg = 1, arg = 2 or arg = 3
##            param: arg_num: assigned range and return list object from 1 including end point such as arg_num = 95 or arg_num = 200
##            param: query_string: absolute url path to be scraped - often use to indicate absolute path specificity such as query_string='/' or uery_string='?s='.
##                   query_string can also be parse as tuple such as ('page', '.html') which will be assigned to var_1 and var_2 respectively
##            param: link: only assigned a different value if link tag <a> specifies otherwise rather than href
##            param: index: only to be set to True if URL page start from page forcing first page to exist without page number attached (/1)
##            param: start: only to be set when starting do not have first page as valid URL (http://host:port/2) - default = 1
##
##            change log 14/03/2023
##
##            Introduction of attr_option allows attribute href to be filter like the filter in fetch list.
##            Introduction of query_string tuple type allows tuple value query string to be parse as argument.
##            
##        """
##        
##        element_dict = {}
##        image_src_ = image.split(',')
##
##        url = self.html(page_info=True)['URL']
##
##        if attr_option:
##                
##
##            element_list = [WebCrawler.check_attr_option(WebCrawler(url_).fetch_list(selector=selector),attr_option)
##                            for url_ in WebCrawler.urls(url, arg, arg_num, query_string, index, start)]
##
##        elif not attr_option:
##
##            element_list = [WebCrawler(url_).fetch_list(selector) for url_ in WebCrawler.urls(url, arg, arg_num, query_string, index, start)]
##
##        elements = self.Flattern().recursive(element_list)
##       
##
##        if title:
##
##            if not self.regex.search(PROTOCOL, image):
##
##                for name in elements:
##
##                    if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
##                        
##                        try:
##
##                            image_ = name.img.attrs[image_src_[0]]
##
##                        except AttributeError:continue
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
##                                    ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##                    elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
##                        
##                        if name.img.attrs[image_src_[0]].endswith('.jpg'):
##
##                            image_ = name.img.attrs[image_src_[0]]
##
##                        elif name.img.attrs[image_src_[1]].endswith('.jpg'):
##
##                            image_ = name.img.attrs[image_src_[1]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
##                                    ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##                    elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
##                        
##                        image_ = name.img.attrs[image_src_[0]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
##                                    ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##                  
##
##            elif self.regex.search(PROTOCOL, image):
##
##                for name in elements:
##              
##                    try:
##
##                        element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), image,
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[title]).title()
##                            ]
##
##                    except (AttributeError, KeyError):   
##
##                        continue
##
##        elif image_alt and not title and not title_split:
##
##            if self.regex.search(PROTOCOL, image):
##
##                   for name in elements:  
##
##                       try:
##
##                           element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[title]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), image,
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
##                            ]
##
##                       except (AttributeError, KeyError):
##
##                          continue
##
##            elif not self.regex.search(PROTOCOL, image):
##                
##                for name in elements:
##
##                    if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
##                        
##                        image_ = name.img.attrs[image_src_[0]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.img.attrs[image_alt]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]),  self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
##                                      ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##                    elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
##                        
##                        if name.img.attrs[image_src_[0]].endswith('.jpg'):
##
##                            image_ = name.img.attrs[image_src_[0]]
##
##                        elif name.img.attrs[image_src_[1]].endswith('.jpg'):
##
##                            image_ = name.img.attrs[image_src_[1]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.img.attrs[image_alt]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]),  self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
##                                      ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##                    elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
##                        
##                        image_ = name.img.attrs[image_src_[0]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.img.attrs[image_alt]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]),  self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.img.attrs[image_alt]).title()
##                                      ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##
##        elif title_split and not title and not image_alt:
##
##            if self.regex.search(PROTOCOL, image): 
##
##                   for name in elements:
##
##                       try:
##
##                           element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), image,
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE, name.attrs[link].split('/')[title_split]).title()
##                            ]
##
##                       except (AttributeError, KeyError):
##
##                          continue
##
##            elif not self.regex.search(PROTOCOL, image):
##
##                for name in elements:
##
##                    if MIN_CHECK[0] < len(image_src_) < MIN_CHECK[1]:
##                        
##                        image_ = name.img.attrs[image_src_[0]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE,name.attrs[link].split('/')[title_split]).title()
##                                      ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##                    elif MIDDLE_CHECK[0] < len(image_src_) < MIDDLE_CHECK[1]:
##                       
##                        if name.img.attrs[image_src_[0]].endswith('.jpg'):
##
##                            image_ = name.img.attrs[image_src_[0]]
##
##                        elif name.img.attrs[image_src_[1]].endswith('.jpg'):
##
##                            image_ = name.img.attrs[image_src_[1]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE,name.attrs[link].split('/')[title_split]).title()
##                                      ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##                    elif MAX_CHECK[0] <= len(image_src_) >= MAX_CHECK[1]:
##                        
##                        image_ = name.img.attrs[image_src_[0]]
##
##                        try:
##
##                            element_dict[self.regex.sub(CLEAN_STR,SUB_WHITE_SPACE,name.attrs[link].split('/')[title_split]).lower()] = [
##                                    self.absolute_link_single(name.attrs[link]), self.absolute_link_single(image_),
##                                    self.regex.sub(CLEAN_ALL,WHITE_SPACE,name.attrs[link].split('/')[title_split]).title()
##                                      ]
##
##                        except (AttributeError, KeyError):
##
##                            continue
##
##
##        return element_dict
#===============================================================================


    def meta_data(self, attr_selector = 'meta[name="description"]',attr_regex=None,group = 0,content = 'content',meta = 'meta',meta_single = True):
        """Return page meta data.
           
            param:
              attr_selector: meta data element to be returned default - 'meta[name="description"]'.
              This can also be specified as list of attribute selector - 'meta[name="description"], meta[name="tdate"], meta[itemprop="thumbnailUrl"]'
           
            param: attr_regex: regular expression pattern to be used to extract specific information from URL
           
            param: group: parenthesised regular expression match to be return - default = 0 

            param: content: meta data attribute to be fetch - default = content

            param: meta: page meta element to be fetch - default = meta

            param: meta_single: if set to False fetch list of match meta tags - default = True
        """

        meta_list = []

        if meta_single and len(attr_selector.split(',')) == 1:

            meta_match = self.soup(self.html(), 'html.parser').select_one(attr_selector)

            return meta_match.attrs[content] if not attr_regex else self.sieve_fetch(meta_match.attrs[content], attr_regex, group)
       
        elif meta_single and len(attr_selector.split(',')) > 1:
           
            meta_match = self.soup(self.html(), 'html.parser').select(attr_selector)
           
            if not attr_regex:
               
                for match_element in meta_match:
                   
                    meta_list.append(match_element.attrs[content])

                return meta_list
           
            elif attr_regex:

                if not '|' in attr_regex:

                    for match_element in meta_match:

                        if self.regex.search(attr_regex, match_element.attrs[content]):
                           
                            meta_list.append(self.sieve_fetch(match_element.attrs[content], attr_regex, group))

                    return meta_list

                elif '|' in attr_regex:

                    regex_list = attr_regex.split('|')

                    while regex_list: 
                   
                        for match_element in meta_match:
                           
                            meta_list.append(self.sieve_fetch(match_element.attrs[content],regex_list.pop(0) , group))

                        if not regex_list: break
           
                    return meta_list

        elif not meta_single:

            meta_match = self.soup(self.html(), 'html.parser').select(meta)

            return meta_match

if __name__ == "__main__":
               
    html = WebCrawler('http://www.hotgirlclub.com/')
    xbmc.log(html.scheme_domain)



