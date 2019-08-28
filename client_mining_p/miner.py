import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 
def proof_of_work(last_block_string):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    
    :return: <int> A valid proof
    """
    proof = 0
    while valid_proof(last_block_string, proof) is False:
        proof += 1

    return proof

def valid_proof(last_block_string, proof):
    """
    Validates the Proof:  Does hash(last_block_string, proof) contain 6
    leading zeroes?
    
    :param proof: <string> The proposed proof
    :return: <bool> Return true if the proof is valid, false if it is not
    """
    h = hashlib.sha256(f'{last_block_string}{proof}'.encode()).hexdigest()
    if h[0:6] == '000000':
        return True

    return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"
    
    MINE_URL = node + "/mine"
    LAST_BLOCK_STRING_URL = node + "/last_block_string"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        
        # generate request with last block string
        r = requests.get(url=LAST_BLOCK_STRING_URL)
        data = r.json()
        last_block_string = data['last_block_string']

        # Look for a new one
        print("Working on a new proof...")
        new_proof = proof_of_work(last_block_string)
        print("Received a new proof...")
        
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        proof_data = {
            "proof": new_proof
        }

        r = requests.post(url=MINE_URL, json=proof_data)
        data = r.json()

        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data.get('message') == "New Block Forged":
            coins_mined += 1
            print("You have: " + str(coins_mined) + " coins")
        print(data.get('message'))
