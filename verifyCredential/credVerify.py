import json, hashlib, time

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

def getHash(item):
    result = hashlib.sha256(item.encode('utf-8')).hexdigest()
    return result

def getObjHash(data, hashList):
    #flatten the cred
    f_data = flatten_json(data)
    #compute hash value for each attribute and add to hashList
    hash_list = []
    for key, value in f_data.items():
        item = str(key) + ":" + str(value)
        hashed = getHash(item)
        hash_list.append(hashed)
    #combine hash list with the hash values in the "obfuscatedData"
    hash_list = hash_list + hashList
    #sort hash list
    hash_list.sort()
    #compute obj_hash
    obj_hash = getHash(str(hash_list))
    return obj_hash

def getCredHash(cred):
    option_root = ""
    privacy = cred['privacy']

    #compute root of 'data'
    data = cred['data']
    if 'data' in privacy.keys():
        dataHash = privacy['data']['dataHash']
        data_root = getObjHash(data, dataHash)
    else:
        data_root = getObjHash(data, [])

    #compute root of 'option'
    if 'option' in cred.keys():
        option = cred['option']
        option_hash = []
        for obj in option:
            optionData = obj['optionData']
            hashList = obj['hashList']
            obj_hash = getObjHash(optionData, hashList)
            #add each obj's hash to the obfuscatedData
            option_hash.append(obj_hash)
        if 'option' in privacy.keys():
            optionHash = privacy['option']['optionHash']
            option_hash = option_hash + optionHash
            option_hash.sort()
            option_root = getHash(str(option_hash))
        else:
            option_hash.sort()
            option_root = getHash(str(option_hash))
    else:
        if 'option' in privacy.keys():
            option_root = privacy['option']['optionRoot']

    #print('data root: ', data_root)
    #print('option root: ', option_root)
    #compute cred hash (Hash(data_root + option_root))
    cred_hash = getHash(str(data_root) + str(option_root))
    #print('credential credential: ', cred_hash)
    return cred_hash

def test_ourMethod():
    credPath = "data\\cred.json"
    targetHash = "d39d2c23a1cff616eb710b14d37269036b4f94d075da8696112dc3339182a6f5"
    with open(credPath) as f:
        cred = json.load(f)
    cred_hash = getCredHash(cred)
    #print("result: ", cred_hash)
    if cred_hash == targetHash:
        print("our method result: True")
    else:
        print("our method result: False")

if __name__ == '__main__':
    start_time = time.process_time()
    test_ourMethod()
    end_time = time.process_time()
    total_time = end_time - start_time
    print("total time : ", total_time)



