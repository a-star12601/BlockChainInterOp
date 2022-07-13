from brownie import accounts, config, IPFSHealthRecord, network
import json

def get_account():

    if network.show_active() == "development":

        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


account = get_account()
# chain :  0x044926296CE4841faE2601082eD7B56EC8C2c874
chain = IPFSHealthRecord.at("0xafC6EeD4C8a26a289330610b39caB0175AA5Bb52")
import ipfshttpclient
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')  # Connects to: /dns/localhost/tcp/5001/http


object2=chain.SearchRecord(1, {"from": account})
object = chain.RetFilter()
print(object)
object = list(chain.RetFilter())
res=[]
for i in object:
    print(i)
    d=client.get_json(i[0])
    print(d,type(d))
    res.append([d['DID'],d['PID'],d['Object'],d['Date'],d['Dept'],d['Prescription'],d['File']])
print(res)