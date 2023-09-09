import os, re
from json import dump as json_dump, load as json_load

keys_path = re.sub('\\\\sources\\\\source_three','\\\\modules\\\\keys',os.path.dirname(os.path.abspath(__file__)))
mode_keys = os.path.join(keys_path, 'modelist.json')

def load_data(filename):

    with open(filename) as fh:

        content = json_load(fh)

        return content

def view_keys(filename):

    d_data = dict()
    count = 0

    with open(filename) as fh:

        content = json_load(fh)

        for item in content:

            if count > 1:

                d_data[count] = item

            count += 1
        
        return d_data

def assign_num(filename, check_name):

    data = list(zip(view_keys(filename).keys(), view_keys(filename).values()))
    
    try:

        for item in data:

            if item[1][0][0] == check_name:

                 name = item[0]
                 
        return name
            
    except UnboundLocalError:

        print('Name not found..............')
        #xbmc.log('Name not found..............')
        return

if __name__ == "__main__":

    print(assign_num(mode_keys,'alothome'))

