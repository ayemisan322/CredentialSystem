# OP_RETURN.py
#
# Python script to generate and retrieve OP_RETURN bitcoin transactions
#
# Copyright (c) Coin Sciences Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#coinspark/python-OP_RETURN (OP_RETURN.py)
#https://github.com/coinspark/python-OP_RETURN/blob/master/OP_RETURN.py

import subprocess, json

"""
# Python 2-3 compatibility logic

try:
    basestring
except NameError:
    basestring = str
"""

# User-defined quasi-constants
BITCOIN_IP = '127.0.0.1'  # IP address of your bitcoin node

BITCOIN_PATH = 'D:\\Bitcoin\\daemon\\bitcoin-cli'  # path to bitcoin-cli executable on this server

BTC_FEE = 0.0001  # BTC fee to pay per transaction
BTC_DUST = 0.00001  # omit BTC outputs smaller than this

MAX_BYTES = 80  # maximum bytes in an OP_RETURN (80 as of Bitcoin 0.11)
MAX_BLOCKS = 10  # maximum number of blocks to try when retrieving data

NET_TIMEOUT = 10  # how long to time out (in seconds) when communicating with bitcoin node

#bitcoin-cmd
def bitcoin_cmd(command, *args):  # more params are read from here

    sub_args = [BITCOIN_PATH]

    sub_args.append(command)

    for arg in args:
        #sub_args.append(json.dumps(arg) if isinstance(arg, (dict, list, tuple)) else str(arg))
        sub_args.append(json.dumps(arg) if isinstance(arg, (dict, list, tuple, int)) else str(arg))

    raw_result = subprocess.check_output(sub_args).decode("utf-8").rstrip("\n")

    try:  # decode JSON if possible
        result = json.loads(raw_result)
    except ValueError:
        result = raw_result

    return result

#get all tx (listreceivedbyaddress)
def getTxids(addr):
    txList = bitcoin_cmd('listreceivedbyaddress')
    for tx in txList:
        txaddr = tx['address']
        if addr == txaddr:
            txids = tx['txids']
            break
    return txids

#decode raw transaction
def decodeTx(txid):
    tx = bitcoin_cmd('gettransaction', str(txid))
    tx_data = bitcoin_cmd('decoderawtransaction', tx['hex'])
    return tx_data

def getInputAddr(decode_tx_data):
    in_data = decode_tx_data['vin']
    in_txid = in_data[0]['txid']
    out_index = in_data[0]['vout']
    in_tx_data = decodeTx(in_txid)
    tx_out = in_tx_data['vout'][out_index]['scriptPubKey']
    input_addr = tx_out['addresses'][0]
    return input_addr

def test():
    txids = getTxids("2MuVNbvxJFG9JNdQykj8PjJtaktLquiU4Zx")
    print("txList:", txids)

if __name__ == '__main__':
    test()
