from brownie import accounts, config, IPFSHealthRecordV2,Intermediate, network

#int 0x3835C421B2F1E5a5732ecE5B3f9a91C21BED5581
#chain1 0x04Ac8f21145Cd347b5C06b81c616a5727C0d428d sep 
#chain2 0xE746eD7d1c94BD10410e0D1c771102aeA51Ed40E sep
#chain3 0x925f32D6DC854Cc85b0E20671B1eb81Aa43be5Bd  goe

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
    test1()
