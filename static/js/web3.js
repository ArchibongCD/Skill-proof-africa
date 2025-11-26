// static/js/web3.js
// Web3 Integration for SkillProof Africa

// Contract Configuration
const CONTRACT_ADDRESS = '0x5cA16DD43883423E8ACEF5d2C38b2B7fbcEEAfF1';
const CAMP_CHAIN_ID = '123420001114'; // Replace with Camp Network Chain ID (get from their docs)
const CAMP_RPC_URL = 'https://origin.campnetwork.xyz/';

// Contract ABI (Application Binary Interface)
// This is how JavaScript talks to the smart contract
const CONTRACT_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"indexed": false, "internalType": "string", "name": "certificateId", "type": "string"},
            {"indexed": true, "internalType": "address", "name": "student", "type": "address"},
            {"indexed": false, "internalType": "string", "name": "courseName", "type": "string"},
            {"indexed": false, "internalType": "uint256", "name": "score", "type": "uint256"},
            {"indexed": false, "internalType": "uint256", "name": "issueDate", "type": "uint256"}
        ],
        "name": "CertificateMinted",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_certificateId", "type": "string"},
            {"internalType": "string", "name": "_courseName", "type": "string"},
            {"internalType": "string", "name": "_studentName", "type": "string"},
            {"internalType": "address", "name": "_studentWallet", "type": "address"},
            {"internalType": "uint256", "name": "_score", "type": "uint256"},
            {"internalType": "string", "name": "_tokenURI", "type": "string"}
        ],
        "name": "mintCertificate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_tokenId", "type": "uint256"}],
        "name": "getCertificate",
        "outputs": [
            {"internalType": "string", "name": "certificateId", "type": "string"},
            {"internalType": "string", "name": "courseName", "type": "string"},
            {"internalType": "string", "name": "studentName", "type": "string"},
            {"internalType": "address", "name": "studentWallet", "type": "address"},
            {"internalType": "uint256", "name": "score", "type": "uint256"},
            {"internalType": "uint256", "name": "issueDate", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "_certificateId", "type": "string"}],
        "name": "verifyCertificate",
        "outputs": [
            {"internalType": "bool", "name": "isValid", "type": "bool"},
            {"internalType": "string", "name": "courseName", "type": "string"},
            {"internalType": "string", "name": "studentName", "type": "string"},
            {"internalType": "uint256", "name": "score", "type": "uint256"},
            {"internalType": "uint256", "name": "issueDate", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalCertificates",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_student", "type": "address"},
            {"internalType": "string", "name": "_courseName", "type": "string"}
        ],
        "name": "checkCertificate",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "_owner", "type": "address"}],
        "name": "tokensOfOwner",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    }
];

// Global variables
let web3;
let contract;
let userAccount;

// Check if MetaMask is installed
function isMetaMaskInstalled() {
    return typeof window.ethereum !== 'undefined';
}

// Connect wallet
async function connectWallet() {
    if (!isMetaMaskInstalled()) {
        alert('Please install MetaMask to use blockchain features!');
        window.open('https://metamask.io/download/', '_blank');
        return;
    }

    try {
        showLoading(true);
        
        // Request account access
        const accounts = await window.ethereum.request({ 
            method: 'eth_requestAccounts' 
        });
        
        userAccount = accounts[0];
        
        // Initialize Web3
        web3 = new Web3(window.ethereum);
        
        // Initialize contract
        contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);
        
        // Check if on correct network
        const chainId = await web3.eth.getChainId();
        if (chainId !== CAMP_CHAIN_ID) {
            await switchToCAMPNetwork();
        }
        
        // Update UI
        updateWalletUI(userAccount);
        
        // Save wallet to backend
        await saveWalletAddress(userAccount);
        
        showNotification('Wallet connected successfully!', 'success');
        showLoading(false);
        
        return userAccount;
    } catch (error) {
        console.error('Error connecting wallet:', error);
        showNotification('Failed to connect wallet: ' + error.message, 'error');
        showLoading(false);
        return null;
    }
}

// Switch to Camp Network
async function switchToCAMPNetwork() {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: CAMP_CHAIN_ID }],
        });
    } catch (switchError) {
        // Network not added, try to add it
        if (switchError.code === 4902) {
            try {
                await window.ethereum.request({
                    method: 'wallet_addEthereumChain',
                    params: [{
                        chainId: CAMP_CHAIN_ID,
                        chainName: 'Camp Network Basecamp',
                        rpcUrls: ['CAMP_RPC_URL'], // Replace with actual RPC
                        nativeCurrency: {
                            name: 'CAMP',
                            symbol: 'CAMP',
                            decimals: 18
                        },
                        blockExplorerUrls: ['https://basecamp.cloud.blockscout.com/']
                    }]
                });
            } catch (addError) {
                throw addError;
            }
        } else {
            throw switchError;
        }
    }
}

