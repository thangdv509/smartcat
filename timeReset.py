from web3 import Web3
from web3.middleware import geth_poa_middleware 
import config
from datetime import datetime

web3 = Web3(Web3.HTTPProvider(config.provider))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
from time import sleep

if web3.is_connected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")

# Create smart contract instance
contract = web3.eth.contract(address=config.contract_address, abi=config.abi)

# initialize the chain id, we need it to build the transaction for replay protection
Chain_id = web3.eth.chain_id

def getNonce(publicKey):
    return web3.eth.get_transaction_count(publicKey)

def task():
    maxTimestampMain = 0
    maxTimestampPeer = 0
    totalPointMain = 0
    totalPointPeer = 0
    catLevelMain = []
    catLevelPeer = []
    mainWallet = config.wallet1
    peerWallet = config.wallet2

    walletCat = mainWallet['catId']
    
    print(walletCat)
    print(f"======================CAT INFORMATION=======================")
    
    print("*" * 50)
    print("Wallet 1")
    print("*" * 50)
    for i in range(len(walletCat)):
        catId = mainWallet['catId'][i]
        catStatus = contract.functions.getCatInfo2(catId).call()

        print("-" * 50)
        print("Cat Number: " + str(i+1))
        print("Cat Id: " + str(catId))
        print("Cat Level: " + str(catStatus[0][0]))
        print("Num Feeds: " + str(catStatus[0][1]))
        print("Num Plays: " + str(catStatus[0][3]))
        print("Num Cleans: " + str(catStatus[0][5]))
        print("Points: " + str(catStatus[1]))
        print("Time reset: " + str(datetime.fromtimestamp(catStatus[2])))

        totalPointMain += catStatus[1]
        catLevelMain.append(catStatus[0][0])
        if catStatus[2] > maxTimestampMain:
            maxTimestampMain = catStatus[2]


    walletCat = peerWallet['catId']
    print("*" * 50)
    print("Wallet 2")
    print("*" * 50)
    for i in range(len(walletCat)):
        catId = peerWallet['catId'][i]
        catStatus = contract.functions.getCatInfo2(catId).call()

        print("-" * 50)
        print("Cat Number: " + str(i+1))
        print("Cat Id: " + str(catId))
        print("Cat Level: " + str(catStatus[0][0]))
        print("Num Feeds: " + str(catStatus[0][1]))
        print("Num Plays: " + str(catStatus[0][3]))
        print("Num Cleans: " + str(catStatus[0][5]))
        print("Points: " + str(catStatus[1]))
        print("Time reset: " + str(datetime.fromtimestamp(catStatus[2])))

        catLevelPeer.append(catStatus[0][0])
        totalPointPeer += catStatus[1]
        if catStatus[2] > maxTimestampPeer:
            maxTimestampPeer = catStatus[2]

    print(f"======================NEXT TIMESTAMP=======================")
    print("Wallet 1: " + str(datetime.fromtimestamp(maxTimestampMain)) + " with point - " + str(totalPointMain))
    print("Cat level wallet 1: " + mainWallet['publicKey'])
    print(catLevelMain)
    print("***********************************************************")
    print("Wallet 2: " + str(datetime.fromtimestamp(maxTimestampPeer)) + " with point - " + str(totalPointPeer))
    print("Cat level wallet 2: " + peerWallet['publicKey'])
    print(catLevelPeer)

task()
print("\n")
print("END. Thanks")
print("\n")
