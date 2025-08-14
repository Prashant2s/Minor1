// SPDX-License-Identifier: MIT

pragma solidity >=0.8.2 <0.9.0;

/*
Example C: 
    Public schools and universities issues graduation certificates or 
degrees to students.  Students rely on these certificates or degrees 
to seek employment.  Potential employers check the certificates/degrees 
to decide whether to give jobs to the students.   This scenario involves 
a few smart contracts.  One smart contract is from the schools or 
universities.   One smart contract represents the students. The third 
smart contract represents companies and organizations.
*/

// ===========================================================
//           Contract for Educational Institutions
// ===========================================================

contract EducationalInstitutionsSmartContract {

    // For keepping the records of certificate / degree of the student graduated from this institution
    struct Certificate {
        uint256 cid;
        string studentName;
        string degreeName;
        string issueDate;
        string hash; // Hash of the certificate for verification
        bool isValid;
    }

    // Store all the records in a mapping: id(key) - certficate(value)
    mapping(uint => Certificate) private certificates;
    // The owner of the contract, i.e., NTU
    address private owner; 
    // Automatically assign an id for a certificate, initialized to 1 at the beginning
    uint256 private currentCertificateId = 1;

    constructor() {
        // Set the owner of the contract to the account that deploys it
        owner = msg.sender; 
    }

    // Events
    event CertificateIssued(uint256 indexed id, string studentName, string degreeName);
    event CertificateRevoked(uint256 indexed id);
    event CertificateUpdated(uint256 indexed id, string newHash);

    /*
    This contract will allow the institution to:
        - Issue a certificate (for owner use)
        - Revoke a certificate (for owner use)
        - Update a certificate (for owner use)
        - Verify a certificate (for external personnel use)
        - transfer tokens from this SC to the address of this institution
    */