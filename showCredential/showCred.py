import json, hashlib, re

def flatten_json(data):
    out = {}
    def flatten(x, name=''):
        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(data)
    return out

def unflatten_json(data):
    d = {}
    for key, value in data.items():
        s = d
        tokens = re.findall(r'\w+', key)
        for count, (index, next_token) in enumerate(zip(tokens, tokens[1:] + [value]), 1):
            value = next_token if count == len(tokens) else [] if next_token.isdigit() else {}
            if isinstance(s, list):
                index = int(index)
                while index >= len(s):
                    s.append(value)
            elif index not in s:
                s[index] = value
            s = s[index]
    return d

def getHash(data):
    result = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return result

def showCred(cred):
    #construct new selected_cred
    selected_cred = {}
    data_hash = []
    option_root = ""
    option_hash = []
    data_list = [] #store the keys in 'data'
    data_hidden_key = [] #store the hidden keys in 'data'
    option_list = [] #store the keys in 'option'
    option_hidden_key = [] #store the hidden keys in 'option'

    #for 'data' (display data's attributes and select attribute to hide)
    data = cred['data']
    f_data = flatten_json(data)
    for index,item in enumerate(f_data.items()):
        data_list.append(item[0])
        item = item[0] + ":" + item[1]
        print(str(index) + ' -> ' + str(item))
    #get the index for hidden attributes
    data_hidden_index = input('Select attribute to hide (enter no. with space):')
    data_hidden_index = data_hidden_index.split()
    #get 'key' of the hidden attributes
    for index,key in enumerate(data_list):
        if str(index) in data_hidden_index:
            data_hidden_key.append(key)

    #for option (display option's attributes and select attribute to hide)
    if 'option' in cred.keys():
        option = cred['option']
        """
        #display option's attrs
        for i, obj in enumerate(option):
            option_data = obj['optionData']
            f_option_data = flatten_json(option_data)
            for j, item in enumerate(f_option_data.items()):
                #add all option's key to option_list with index(i,j)
                option_list.append(str(i) + '.' + str(j) + '|' + item[0])
                item = item[0] + ":" + item[1]
                #for option (display option's attributes and select attribute to hide)
                print(str(i) + '.' + str(j) + ' -> ' + str(item))
        """
        option_hide = input('Want to hide the whole option part? y/n: ')
        if option_hide == 'y': #hide the whole option part
            option_hash_list = []
            for obj in option:
                option_data = obj['optionData']
                f_option_data = flatten_json(option_data)
                obj_hash_list = []
                for item in f_option_data.items():
                    item = item[0] + ":" + item[1]
                    hash_item = getHash(item)
                    obj_hash_list.append(hash_item)
                obj_hash_list.sort()
                hash_obj = getHash(str(obj_hash_list))
                option_hash_list.append(hash_obj)
            option_hash_list.sort()

            option_root = getHash(str(option_hash_list))
            del cred['option']
        else:#hide some attributes in 'option'
            #get the index for hidden attributes
            option_hidden_index = input('Select which attribute to hide (enter no. with space):')
            option_hidden_index = option_hidden_index.split()
            #get 'key' of the hidden attributes with index ('i.j.key')
            for attr in option_list:
                attr = attr.split('|')
                index = attr[0]
                key = attr[1]
                if str(index) in option_hidden_index:
                    option_hidden_key.append(index + '.' + key)
            #print('option_hidden_key: ', option_hidden_key)

    #update data (delete hidden attrs and compute hash for hidden attrs)
    if (len(data_hidden_key) > 0):
        new_f_data = f_data.copy()
        for key,value in f_data.items():
            if str(key) in data_hidden_key:
                item = str(key) + ":" + str(value)
                hash_value = getHash(item)
                data_hash.append(hash_value)
                #delete hidden attr
                del new_f_data[str(key)]

        new_data = unflatten_json(new_f_data)
        selected_cred['data'] = new_data
    else:
        selected_cred['data'] = cred['data']

    #update option (delete hidden attrs and compute hash for hidden attrs)
    if (len(option_hidden_key) > 0):
        option = cred['option']
        new_option = []
        for i, obj in enumerate(option):
            option_data = obj['optionData']
            f_option_data = flatten_json(option_data)
            new_f_option_data = f_option_data.copy()
            hash_list = []
            for j, key in enumerate(f_option_data):
                option_key = str(i) + '.' + str(j) + '.' + key
                if option_key in option_hidden_key:
                    value = f_option_data[key]
                    item = key + ":" + value
                    hash_value = getHash(item)
                    hash_list.append(hash_value)
                    #delete hidden attr
                    del new_f_option_data[key]
            #update option's obj
            new_option_data = unflatten_json(new_f_option_data)
            if (len(new_option_data) > 0):
                obj['optionData'] = new_option_data
                obj['hashList'] = hash_list
                new_option.insert(i, obj)
            else:
                hash_list.sort()
                hash_obj = getHash(str(hash_list))
                option_hash.append(hash_obj)

        selected_cred['option'] = new_option
    else:
        if ('option' in cred.keys()):
            selected_cred['option'] = cred['option']

    #update 'privacy'
    selected_cred['privacy'] = {}
    if len(data_hash) > 0:
        selected_cred['privacy']['data'] = {}
        selected_cred['privacy']['data']['dataHash'] = data_hash
    if len(option_root) > 0:
        selected_cred['privacy']['option'] = {}
        selected_cred['privacy']['option']['optionRoot'] = option_root
    if len(option_hash) > 0:
        selected_cred['privacy']['option'] = {}
        selected_cred['privacy']['option']['optionHash'] = option_hash

    selected_cred['signature'] = cred['signature']

    #write to 'selected_cred.json'
    with open("data\\selected_cred.json", 'w') as f:
        json.dump(selected_cred, f, indent=2)

if __name__ == '__main__':
    cred_path = "data\\signed_cred.json"
    with open(cred_path) as f:
        cred = json.load(f)

    showCred(cred)