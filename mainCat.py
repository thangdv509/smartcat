from web3 import Web3
from web3.middleware import geth_poa_middleware 
import config

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

wallet1 = config.wallet1
wallet2 = config.wallet2
wallet1['status'] = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
wallet2['status'] = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
print(wallet1)

def getNonce(publicKey):
    return web3.eth.get_transaction_count(publicKey)

def task():
    wallet1['status'] = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    wallet2['status'] = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    for walletOrder in range(0,2):
        if walletOrder == 1:
            mainWallet = wallet1
            peerWallet = wallet2
        else:
            mainWallet = wallet2
            peerWallet = wallet1

        walletCat = mainWallet['catId']

        while(len(walletCat) >  mainWallet['status'].count(True)):

            print(f"=======================WALLET {walletOrder + 1}=======================")
            print("Number of completed cat: " + str(mainWallet['status'].count(True)))

            for i in range(len(walletCat)):
                if mainWallet['status'][i]:
                    continue

                mainCatId = mainWallet['catId'][i]
                peerCatId = peerWallet['catId'][i]
                mainPublicKey = mainWallet['publicKey']
                peerPublicKey = peerWallet['publicKey']
                mainPrivateKey = mainWallet['privateKey']
                peerPrivateKey = peerWallet['privateKey']

                catStatus = contract.functions.catStates(mainCatId).call()
                print("*" * 50)
                print("Pair number: " + str(i + 1))
                print("*" * 50)
                print("-" * 50)
                print("Cat Id: " + str(mainCatId))
                print("Cat Level: " + str(catStatus[0]))
                print("Num Feeds: " + str(catStatus[1]))
                print("Num Plays: " + str(catStatus[3]))
                print("Num Cleans: " + str(catStatus[5]))

                print("\n")
                
                peerCatStatus = contract.functions.catStates(peerCatId).call()
                print("Peer Cat Id: " + str(peerCatId))
                print("Peer Cat Level: " + str(peerCatStatus[0]))
                print("Peer Num Feeds: " + str(peerCatStatus[1]))
                print("Peer Num Plays: " + str(peerCatStatus[3]))
                print("Peer Num Cleans: " + str(peerCatStatus[5]))

                print("\n")

                if catStatus[0] > peerCatStatus[0]: 
                    mainWallet['status'][i] = True
                    continue

                if catStatus[0] >= 15:
                
                    feedStatus = contract.functions.canFeed(mainCatId).call();
                    playStatus = contract.functions.canPlay(mainCatId).call();
                    peerPlayStatus = contract.functions.canPlay(peerCatId).call();
                    cleanStatus = contract.functions.canClean(mainCatId).call();
                    
                    if catStatus[3] < (catStatus[0] - 14) * 15 + 14 * 5 and playStatus and peerPlayStatus :
                        print("* Start inviting cat " + str(mainCatId) + " with cat " + str(peerCatId))
                        pendingList = contract.functions.getPendingInvitesList(mainCatId).call();
                        pendingIdList = []
                        for id in pendingList:
                            pendingIdList.append(id[0])
                        if(peerCatId in pendingIdList):
                            print("Already invite!")
                        else:
                            inviteTransaction = contract.functions.inviteCatForPlaying(mainCatId, peerCatId).build_transaction({
                                    'chainId': Chain_id,
                                    'from': mainPublicKey,
                                    'nonce': getNonce(mainPublicKey)
                                })
                            invite_signed_txn = web3.eth.account.sign_transaction(inviteTransaction, private_key=mainPrivateKey)
                            tx_receipt = web3.eth.send_raw_transaction(invite_signed_txn.rawTransaction)
                            print("Successful invite cat!")
                            print("Tx hash: " + tx_receipt.hex())

                        sleep(15)

                        for j in range(0, 10):
                            try:
                                acceptTransaction = contract.functions.acceptPlayDate(peerCatId, mainCatId).build_transaction({
                                        'chainId': Chain_id,
                                        'from': peerPublicKey,
                                        'nonce': getNonce(peerPublicKey)
                                    })
                                accept_signed_txn = web3.eth.account.sign_transaction(acceptTransaction, private_key=peerPrivateKey)
                                tx_receipt = web3.eth.send_raw_transaction(accept_signed_txn.rawTransaction)
                                print("Successful accept invite")
                                print("Tx hash: " + tx_receipt.hex())
                                break
                            except:
                                sleep(5)
                                print("Fail to accept. Trying again!")
                        sleep(15)

                    if catStatus[1] < (catStatus[0] - 14) * 21 + 14 * 7 and feedStatus :
                        print("* Start feeding cat " + str(mainCatId))
                        feedTransaction = contract.functions.feedCat(mainCatId).build_transaction({
                                'chainId': Chain_id,
                                'from': mainPublicKey,
                                'nonce': getNonce(mainPublicKey)
                            })
                        feed_signed_txn = web3.eth.account.sign_transaction(feedTransaction, private_key=mainPrivateKey)
                        tx_receipt = web3.eth.send_raw_transaction(feed_signed_txn.rawTransaction)
                        print("Successful feed cat " + str(mainCatId))
                        print("Tx hash: " + tx_receipt.hex())
                        sleep(15)
                    
                    if catStatus[5] < (catStatus[0] - 14) * 6 + 14 * 2 and cleanStatus :
                        print("* Start cleaning cat " + str(mainCatId))
                        cleanTransaction = contract.functions.cleanCat(mainCatId).build_transaction({
                                'chainId': Chain_id,
                                'from': mainPublicKey,
                                'nonce': getNonce(mainPublicKey)
                            })
                        clean_signed_txn = web3.eth.account.sign_transaction(cleanTransaction, private_key=mainPrivateKey)
                        tx_receipt = web3.eth.send_raw_transaction(clean_signed_txn.rawTransaction)
                        print("Successful clean cat " + str(mainCatId))
                        print("Tx hash: " + tx_receipt.hex())
                        sleep(15)

                    levelStatus = contract.functions.canLevelUp(mainCatId).call();
                    
                    if levelStatus: 
                        print("* Start leveling up cat " + str(mainCatId))
                        levelTransaction = contract.functions.levelUp(mainCatId).build_transaction({
                                'chainId': Chain_id,
                                'from': mainPublicKey,
                                'nonce': getNonce(mainPublicKey)
                            })
                        levelup_signed_txn = web3.eth.account.sign_transaction(levelTransaction, private_key=mainPrivateKey)
                        tx_receipt = web3.eth.send_raw_transaction(levelup_signed_txn.rawTransaction)
                        print("Successful level up cat " + str(mainCatId))
                        print("Tx hash: " + tx_receipt.hex())
                        sleep(15)
                            
                    if (catStatus[1] >= catStatus[0] * 7 and catStatus[3] >= catStatus[0] * 5 and catStatus[5] >= catStatus[0] * 2) or (not feedStatus and not playStatus and not cleanStatus):
                        mainWallet['status'][i] = True

                    print("-" * 50)
                    sleep(5)
                    
                else: 
                    feedStatus = contract.functions.canFeed(mainCatId).call();
                    playStatus = contract.functions.canPlay(mainCatId).call();
                    peerPlayStatus = contract.functions.canPlay(peerCatId).call();
                    cleanStatus = contract.functions.canClean(mainCatId).call();
                    
                    if catStatus[3] < catStatus[0] * 5 and playStatus and peerPlayStatus :
                        print("* Start inviting cat " + str(mainCatId) + " with cat " + str(peerCatId))
                        pendingList = contract.functions.getPendingInvitesList(mainCatId).call();
                        pendingIdList = []
                        for id in pendingList:
                            pendingIdList.append(id[0])
                        if(peerCatId in pendingIdList):
                            print("Already invite!")
                        else:
                            inviteTransaction = contract.functions.inviteCatForPlaying(mainCatId, peerCatId).build_transaction({
                                    'chainId': Chain_id,
                                    'from': mainPublicKey,
                                    'nonce': getNonce(mainPublicKey)
                                })
                            invite_signed_txn = web3.eth.account.sign_transaction(inviteTransaction, private_key=mainPrivateKey)
                            tx_receipt = web3.eth.send_raw_transaction(invite_signed_txn.rawTransaction)
                            print("Successful invite cat!")
                            print("Tx hash: " + tx_receipt.hex())

                        sleep(15)

                        for j in range(0, 10):
                            try:
                                acceptTransaction = contract.functions.acceptPlayDate(peerCatId, mainCatId).build_transaction({
                                        'chainId': Chain_id,
                                        'from': peerPublicKey,
                                        'nonce': getNonce(peerPublicKey)
                                    })
                                accept_signed_txn = web3.eth.account.sign_transaction(acceptTransaction, private_key=peerPrivateKey)
                                tx_receipt = web3.eth.send_raw_transaction(accept_signed_txn.rawTransaction)
                                print("Successful accept invite")
                                print("Tx hash: " + tx_receipt.hex())
                                break
                            except:
                                sleep(5)
                                print("Fail to accept. Trying again!")
                        sleep(15)

                    if catStatus[1] < catStatus[0] * 7 and feedStatus :
                        print("* Start feeding cat " + str(mainCatId))
                        feedTransaction = contract.functions.feedCat(mainCatId).build_transaction({
                                'chainId': Chain_id,
                                'from': mainPublicKey,
                                'nonce': getNonce(mainPublicKey)
                            })
                        feed_signed_txn = web3.eth.account.sign_transaction(feedTransaction, private_key=mainPrivateKey)
                        tx_receipt = web3.eth.send_raw_transaction(feed_signed_txn.rawTransaction)
                        print("Successful feed cat " + str(mainCatId))
                        print("Tx hash: " + tx_receipt.hex())
                        sleep(15)
                    
                    if catStatus[5] < catStatus[0] * 2 and cleanStatus :
                        print("* Start cleaning cat " + str(mainCatId))
                        cleanTransaction = contract.functions.cleanCat(mainCatId).build_transaction({
                                'chainId': Chain_id,
                                'from': mainPublicKey,
                                'nonce': getNonce(mainPublicKey)
                            })
                        clean_signed_txn = web3.eth.account.sign_transaction(cleanTransaction, private_key=mainPrivateKey)
                        tx_receipt = web3.eth.send_raw_transaction(clean_signed_txn.rawTransaction)
                        print("Successful clean cat " + str(mainCatId))
                        print("Tx hash: " + tx_receipt.hex())
                        sleep(15)

                    levelStatus = contract.functions.canLevelUp(mainCatId).call();
                    
                    if levelStatus: 
                        print("* Start leveling up cat " + str(mainCatId))
                        levelTransaction = contract.functions.levelUp(mainCatId).build_transaction({
                                'chainId': Chain_id,
                                'from': mainPublicKey,
                                'nonce': getNonce(mainPublicKey)
                            })
                        levelup_signed_txn = web3.eth.account.sign_transaction(levelTransaction, private_key=mainPrivateKey)
                        tx_receipt = web3.eth.send_raw_transaction(levelup_signed_txn.rawTransaction)
                        print("Successful level up cat " + str(mainCatId))
                        print("Tx hash: " + tx_receipt.hex())
                        sleep(15)
                            
                    if (catStatus[1] >= catStatus[0] * 7 and catStatus[3] >= catStatus[0] * 5 and catStatus[5] >= catStatus[0] * 2) or (not feedStatus and not playStatus and not cleanStatus):
                        mainWallet['status'][i] = True

                    print("-" * 50)
                    sleep(5)
            sleep(60)
        
for time in range(0, 50):
    try:
        task()
    except:
        print("&&&&&&&&&&&&&&&&&&&&&&& FAIL TO COMPELTE! I'M TRYING AGAIN &&&&&&&&&&&&&&&&&&&&&&&")

task()
print("\n")
print("END. Thanks")
print("\n")
