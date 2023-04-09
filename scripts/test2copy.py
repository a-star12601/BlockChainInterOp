from brownie import accounts, config, IPFSHealthRecordV2,Intermediate, network
#int 0x0742Bc10181401Db501822696e948AA676CfEFbD
#chain1 0x97299c4f69AFcb343c30E7D7417cead45197e7C4
#chain2 0xA5468dC5C33Ebd5E1f0aD8eC862ACe74555B3B98

#gint 0x1C7B2Bd2e9ec4476D5d7c37998334d0a353cdEa2
def test1():
    account = get_account()
    test = Intermediate.at("0x3835C421B2F1E5a5732ecE5B3f9a91C21BED5581")
    HospList=list(test.GetH())
    print(HospList)
    data=[]
    for i in HospList:
        nw,link = i[1], i[2]
        network.disconnect()
        network.connect(nw)
        print(network.show_active())
        temp=IPFSHealthRecordV2.at("0x"+link)
        object2=temp.SearchRecordSSN("222222", {"from": account})
        object = list(temp.RetFilter())
        data+=object
    print(data)

def test3():
    account = get_account()
    test = Intermediate.at("0x4C9c8d92df21E9a86Ff34Ac868C89e802807D210")
    test.RegHosp("H1","sepolia","04Ac8f21145Cd347b5C06b81c616a5727C0d428d", {"from": account})
    test.RegHosp("H2","sepolia","E746eD7d1c94BD10410e0D1c771102aeA51Ed40E", {"from": account})
    test.RegHosp("H3","goerli","925f32D6DC854Cc85b0E20671B1eb81Aa43be5Bd", {"from": account})



def test2():
    print(network.show_active())
    network.disconnect()
    network.connect('sepolia')
    print(network.show_active())
    l = Intermediate.at("0x0742Bc10181401Db501822696e948AA676CfEFbD").RetHosp("Chain2")
    print(l)
    nw,link = l[0], l[1]
    network.disconnect()
    network.connect('goerli')
    print(network.show_active())
    network.disconnect()
    network.connect(nw)
    print(network.show_active())
    l2="0x"+link
    chain=IPFSHealthRecordV2.at(l2).GetPDetails()
    print(chain)
    network.disconnect()
    network.connect('goerli')
    print(network.show_active())

def get_account():

    if network.show_active() == "development":

        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    test3()
