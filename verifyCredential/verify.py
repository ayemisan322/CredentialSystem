from credVerify import *
from issuerVerify import *
from bitcoinTool import *

def verify(cred):
    cred_result = False
    issuer_result = False
    result = False
    trust_list = []
    #credential verification
    #compute hash of the credential
    cred_hash = getCredHash(cred)
    #print('cred_hash: ', cred_hash)
    txid = cred['signature']['anchors'][0]['sourceId']
    #get the OP_Return data
    tx_data = decodeTx(txid)
    asm = tx_data['vout'][-1]['scriptPubKey']['asm'].split()
    data = asm[1]
    #print('data: ', data)
    #compare the cred_hash with the data from the blockchain
    if cred_hash == data:
        cred_result = True

    #issuer verification
    #get issuer addr from credential
    issuer = cred['data']['issuers'][0]['address']
    issuer_addr = issuer.split(':')[-1]
    #get sender addr from blockchain
    #here we can use blockcyhper api but now we decode the tx
    sender = getInputAddr(tx_data)
    if (issuer_addr == sender):
        issuer_result = True
        trust_list = getTrustList(issuer_addr)

    if cred_result and issuer_result:
        result = True
    return result, trust_list

if __name__ == '__main__':
    credPath = "data\\cred.json"
    with open(credPath) as f:
        cred = json.load(f)
    result, trust_list = verify(cred)
    if result:
        print("\ncredential verification: ", result)
        print("\nissuer trust list: ")
        for list in trust_list:
            print(list)
    else:
        print("credential verification: ", result)