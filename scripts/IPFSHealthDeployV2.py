from sys import displayhook
import PySimpleGUI as sg
from brownie import accounts, config, IPFSHealthRecordV2,Intermediate, network

import json
import webbrowser

from Crypto.Cipher import PKCS1_OAEP
import Crypto
from Crypto.PublicKey import RSA
import binascii
import Crypto.Random
import brownie
from pytest import hookspec

#int 0x3835C421B2F1E5a5732ecE5B3f9a91C21BED5581
#chain1 0x04Ac8f21145Cd347b5C06b81c616a5727C0d428d sep 
#chain2 0xE746eD7d1c94BD10410e0D1c771102aeA51Ed40E sep
#chain3 0x925f32D6DC854Cc85b0E20671B1eb81Aa43be5Bd  goe

sg.theme('default1')

new = 2
chain1,chain2,chain3="0x04Ac8f21145Cd347b5C06b81c616a5727C0d428d","0xE746eD7d1c94BD10410e0D1c771102aeA51Ed40E","0x925f32D6DC854Cc85b0E20671B1eb81Aa43be5Bd"
curNetwork=network.show_active()
chain = IPFSHealthRecordV2.at(chain1)

import ipfshttpclient
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')  # Connects to: /dns/localhost/tcp/5001/http

headings = ["DID","PID","Object","Date","Dept","Prescription","File"]


def showTable(rows, height):
    table_layout = [
        [
            sg.Table(
                values=rows,
                headings=headings,
                # def_col_width=8,
                # auto_size_columns=False,
                expand_x=True,
                display_row_numbers=False,
                justification="right",
                num_rows=height,
                row_height=35,
                key='click',
                enable_events=True
            )
        ]
        
    ]

    window = sg.Window("", table_layout, modal=True, size=(500, 350))
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "click":
            data_selected = [rows[row] for row in values[event]]
            print(data_selected)  # an array like this [[6, 'Fischl', 4.0]]
            url = "http://localhost:8080/ipfs/"+str(data_selected[0][-1])
            webbrowser.open(url,new=new)
        else:
            continue
    window.close()

permission=["Sender","Receiver","Status"]
def showPerm(rows, height):
    table_layout = [
        [
            sg.Table(
                values=rows,
                headings=permission,
                # def_col_width=8,
                # auto_size_columns=False,
                expand_x=True,
                display_row_numbers=False,
                justification="right",
                num_rows=height,
                row_height=35,
                key='click2',
                enable_events=True
            )
        ]
    ]

    window = sg.Window("Permissions", table_layout, modal=True, size=(500, 350))
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "click2":
            data_selected = [rows[row] for row in values[event]]
            print(data_selected)  # an array like this [[6, 'Fischl', 4.0]]
            flip=chain.FlipFlagDataShare(data_selected[0][0],data_selected[0][1],{"from":account})
            break
        else:
            continue
    window.close()




def selfdata(uname):
    pid = chain.getPid(uname)
    object2=chain.SearchRecord(pid, {"from": account})
    object = chain.RetFilter()
    object = list(chain.RetFilter())
    res=[]
    for i in object:
        print(i)
        d=client.get_json(i[0])
        print(d,type(d))
        res.append([d['DID'],d['PID'],d['Object'],d['Date'],d['Dept'],d['Prescription'],d['File']])
    if res == []:
        sg.popup("Not Found")
    else:
        showTable(res, 10)


def open_register(flag):
    UserType = {1: "Doctor", 2: "Patient"}
    FieldSet = {1: "Department", 2: "Address"}
    layout=[[sg.Text('Enter Your Details:')],
          [sg.Text('Username:', size=(10, 1)), sg.InputText(key='-UNAME-')],
          [sg.Text('Password', size=(10, 1)), sg.InputText(key='-PASS-')],
          [sg.Text('Name:', size=(10, 1)), sg.InputText(key='-NAME-')],
          [sg.Text('ID:', size=(10, 1)), sg.InputText(key='-ID-')],
          [sg.Text(FieldSet[flag], size=(10, 1)), sg.InputText(key='-FLAG-')],
          [sg.Text('SSN:', size=(10, 1)), sg.InputText(key='-SSN-')],
          [sg.Button('Register'), sg.Button('Cancel')]]
    
    window = sg.Window("Register", layout, modal=True)
    choice = None
    while True:
        event, values = window.read(close=True)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Register":
            random_gen = Crypto.Random.new().read
            private_key = RSA.generate(2048,random_gen)
            public_key = private_key.publickey()
            response = {
                'private_key': binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
                'public_key': binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
            }
            c1 = chain.Register(
                values[0],
                values[1],
                UserType[flag],
                values[2],
                values[3],
                values[4],
                values[5],
                response["private_key"],
                response["public_key"],
                flag,
                {"from": account},
            )
            if c1 == "Already Present":
                sg.popup("Already Present")
            else:
                sg.popup("Success")
    window.close()


