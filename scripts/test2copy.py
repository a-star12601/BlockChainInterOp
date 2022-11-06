from brownie import accounts, config, IPFSHealthRecordV2,Intermediate, network
#int 0x0742Bc10181401Db501822696e948AA676CfEFbD
#chain1 0x97299c4f69AFcb343c30E7D7417cead45197e7C4
#chain2 0xA5468dC5C33Ebd5E1f0aD8eC862ACe74555B3B98
def test1():
    account = get_account()
    test = Intermediate.at("0x0742Bc10181401Db501822696e948AA676CfEFbD")
    test.RegHosp("Chain3","goerli","1DED0Ed4eEf28085dfB143244f9d189d47925BeA",{"from": account})
    a=test.RetHosp("Chain3")
    print(a)
    print(test.GetH())

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
    test1()
