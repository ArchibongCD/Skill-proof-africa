// static/js/web3.js
// Web3 Integration for SkillProof Africa with Camp Network Origin SDK

// Contract Configuration
const CONTRACT_ADDRESS = '0x5cA16DD43883423E8ACEF5d2C38b2B7fbcEEAfF1';
const CAMP_CHAIN_ID = '123420001114';
const CAMP_RPC_URL = 'https://rpc.basecamp.t.raas.gelato.cloud';

// Camp Network Origin SDK Configuration
const CAMP_CONFIG = {
    clientId: "fce77d7a-8085-47ca-adff-306a933e76aa",
    apiKey: '4f1a2c9c-008e-47ca-adff-306a933e76aa', 
    environment: 'DEVELOPMENT',
    redirectUri: window.location.origin,
};

// Contract ABI
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
let campAuth = null;

// Initialize Camp Origin SDK
function initializeOriginSDK() {
    return new Promise((resolve, reject) => {
        if (typeof window.CampNetwork === 'undefined') {
            reject(new Error('CampNetwork SDK not loaded'));
            return;
        }
        
        try {
            campAuth = new window.CampNetwork.Auth({
                clientId: CAMP_CONFIG.clientId,
                redirectUri: CAMP_CONFIG.redirectUri,
                environment: CAMP_CONFIG.environment,
                allowAnalytics: true,
            });
            resolve(true);
        } catch (error) {
            reject(error);
        }
    });
}

// Check if MetaMask is installed
function isMetaMaskInstalled() {
    return typeof window.ethereum !== 'undefined';
}