def open_login(uname, pword, flag):
    UserType = {1: "Doctor", 2: "Patient"}
    check = chain.Login(uname, pword)
    print(check)
    if check == "Fail" or UserType[flag]!=check:
        sg.popup("Invalid Login")
    else:
        if flag == 1:
            layout = [
                [sg.Text("Enter your choice:")],
                [sg.Button("Add"), sg.Button("Search"),sg.Button("OtherHosp")],
            ]
            window = sg.Window("Doctor View", layout, modal=True)
            choice = None
            while True:
                event, values = window.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "Add":
                    add(uname)
                if event == "Search":
                    search()
                if event == "OtherHosp":
                    external()
            window.close()
        if flag == 2:
            layout = [
                [sg.Text("Enter your choice:")],
                [sg.Button("ViewData"), sg.Button("SendData"),sg.Button("ViewShare"),sg.Button("SetPerm")],
            ]
            window = sg.Window("Patient View", layout, modal=True)
            choice = None
            while True:
                event, values = window.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "ViewData":
                    selfdata(uname)
                if event == "SendData":
                    Spid=chain.getPid(uname)                    
                    Rpid = sg.popup_get_text("Enter Receiver pid:")
                    Rpub=chain.getPubKey(Rpid)
                    if Rpub=="Not Found":
                        sg.popup("Invalid PID")
                    else:
                        object2=chain.SearchRecord(Spid, {"from": account})
                        object = chain.RetFilter()
                        object = list(chain.RetFilter())
                        res=[]
                        for i in object:
                            print(i)
                            d=client.get_json(i[0])
                            print(d,type(d))
                            res.append([d['DID'],d['PID'],d['Object'],d['Date'],d['Dept'],d['Prescription'],d['File']])
                        if res == []:
                            sg.popup("No Records")
                        else:
                            hash=client.add_json(res)
                            public_key = RSA.importKey(binascii.unhexlify(Rpub))
                            public_key=public_key.export_key('PEM')
                            rsa_public_key = RSA.importKey(public_key)
                            rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
                            message = str.encode(hash)
                            encrypted_text = rsa_public_key.encrypt(message)
                            chain.SetDataShare(Spid,Rpid,encrypted_text,{"from": account})
                if event == "ViewShare":
                    Rpid=chain.getPid(uname)                    
                    Spid = sg.popup_get_text("Enter Sender pid:")
                    Rpriv=chain.getPrivKey(Rpid)
                    try:
                        encrypted_data=chain.GetDataShare.call(Spid,Rpid,{"from": account})
                        private_key=RSA.importKey(binascii.unhexlify(Rpriv))
                        private_key=private_key.export_key('PEM')
                        rsa_private_key = RSA.importKey(private_key)
                        cipher = PKCS1_OAEP.new(rsa_private_key)
                        json=cipher.decrypt(encrypted_data)
                        json=json.decode('utf-8')
                        data=client.get_json(json)
                        showTable(data, 10)
                    except:
                        sg.popup("No records")
                if event == "SetPerm":
                    Spid=chain.getPid(uname)  
                    object=chain.ShowDS.call(Spid,{"from":account})
                    res=[]
                    for i in object:
                        res.append(i[:-1])
                    object=res
                    print(object)
                    if object == []:
                        sg.popup("Nothing Shared")
                    else:
                        showPerm(object, 10)                      
            window.close()
            


