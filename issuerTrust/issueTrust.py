from bitcoinTool import *
import hashlib

def getHash(data):
    result = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return result

def issueTrust(send_addr, trust_addr, revoke_addr):
    data = {"trust":True,"name":"Lily","url":"www.example.com/lily"}
    hash_data = getHash(str(data))

    raw_txn = create_raw_txn(send_addr, trust_addr, revoke_addr, hash_data)
    result = sign_send_txn(raw_txn[0:-1])
    txid = result['txid'].strip()

    if 'error' in result:
        print('Error: ' + result['error'])
    else:
        print('TxID: ' + result['txid'])

    return txid

if __name__ == '__main__':

    send_addr = '2N5um1vT5RvfPX5TgURhh2TAe4h4z9tgYD7'
    trust_addr = '2MytmEDSkDQhbBckb6LoATd4n1cxRxgBtXP'
    revoke_addr = '2MxDw85MtHfizdx1iNEKadmGb5kHJDByhty'

    txid = issueTrust(send_addr, trust_addr, revoke_addr)
