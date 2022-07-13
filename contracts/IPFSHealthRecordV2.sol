// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;
pragma experimental ABIEncoderV2;


contract IPFSHealthRecordV2 {
    //  USERS PART //
    struct users {
        string username;
        bytes32 password;
        string usertype;
    }
    users[] public UserList;

    function RetUser() public view returns (users[] memory) {
        return UserList;
    }

    function Login(string memory uname, string memory pass)
        public
        view
        returns (string memory)
    {
        uint256 i;

        for (i = 0; i < UserList.length; i++) {
            users memory User = UserList[i];
            if (
                (keccak256(abi.encodePacked(User.username)) ==
                    keccak256(abi.encodePacked(uname))) &&
                (User.password ==
                    keccak256(abi.encodePacked(pass)))
            ) {
                return "Success";
            }
        }
        return "Fail";
    }

    function Register(
        string memory uname,
        string memory pass,
        string memory utype,
        string memory name,
        string memory id,
        string memory var1,
        string memory dob,
        string memory privkey,
        string memory pubkey,
        uint256 flag
    ) public returns (string memory) {
        uint256 i;
        for (i = 0; i < UserList.length; i++) {
            users memory User = UserList[i];
            if (
                keccak256(abi.encodePacked((User.username))) ==
                keccak256(abi.encodePacked(uname))
            ) {
                return "Already Present";
            }
        }
        
        UserList.push(users(uname,keccak256(abi.encodePacked((pass))) , utype));
        if (flag == 1) {
            DDetails.push(doctor(uname, name, id, var1, dob,privkey,pubkey));
            return "Success";
        } else {
            PDetails.push(patient(uname, name, id, var1, dob,privkey,pubkey));
            return "Success";
        }
    }

    // DOCTOR PART //
    struct doctor {
        string uname;
        string name;
        string DID;
        string dept;
        string dob;
        string privkey;
        string pubkey;
    }
    doctor[] public DDetails;

    struct patient {
        string uname;
        string name;
        string PID;
        string addr;
        string dob;
        string privkey;
        string pubkey;
    }
    patient[] public PDetails;

    function GetPDetails() public view returns (patient[] memory) {
        return PDetails;
    }

    function GetDDetails() public view returns (doctor[] memory) {
        return DDetails;
    }

    function getPid(string memory uname) public view returns (string memory) {
        uint256 i;
        for (i = 0; i < PDetails.length; i++) {
            patient memory P = PDetails[i];
            if (
                keccak256(abi.encodePacked((P.uname))) ==
                keccak256(abi.encodePacked(uname))
            ) {
                return P.PID;
            }
        }
        return "Not Found";
    }

    function getDid(string memory uname)
        public
        view
        returns (string memory, string memory)
    {
        uint256 i;
        for (i = 0; i < DDetails.length; i++) {
            doctor memory D = DDetails[i];
            if (
                keccak256(abi.encodePacked((D.uname))) ==
                keccak256(abi.encodePacked(uname))
            ) {
                return (D.DID, D.dept);
            }
        }
        return ("None","None");
    }
    


    //  EHR PART //
    
    struct hashtable {			//structure containing pid and corresponding indexes
        string pid;
        uint256[] indexes;
    }
    hashtable[] public HashList;		//array of structures

    
    struct phealthrec {
        string Hash;
        string PID;
    }
    phealthrec[] public Records;

    // mapping

    function AddRecord(

        string memory hashval,
        string memory pid
    ) public {
        Records.push(phealthrec(hashval,pid));
        uint256 i;
        uint256 flag = 0;
        for (i = 0; i < HashList.length; i++) {				//iterate through hashtable
            if (
                keccak256(abi.encodePacked((HashList[i].pid))) ==
                keccak256(abi.encodePacked(pid))
            ) {								//if present
                HashList[i].indexes.push(Records.length);			//add index to pid in hashtable
                flag = 1;							//set the flag
                break;
            }    

        }
        if (flag != 1) {							//if flag not set(not present)
            uint256[] memory arr = new uint256[](1);
            arr[0] = Records.length;
            HashList.push(hashtable(pid, arr));				//create new entry in hashtable
        }

    }

    function GetAllRecords() public view returns (phealthrec[] memory) {
        return Records;
    }

    phealthrec[] public FilteredData;
    phealthrec[] public Empty;

    function RetFilter() public view returns (phealthrec[] memory) {
        return FilteredData;
    }

    function SearchRecord(string memory pid)
        public
        returns (phealthrec[] memory)
    {
        uint256 i;
        uint256 j;
        FilteredData = Empty;						//clear  FilteredData
 
        for (i = 0; i < HashList.length; i++) {				//iterate through Hashtable
            if (
                keccak256(abi.encodePacked((HashList[i].pid))) ==
                keccak256(abi.encodePacked(pid))				//if pid matches
            ) {
                for (j = 0; j < HashList[i].indexes.length; j++) {		//iterate through indexes
                    FilteredData.push(Records[HashList[i].indexes[j] - 1]);	
                }					//push record present in the index to FilteredData
            }
        }
        return FilteredData;
    }


    //encryption+sharing

    struct datasharing {
        string SenderPID;
        string ReceiverPID;
        int256 flag;
        bytes data;
    }
    datasharing[] public SharedData;

    function getPubKey(string memory pid) public view returns (string memory) {
        uint256 i;
        for (i = 0; i < PDetails.length; i++) {
            patient memory P = PDetails[i];
            if (
                keccak256(abi.encodePacked((P.PID))) ==
                keccak256(abi.encodePacked(pid))
            ) {
                return P.pubkey;
            }
        }
        return "Not Found";
    }

    function getPrivKey(string memory pid) public view returns (string memory) {
        uint256 i;
        for (i = 0; i < PDetails.length; i++) {
            patient memory P = PDetails[i];
            if (
                keccak256(abi.encodePacked((P.PID))) ==
                keccak256(abi.encodePacked(pid))
            ) {
                return P.privkey;
            }
        }
        return "Not Found";
    }

    function SetDataShare(

        string memory SenderPid,
        string memory ReceiverPid,
        bytes memory encdata
        
    ) public {
        uint256 i;
        uint256 flag=0;
        for (i = 0; i < SharedData.length; i++) {				//iterate through hashtable
            if(

             (
                keccak256(abi.encodePacked((SharedData[i].SenderPID))) ==
                keccak256(abi.encodePacked(SenderPid))  
            ) &&
            (
                keccak256(abi.encodePacked((SharedData[i].ReceiverPID))) ==
                keccak256(abi.encodePacked(ReceiverPid))  
            )
            ) {								//if present
                SharedData[i].data=encdata;			//add index to pid in hashtable
                flag = 1;							//set the flag
                break;
            }    

        }
        if (flag != 1) {							//if flag not set(not present)            
            SharedData.push(datasharing(SenderPid,ReceiverPid,1,encdata));				//create new entry in hashtable
        }

    }
    function UnSetFlagDataShare(

        string memory SenderPid,
        string memory ReceiverPid
        
    ) public returns (string memory) {
        uint256 i;
        for (i = 0; i < SharedData.length; i++) {				//iterate through hashtable
            if(

             (
                keccak256(abi.encodePacked((SharedData[i].SenderPID))) ==
                keccak256(abi.encodePacked(SenderPid))  
            ) &&
            (
                keccak256(abi.encodePacked((SharedData[i].ReceiverPID))) ==
                keccak256(abi.encodePacked(ReceiverPid))  
            )
            ) {								//if present
                SharedData[i].flag=0;			//add index to pid in hashtable
                return("Success");
            }    

        }
        return("Not Present");

    }
    function GetDataShare(

        string memory SenderPid,
        string memory ReceiverPid
        
    ) public returns(bytes memory){
        uint256 i;
        uint256 flag=0;
        for (i = 0; i < SharedData.length; i++) {				//iterate through hashtable
            if(

             (
                keccak256(abi.encodePacked((SharedData[i].SenderPID))) ==
                keccak256(abi.encodePacked(SenderPid))  
            ) &&
            (
                keccak256(abi.encodePacked((SharedData[i].ReceiverPID))) ==
                keccak256(abi.encodePacked(ReceiverPid))  
            )
            && SharedData[i].flag==1
            ) {								//if present
                return SharedData[i].data;
            }    

        }
        if (flag != 1) {							//if flag not set(not present)            
            return "";				//create new entry in hashtable
        }

    }

}
