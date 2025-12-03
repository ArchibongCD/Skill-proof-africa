
# SkillProof Africa

A blockchain-powered certificate verification platform built on Camp Network, enabling African learners to earn tamper-proof, globally recognized credentials.

## The Problem

African professionals face significant challenges in having their skills recognized globally. Traditional paper certificates can be easily forged, lost, or difficult to verify. This creates barriers for:

- **Job seekers** who struggle to prove their qualifications to international employers
- **Employers** who need reliable ways to verify candidate credentials
- **Educational institutions** that lack resources for secure certificate issuance
- **Remote workers** competing in the global marketplace without verified credentials

The credibility gap costs African talent opportunities in the growing remote work economy, where skill verification is critical but difficult across borders.

## The Solution

SkillProof Africa provides blockchain-verified certificates that are:

- **Tamper-proof**: Stored permanently on Camp Network blockchain
- **Instantly verifiable**: Anyone can verify authenticity in seconds
- **Portable**: Certificates belong to learners, not institutions
- **Globally recognized**: Blockchain verification accepted worldwide
- **Cost-effective**: Lower issuance costs than traditional systems

## Features

### Current Implementation

- User registration and authentication
- Course enrollment and learning management
- Quiz-based skill assessment
- Certificate generation with unique IDs
- Wallet connection via MetaMask
- Camp Network blockchain integration
- Certificate display dashboard
- Public certificate verification
- Responsive design for mobile devices

### Technical Stack

**Backend**
- Django 4.2
- Python 3.12
- PostgreSQL/SQLite
- Django REST Framework

**Frontend**
- HTML5, CSS3, JavaScript
- Web3.js for blockchain interaction
- Camp Network Origin SDK
- Responsive design

**Blockchain**
- Camp Network Testnet
- Smart Contract: Solidity 0.8.20
- ERC-721 NFT standard

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- pip package manager
- MetaMask browser extension
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/ArchibongCD/Skill-proof-africa.git
cd Skill-proof-africa
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Camp Network Credentials
CAMP_CLIENT_ID=your-client-id
CAMP_API_KEY=your-api-key
```

Get your Camp Network credentials from [https://origin.campnetwork.xyz/](https://origin.campnetwork.xyz/)

### Step 5: Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### Step 7: Load Sample Data (Optional)

```bash
python manage.py loaddata courses
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

### Step 9: Access Admin Panel

Navigate to `http://localhost:8000/admin` and log in with your superuser credentials to manage courses, users, and certificates.

## User Guide

### For Learners

**1. Register an Account**
- Visit the homepage
- Click "Register" and complete the form
- Verify your email if required

**2. Browse and Enroll in Courses**
- Navigate to "Courses" page
- Select a course matching your interests
- Click "Start Learning"

**3. Complete Course Content**
- Read through course materials
- Take notes as needed
- Prepare for the assessment

**4. Take the Quiz**
- Pass with minimum 70% score
- Results displayed immediately
- Certificate generated automatically

**5. Connect Your Wallet**
- Install MetaMask extension
- Click "Connect Wallet" on dashboard
- Approve the connection request
- Switch to Camp Network when prompted

**6. Mint Your Certificate NFT**
- View certificates on your dashboard
- Click "Mint NFT" on any certificate
- Approve the transaction in MetaMask
- Wait for blockchain confirmation

**7. Share Your Achievement**
- View certificate details
- Click "Share" to post on Twitter
- Add certificate link to your resume/LinkedIn

### For Employers

**1. Verify a Certificate**
- Navigate to verification page
- Enter certificate ID provided by candidate
- View complete certificate details
- Check blockchain transaction hash
- Confirm on Camp Network block explorer


**2. Validate Authenticity**
- Certificate ID format: SP-XXXXXXXX
- Check issuing date and score
- Verify on blockchain using transaction hash
- Contact issuer if additional verification needed
- Direct http://127.0.0.1:8000/verify/?id=SP-42C3E1F4

## Smart Contract Details

**Contract Address:** `0x5cA16DD43883423E8ACEF5d2C38b2B7fbcEEAfF1`

**Network:** Camp Network Testnet (Chain ID: 123420001114)

**Contract Functions:**
- `mintCertificate`: Create new certificate NFT
- `getCertificate`: Retrieve certificate details
- `verifyCertificate`: Validate certificate authenticity
- `tokensOfOwner`: Get all certificates for a user

**Block Explorer:** [https://basecamp.cloud.blockscout.com/](https://basecamp.cloud.blockscout.com/)

## Current Limitations

### Technical

1. **NFT Minting Requires Contract Owner**: Current smart contract uses `onlyOwner` modifier, preventing users from minting directly
2. **Origin SDK Integration**: Camp Network Origin SDK requires additional configuration for full functionality
3. **Limited Payment Options**: No payment gateway for premium courses
4. **Single Chain Support**: Currently only supports Camp Network Testnet

### Platform Features

1. **Course Content**: Limited course library, no video content yet
2. **Assessment Types**: Only multiple-choice quizzes available
3. **User Profiles**: Basic profiles without social integration
4. **Mobile App**: No native mobile application
5. **Offline Access**: Requires internet connection

### Scalability

1. **Performance**: Not optimized for thousands of concurrent users
2. **Storage**: Media files stored locally, not on distributed storage
3. **Caching**: No Redis or caching layer implemented

## Future Improvements

**more courses will be added**

**Enhanced Learning Experience**
- Video course content with progress tracking
- Interactive coding exercises
- Peer-to-peer learning forums
- Live webinar integration
- Multiple assessment formats (projects, essays)

**Blockchain Features**
- Remove `onlyOwner` restriction for direct user minting
- Support Camp network mainet
- NFT marketplace for certificates
- Credential stacking and skill trees
- On-chain reputation system

**Platform Optimization**
- Redis caching for faster load times
- CDN integration for static assets
- Database query optimization
- API rate limiting and security

**Institutional Integration**
- University partnership program
- Employer verification portal
- API access for third-party integrations
- Bulk certificate issuance tools
- White-label solutions for institutions

**Advanced Features**
- AI-powered course recommendations
- Adaptive learning paths
- Skill gap analysis
- Career counseling integration
- Job board for verified candidates

**Mobile Experience**
- Native iOS and Android apps
- Progressive Web App (PWA)
- Offline course access
- Push notifications


**Ecosystem Growth**
- Decentralized governance (DAO)
- Token economics for platform rewards
- Content creator marketplace
- Global certification standards body
- Cross-platform credential portability

**Social Impact**
- Scholarship fund for underserved communities
- Partnerships with African tech hubs
- Free basic courses in local languages
- Rural internet cafe partnerships
- Employment outcome tracking

## Contributing

We welcome contributions from developers, designers, educators, and blockchain enthusiasts.

**How to Contribute:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

**Contribution Areas:**
- Course content development
- Smart contract improvements
- UI/UX enhancements
- Documentation
- Bug fixes
- Translation to local languages

## Testing

Run the test suite:

```bash
python manage.py test
```

Run specific tests:

```bash
python manage.py test certificates.tests
```

## Security

**Security Measures:**
- Django security middleware enabled
- CSRF protection on all forms
- SQL injection prevention via ORM
- XSS protection headers
- Regular dependency updates


## Acknowledgments

- Camp Network team for blockchain infrastructure
- Open-source community for tools and libraries
- Beta testers and early adopters
- African tech community for inspiration

## Project Status

**Current Version:** 1.0.0 (Beta)

**Last Updated:** December 2025

**Development Status:** Active development for Camp Network Africa Buildathon

Built with passion for African talent by the SkillProof Africa team.
