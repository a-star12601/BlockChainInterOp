// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;
pragma experimental ABIEncoderV2;


contract Intermediate {

    struct hospitals {
        string name;
        string network;
        string link;
    }
    hospitals[] public HospitalList;

    function RetHosp(string memory name) public view returns (string memory network,string memory link) {
         uint256 i;
        for (i = 0; i < HospitalList.length; i++) {
            hospitals memory H = HospitalList[i];
            if (
                (keccak256(abi.encodePacked(H.name)) ==
                    keccak256(abi.encodePacked(name)))
            ) {
                return (H.network,H.link);
            }
        }
    }

    function RegHosp(
        string memory name,
        string memory network,
        string memory link
    ) public {
        HospitalList.push(hospitals(name,network,link));
    }

    function GetH() public view returns (hospitals[] memory) {
        return HospitalList;
    }
}