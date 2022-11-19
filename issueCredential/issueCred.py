import hashlib
from bitcoinTool import *

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

def getHash(data):
    result = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return result

def getCredHash(cred):
    data_hash_list = []
    option_hash_list = []
    #for 'data'
    data = cred['data']
    f_data = flatten_json(data)
    for key,value in f_data.items():
        item = str(key) + ":" + str(value)
        hash_item = getHash(item)
        data_hash_list.append(hash_item)
    #for 'option'
    if 'option' in cred.keys():
        option = cred['option']
        for obj in option:
            option_data = obj['optionData']
            f_option_data = flatten_json(option_data)
            obj_hash_list = []
            for key,value in f_option_data.items():
                item = str(key) + ":" + str(value)
                hash_item = getHash(item)
                obj_hash_list.append(hash_item)
            obj_hash_list.sort()
            hash_obj = getHash(str(obj_hash_list))
            option_hash_list.append(hash_obj)
    #sorting the hash list
    data_hash_list.sort()
    option_hash_list.sort()
    #compute data_root and option_root
    data_root = getHash(str(data_hash_list))
    option_root = getHash(str(option_hash_list))
    #print('data root: ', data_root)
    #print('option root: ', option_root)
    #compute credential hash (targetHash)
    cred_hash = getHash(str(data_root) + str(option_root))
    print("cred_hash: ", cred_hash)
    return cred_hash

def issueCred(cred, send_addr, receive_addr):
    metadata = getCredHash(cred)
    raw_txn = create_raw_txn(send_addr, receive_addr, metadata)
    result = sign_send_txn(raw_txn[0:-1])
    txid = result['txid'].strip()

    if 'error' in result:
        print('Error: ' + result['error'])
    else:
        print('TxID: ' + result['txid'])
        chain = bitcoin_cmd('getblockchaininfo')['chain']

        signature = cred['signature']
        signature['type'] = ["MerkleProof2017","Extension"]
        signature['merkleRoot'] = metadata
        signature['targetHash'] = metadata
        signature['proof'] = []
        anchors_list = []
        tx_dict = {}
        tx_dict['sourceId'] = txid
        tx_dict['type'] = "BTCOpReturn"
        tx_dict['chain'] = chain
        anchors_list.append(tx_dict)
        signature['anchors'] = anchors_list

        # write to 'signed_cred.json'
        filename = 'data\\signed_cred.json'
        with open(filename, 'w') as file_obj:
            json.dump(cred, file_obj, indent=2)
    return txid

if __name__ == '__main__':
    #store the cred_hash onto the blockchain
    send_addr = '2MytmEDSkDQhbBckb6LoATd4n1cxRxgBtXP'
    receive_addr = '2MytmEDSkDQhbBckb6LoATd4n1cxRxgBtXP'
    cred_path = "data\\cred.json"
    with open(cred_path) as f:
        cred = json.load(f)
    txid = issueCred(cred, send_addr, receive_addr)