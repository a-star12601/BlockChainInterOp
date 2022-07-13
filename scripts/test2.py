from brownie import accounts, config, IPFSHealthRecordV2, network

#0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87

#0xd3E04fb6002065440eae96c1D02938e5BCB0fD76

#V2:0xe7c958822a9f58e9C35b2B0a5cB1027FF14C921b

#V2new:0x854D67F4375Fc9eD089366Fa70cbd6cA0D465843
def test1():
    account = get_account()
    test = IPFSHealthRecordV2.deploy({"from": account})


def get_account():

    if network.show_active() == "development":

        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    test1()