def add(uname):
    l = chain.getDid(uname)
    did, dept = l[0], l[1]
    layout=[[sg.Text('Enter Record Details:')],
          [sg.Text('Object:', size=(10, 1)), sg.InputText(key='-OBJ-')],
          [sg.Text('PID', size=(10, 1)), sg.InputText(key='-PID-')],
          [sg.Text('Prescription:', size=(10, 1)), sg.InputText(key='-PRES-')],
          [sg.Text('Date:', size=(10, 1)), sg.InputText(key='-DATE-')],
          [sg.Text('Filename', size=(10, 1)), sg.FileBrowse(key='-FILE-')],
          [sg.Button('Add'), sg.Button('Cancel')]]
    window = sg.Window("Add Record", layout,modal=True)
    while True:
        event, values = window.read(close=True)
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Add":
            obj = values['-OBJ-']
            pid = values['-PID-']
            pres = values['-PRES-']
            date = int(values['-DATE-'])
            filename = values['-FILE-']
            fhash=client.add(filename)
            print(fhash['Hash'])
            JSONContent= {'DID':did,'Dept':dept,'Object':obj,'PID':pid,'Prescription':pres,'Date':date,'File':fhash['Hash']}
            print(JSONContent)
            res = client.add_json(JSONContent)
            print(res)
            ssn=chain.getSSN(pid)
            chain.AddRecord(res,pid,ssn,{"from": account})  
            break      
    window.close()



def search():
    pid = sg.popup_get_text("Enter search pid")
    object2=chain.SearchRecord(pid, {"from": account})
    object = chain.RetFilter()
    object = list(chain.RetFilter())
    res=[]
    for i in object:
        print(i)
        d=client.get_json(i[0])
        print(d,type(d))
        res.append([d['DID'],d['PID'],d['Object'],d['Date'],d['Dept'],d['Prescription'],d['File']])
    if res == []:
        sg.popup("Not Found")
    else:
        showTable(res, 10)

def external():
    global chain
    pid = sg.popup_get_text("Enter search pid")
    SSN = chain.getSSN(pid)
    layout=[
          [sg.Button('Server 1'), sg.Button('Server 2')]]
    window = sg.Window("Select Server", layout,modal=True)
    while True:
        event, values = window.read(close=True)
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Server 1":
            network.disconnect()
            network.connect('sepolia')
            print(network.show_active())
            intermediate= Intermediate.at("0x3835C421B2F1E5a5732ecE5B3f9a91C21BED5581")
            break      
        if event == "Server 2":
            network.disconnect()
            network.connect('sepolia')
            print(network.show_active())
            intermediate= Intermediate.at("0x4C9c8d92df21E9a86Ff34Ac868C89e802807D210")
            break      
    window.close()  
    HospList=list(intermediate.GetH())
    print(HospList)
    data=[]
    for i in HospList[:-1]:
        nw,link = i[1], i[2]
        network.disconnect()
        network.connect(nw)
        print(network.show_active())
        temp=IPFSHealthRecordV2.at("0x"+link)
        object2=temp.SearchRecordSSN(SSN, {"from": account})
        object = list(temp.RetFilter())
        data+=object
    network.disconnect()
    network.connect(curNetwork)
    print(network.show_active())
    res=[]
    for i in data:
        d=client.get_json(i[0])
        res.append([d['DID'],d['PID'],d['Object'],d['Date'],d['Dept'],d['Prescription'],d['File']])
    if res == []:
        sg.popup("Not Found")
    else:
        showTable(res, 10)
    chain = IPFSHealthRecordV2.at(chain1)
    


def deploy_health():
    layout = [
        [sg.Text("UserName:"), sg.InputText()],
        [sg.Text("Password:"), sg.InputText()],
        [sg.Text("Login Type"), sg.Listbox(values=["Doctor", "Patient"])],
        [sg.Button("Login")],
        [sg.Button("Doctor Register"), sg.Button("Patient Register")],
    ]
    window = sg.Window("LOGIN", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Doctor Register":
            open_register(1)
        if event == "Patient Register":
            open_register(2)
        if event == "Login":
            print(values[2][0])
            flag = 1 if values[2][0] == "Doctor" else 2
            print(values, flag)
            open_login(values[0], values[1], flag)
    window.close()


def get_account():

    if network.show_active() == "development":

        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


account = get_account()


def main():
    deploy_health()