// Connect wallet
async function connectWallet() {
    if (userAccount) {
        disconnectWallet();
        return;
    }

    const connectWalletBtn = document.getElementById('connectWallet');
    if (connectWalletBtn) {
        connectWalletBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Connecting...`;
    }

    if (!isMetaMaskInstalled()) {
        showNotification('Please install MetaMask to use blockchain features!', 'error');
        window.open('https://metamask.io/download/', '_blank');
        if (connectWalletBtn) {
            connectWalletBtn.innerHTML = `<i class="fas fa-wallet"></i> <span>Connect</span>`;
        }
        return;
    }

    try {
        showLoading(true);
        
        // Initialize Origin SDK if not already done
        if (!campAuth) {
            try {
                await initializeOriginSDK();
            } catch (error) {
                // Continue without Origin SDK
            }
        }
        
        // Request account access
        const accounts = await window.ethereum.request({ 
            method: 'eth_requestAccounts' 
        });
        
        userAccount = accounts[0];
        window.userAccount = userAccount;
        
        // Initialize Web3
        web3 = new Web3(window.ethereum);
        contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);
        
        // Check network
        const chainId = await web3.eth.getChainId();
        if (chainId.toString() !== CAMP_CHAIN_ID) {
            await switchToCAMPNetwork();
        }
        
        // Update UI
        updateWalletUI(userAccount);
        
        // Save to backend
        await saveWalletAddress(userAccount);
        
        // Connect with Origin SDK if available
        if (campAuth) {
            try {
                campAuth.setProvider({
                    provider: window.ethereum,
                    info: { name: 'MetaMask', icon: 'https://metamask.io/images/favicon.ico' }
                });
                await campAuth.connect();
            } catch (originError) {
                // Continue with basic connection
            }
        }
        
        showNotification('Wallet connected successfully!', 'success');
        showLoading(false);
        
        return userAccount;
    } catch (error) {
        showNotification('Failed to connect wallet: ' + error.message, 'error');
        showLoading(false);
        if (connectWalletBtn) {
            connectWalletBtn.innerHTML = `<i class="fas fa-wallet"></i> <span>Connect</span>`;
        }
        return null;
    }
}

// Disconnect wallet
function disconnectWallet() {
    userAccount = null;
    window.userAccount = null;
    
    const walletBtn = document.getElementById('connectWallet');
    if (walletBtn) {
        walletBtn.innerHTML = '<i class="fas fa-wallet"></i> <span>Connect</span>';
        walletBtn.classList.remove('connected');
    }
    
    const walletStatus = document.getElementById('walletStatus');
    if (walletStatus) {
        walletStatus.innerHTML = `
            <i class="fas fa-wallet"></i>
            <div style="margin-top: 0.5rem; font-weight: 600;">
                <div id="walletText">Wallet Not Connected</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">Connect to mint NFTs</div>
            </div>
        `;
        walletStatus.classList.remove('connected');
    }
    
    showNotification('Wallet disconnected', 'info');
}

// Switch to Camp Network
async function switchToCAMPNetwork() {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: '0x' + parseInt(CAMP_CHAIN_ID).toString(16) }],
        });
    } catch (switchError) {
        if (switchError.code === 4902) {
            try {
                await window.ethereum.request({
                    method: 'wallet_addEthereumChain',
                    params: [{
                        chainId: '0x' + parseInt(CAMP_CHAIN_ID).toString(16),
                        chainName: 'Camp Network Testnet',
                        rpcUrls: [CAMP_RPC_URL],
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
    const walletStatus = document.getElementById('walletStatus');
    const shortAddress = `${address.slice(0, 6)}...${address.slice(-4)}`;
    
    if (walletBtn) {
        walletBtn.innerHTML = `<i class="fas fa-check-circle"></i> <span>${shortAddress}</span>`;
        walletBtn.classList.add('connected');
    }
    
    if (walletStatus) {
        walletStatus.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <div style="margin-top: 0.5rem; font-weight: 600;">Wallet Connected</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">${address}</div>
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
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ wallet_address: address })
        });
        
        const data = await response.json();
        if (!data.success) {
            console.error('Failed to save wallet address');
        }
    } catch (error) {
        console.error('Error saving wallet:', error);
    }
}

// Mint certificate NFT using Camp Origin SDK
async function mintCertificateNFT(certificateData) {
    if (!campAuth || !userAccount) {
        showNotification('Please connect your wallet first', 'error');
        return { success: false, error: 'Wallet not connected' };
    }

    try {
        showLoading(true);
        
        const license = {
            price: BigInt("1000000000000000"),
            duration: 86400,
            royaltyBps: 500,
            paymentToken: "0x0000000000000000000000000000000000000000"
        };

        const metadata = {
            name: `Skill Proof: ${certificateData.courseName}`,
            description: `Certificate for ${certificateData.studentName} - Score: ${certificateData.score}%`,
            attributes: [
                { trait_type: "Course", value: certificateData.courseName },
                { trait_type: "Score", value: certificateData.score.toString() },
                { trait_type: "Certificate ID", value: certificateData.certificateId }
            ]
        };

        const tokenId = await campAuth.origin.mintSocial("twitter", metadata, license);
        
        showLoading(false);
        showNotification('Certificate minted successfully!', 'success');
        
        return {
            success: true,
            transactionHash: tokenId,
            tokenId: tokenId
        };
        
    } catch (error) {
        showLoading(false);
        showNotification('Failed to mint certificate: ' + error.message, 'error');
        return { success: false, error: error.message };
    }
}

// Update certificate with blockchain data
async function updateCertificateBlockchain(certificateId, txHash, tokenId) {
    try {
        const response = await fetch('/api/certificates/update-blockchain/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                certificate_id: certificateId,
                transaction_hash: txHash,
                nft_token_id: tokenId
            })
        });
        
        return await response.json();
    } catch (error) {
        console.error('Error updating certificate:', error);
    }
}

// Helper: Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show loading indicator
function showLoading(show) {
    const loadingEl = document.getElementById('loadingOverlay');
    if (loadingEl) {
        loadingEl.style.display = show ? 'flex' : 'none';
    }
}

// Show notification
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Listen for account changes
if (typeof window.ethereum !== 'undefined') {
    window.ethereum.on('accountsChanged', function (accounts) {
        if (accounts.length === 0) {
            disconnectWallet();
        } else {
            userAccount = accounts[0];
            window.userAccount = userAccount;
            updateWalletUI(userAccount);
            saveWalletAddress(userAccount);
        }
    });

    window.ethereum.on('chainChanged', function () {
        window.location.reload();
    });
}