// Update UI after wallet connection
function updateWalletUI(address) {
    const walletBtn = document.getElementById('connectWallet');
    const walletText = document.getElementById('walletText');
    const walletStatus = document.getElementById('walletStatus');
    
    if (walletBtn) {
        const shortAddress = `${address.slice(0, 6)}...${address.slice(-4)}`;
        if (walletText) {
            walletText.textContent = shortAddress;
        } else {
            walletBtn.innerHTML = `<i class="fas fa-wallet"></i> ${shortAddress}`;
        }
        walletBtn.classList.add('connected');
    }
    
    if (walletStatus) {
        walletStatus.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <div style="margin-top: 0.5rem; font-weight: 600;">Wallet Connected</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">${address.slice(0, 10)}...${address.slice(-8)}</div>
        `;
        walletStatus.classList.add('connected');
    }
}

// Save wallet address to backend
async function saveWalletAddress(address) {
    try {
        const response = await fetch('/api/users/update-wallet/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                wallet_address: address
            })
        });
        
        const data = await response.json();
        if (data.success) {
            console.log('Wallet address saved to database');
        }
    } catch (error) {
        console.error('Error saving wallet address:', error);
    }
}

// Mint certificate NFT
async function mintCertificateNFT(certificateData) {
    if (!contract || !userAccount) {
        showNotification('Please connect your wallet first', 'error');
        return false;
    }

    try {
        showLoading(true);
        
        // Call smart contract mintCertificate function
        const tx = await contract.methods.mintCertificate(
            certificateData.certificateId,
            certificateData.courseName,
            certificateData.studentName,
            userAccount,
            certificateData.score,
            "" // tokenURI (optional)
        ).send({ 
            from: userAccount,
            gas: 500000 // Adjust if needed
        });
        
        console.log('Transaction successful:', tx);
        
        // Update backend with transaction hash
        await updateCertificateBlockchain(
            certificateData.certificateId,
            tx.transactionHash,
            tx.events.CertificateMinted.returnValues.tokenId
        );
        
        showNotification('Certificate minted on blockchain!', 'success');
        showLoading(false);
        
        return {
            success: true,
            transactionHash: tx.transactionHash,
            tokenId: tx.events.CertificateMinted.returnValues.tokenId
        };
        
    } catch (error) {
        console.error('Error minting certificate:', error);
        showNotification('Failed to mint certificate: ' + error.message, 'error');
        showLoading(false);
        return { success: false, error: error.message };
    }
}

// Update certificate with blockchain data
async function updateCertificateBlockchain(certificateId, txHash, tokenId) {
    try {
        const response = await fetch(`/api/certificates/update-blockchain/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                certificate_id: certificateId,
                transaction_hash: txHash,
                nft_token_id: tokenId
            })
        });
        
        return await response.json();
    } catch (error) {
        console.error('Error updating certificate blockchain data:', error);
    }
}

// Verify certificate on blockchain
async function verifyCertificateOnChain(certificateId) {
    if (!contract) {
        // Initialize contract in read-only mode
        web3 = new Web3('CAMP_RPC_URL'); // Replace with Camp Network RPC
        contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);
    }

    try {
        const result = await contract.methods.verifyCertificate(certificateId).call();
        
        return {
            isValid: result.isValid,
            courseName: result.courseName,
            studentName: result.studentName,
            score: result.score,
            issueDate: new Date(result.issueDate * 1000)
        };
    } catch (error) {
        console.error('Error verifying certificate:', error);
        return { isValid: false };
    }
}

// Get user's certificates from blockchain
async function getUserCertificates() {
    if (!contract || !userAccount) {
        return [];
    }

    try {
        const tokenIds = await contract.methods.tokensOfOwner(userAccount).call();
        const certificates = [];
        
        for (let tokenId of tokenIds) {
            const cert = await contract.methods.getCertificate(tokenId).call();
            certificates.push({
                tokenId: tokenId,
                certificateId: cert.certificateId,
                courseName: cert.courseName,
                studentName: cert.studentName,
                score: cert.score,
                issueDate: new Date(cert.issueDate * 1000)
            });
        }
        
        return certificates;
    } catch (error) {
        console.error('Error getting user certificates:', error);
        return [];
    }
}

// Listen for account changes
if (typeof window.ethereum !== 'undefined') {
    window.ethereum.on('accountsChanged', function (accounts) {
        if (accounts.length === 0) {
            // User disconnected wallet
            userAccount = null;
            showNotification('Wallet disconnected', 'info');
        } else {
            // User switched accounts
            userAccount = accounts[0];
            updateWalletUI(userAccount);
            saveWalletAddress(userAccount);
        }
    });

    window.ethereum.on('chainChanged', function (chainId) {
        // Reload page when network changes
        window.location.reload();
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if wallet was previously connected
    if (isMetaMaskInstalled() && window.ethereum.selectedAddress) {
        connectWallet();
    }
    
    // Connect wallet button
    const connectWalletBtn = document.getElementById('connectWallet');
    if (connectWalletBtn) {
        connectWalletBtn.addEventListener('click', connectWallet);
    }
});