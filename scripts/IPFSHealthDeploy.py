from sys import displayhook
import PySimpleGUI as sg
from brownie import accounts, config, IPFSHealthRecord, network
import json
import webbrowser
new = 2
# chain :  0x044926296CE4841faE2601082eD7B56EC8C2c874
chain = IPFSHealthRecord.at("0xafC6EeD4C8a26a289330610b39caB0175AA5Bb52")
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


def open_register(flag):
    UserType = {1: "Doctor", 2: "Patient"}
    FieldSet = {1: "Department", 2: "Address"}
    layout = [
        [sg.Text("Enter Your Details:")],
        [sg.Text("Username:"), sg.InputText()],
        [sg.Text("Password:"), sg.InputText()],
        [sg.Text("Name:"), sg.InputText()],
        [sg.Text("ID:"), sg.InputText()],
        [sg.Text(FieldSet[flag]), sg.InputText()],
        [sg.Text("DOBSTRING:"), sg.InputText()],
        [sg.Button("Register")],
    ]
    window = sg.Window("Register", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Register":
            c1 = chain.Register(
                values[0],
                values[1],
                UserType[flag],
                values[2],
                values[3],
                values[4],
                values[5],
                flag,
                {"from": account},
            )
            if c1 == "Already Present":
                sg.popup("Already Present")
            else:
                sg.popup("Success")
    window.close()


def open_login(uname, pword, flag):
    check = chain.Login(uname, pword)
    if check == "Fail":
        sg.popup("Invalid Login")
    else:
        if flag == 1:
            layout = [
                [sg.Text("Enter your choice:")],
                [sg.Button("Add"), sg.Button("Search"),sg.Button("SearchDept")],
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
                if event == "SearchDept":
                    searchdept(uname)
            window.close()
        if flag == 2:
            pid = chain.getPid(uname)
            chain.SearchRecord(pid, {"from": account})
            object = list(chain.RetFilter())
            if object == []:
                sg.popup("No Records")
            else:
                showTable(object, 10)

print("UserList:",end="")
print(chain.RetUser())
print("patientList:",end="")
print(chain.GetPDetails())
print("DoctorList:",end="")
print(chain.GetDDetails())


def add(uname):
    l = chain.getDid(uname)
    did, dept = l[0], l[1]
    obj = sg.popup_get_text("Enter obj:")
    pid = sg.popup_get_text("Enter pid:")
    pres = sg.popup_get_text("Enter pres:")
    date = int(sg.popup_get_text("Enter date:"))
    filename = sg.popup_get_file('Select a file containing Python code:')
    fhash=client.add(filename)
    print(fhash['Hash'])
    JSONContent={'DID':did,'Dept':dept,'Object':obj,'PID':pid,'Prescription':pres,'Date':date,'File':fhash['Hash']}
    print(JSONContent)
    res = client.add_json(JSONContent)
    print(res)
    chain.AddRecord(res,pid,{"from": account})


def show():
    details = chain.GetAllRecords()
    # sg.popup(details)
    showTable(details, 10)
    print(details)


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

def searchdept(uname):
    l = chain.getDid(uname)
    dept=l[1]
    chain.SearchRecorddept(dept, {"from": account})
    object = chain.RetFilter()
    object = list(chain.RetFilter())
    res = [i for i in object if i != ("", "", "", "", "", "", 0)]
    object = res
    print(object)
    if object == []:
        sg.popup("Not Found")
    else:
        showTable(object, 10)


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