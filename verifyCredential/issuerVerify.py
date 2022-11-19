from bitcoinTool import *

def hex2Str(hex):
    data = bytes.fromhex(hex).decode("utf-8")
    return data

def getTrustList(issuer_addr):
    txids = getTxids(issuer_addr)
    trust_list = []
    for txid in txids:
        tx_data = decodeTx(txid)
        #get input address
        input_addr = getInputAddr(tx_data)
        out_data = tx_data['vout']
        #get OP_RETURN type
        asm = out_data[-1]['scriptPubKey']['asm'].split()
        type = asm[0]
        #2.1. tx is 3-out with OP_Return
        if (issuer_addr != input_addr and (len(out_data)==4) and type == 'OP_RETURN'):
            a_addr = out_data[0]['scriptPubKey']['addresses'][0]
            b_addr = out_data[1]['scriptPubKey']['addresses'][0]
            revok_addr = out_data[2]['scriptPubKey']['addresses'][0]
            #2.2. check the revocation_address
            if (revok_addr != a_addr and revok_addr != b_addr):
                #3.1. get OP_RETURN data
                data = asm[-1]
                #3.2. decode the hex data and convert dict string to dict
                trust_data = json.loads(hex2Str(data))
                trust_data['address'] = input_addr
                trust_data['issueTxid'] = txid

                #4. check the revocation state
                #4.1. get all txs related to the address
                rev_txids = getTxids(revok_addr)
                for rtxid in rev_txids:
                    revok_tx = decodeTx(rtxid)
                    rev_in = revok_tx['vin']
                    rev_out = revok_tx['vout']
                    input_txid = rev_in[0]['txid']
                    index = rev_in[0]['vout']
                    #4.2. txid = issuing trust statement tx id
                    if (input_txid == txid and index == 2):
                        #4.3. get the data in OP_Return
                        asm = rev_out[-1]['scriptPubKey']['asm'].split()
                        rev_data = asm[1]
                        #decode the hex data and convert dict string to dict
                        rev_json = json.loads(hex2Str(rev_data))
                        #add/update the revocation data in OP_Return to the jsonData
                        trust_data.update(rev_json)
                        #add the txid to the jsonData
                        trust_data['revokeTxid'] = rtxid
                trust_list.append(trust_data)
    return trust_list

if __name__ == '__main__':
    issuer_addr = '2MuVNbvxJFG9JNdQykj8PjJtaktLquiU4Zx'
    infoList = getTrustList(issuer_addr)
    print("Trust List for " + issuer_addr + " :")
    print(infoList)