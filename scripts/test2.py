from brownie import accounts, config, IPFSHealthRecordV2,Intermediate, network

#int 0x0742Bc10181401Db501822696e948AA676CfEFbD
#chain1 0x97299c4f69AFcb343c30E7D7417cead45197e7C4 sep 
#chain2 0xA5468dC5C33Ebd5E1f0aD8eC862ACe74555B3B98 sep
#chain3 0x1DED0Ed4eEf28085dfB143244f9d189d47925BeA  goe

def test1():
    account = get_account()
    test = Intermediate.deploy({"from": account})

def test2():
    account = get_account()
    test = IPFSHealthRecordV2.deploy({"from": account})

def get_account():

    if network.show_active() == "development":

        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    test2()
