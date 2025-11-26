# certificates/views.py

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Certificate
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def update_blockchain(request):
    """Update certificate with blockchain transaction data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        certificate_id = data.get('certificate_id')
        tx_hash = data.get('transaction_hash')
        token_id = data.get('nft_token_id')
        
        certificate = Certificate.objects.get(certificate_id=certificate_id, user=request.user)
        certificate.transaction_hash = tx_hash
        certificate.nft_token_id = token_id
        certificate.blockchain_minted = True
        certificate.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Certificate updated with blockchain data'
        })
    except Certificate.DoesNotExist:
        return JsonResponse({'error': 'Certificate not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def user_certificates(request):
    """Get all certificates for logged-in user"""
    certificates = Certificate.objects.filter(user=request.user).select_related('course')
    
    certs_data = [{
        'certificate_id': cert.certificate_id,
        'course': {
            'title': cert.course.title,
            'slug': cert.course.slug,
        },
        'score': cert.score,
        'issued_at': cert.issued_at.isoformat(),
        'blockchain_minted': cert.blockchain_minted,
        'transaction_hash': cert.transaction_hash,
        'nft_token_id': cert.nft_token_id,
    } for cert in certificates]
    
    return JsonResponse({'certificates': certs_data})

def certificate_detail(request, certificate_id):
    """Get certificate details (public view for verification)"""
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)
    
    cert_data = {
        'certificate_id': certificate.certificate_id,
        'user': {
            'username': certificate.user.username,
            'wallet_address': certificate.user.wallet_address,
        },
        'course': {
            'title': certificate.course.title,
            'category': certificate.course.category,
            'difficulty': certificate.course.difficulty,
        },
        'score': certificate.score,
        'issued_at': certificate.issued_at.isoformat(),
        'blockchain_minted': certificate.blockchain_minted,
        'transaction_hash': certificate.transaction_hash,
        'nft_token_id': certificate.nft_token_id,
    }
    
    return JsonResponse({'certificate': cert_data})

def verify_certificate(request, certificate_id):
    """Verify if a certificate is valid"""
    try:
        certificate = Certificate.objects.get(certificate_id=certificate_id)
        return JsonResponse({
            'valid': True,
            'certificate_id': certificate.certificate_id,
            'user': certificate.user.username,
            'course': certificate.course.title,
            'issued_at': certificate.issued_at.isoformat()
        })
    except Certificate.DoesNotExist:
        return JsonResponse({
            'valid': False,
            'message': 'Certificate not found'
        }, status=404)

@login_required
def mint_nft(request, certificate_pk):
    """
    Mint NFT certificate on blockchain
    This will be implemented when we integrate Camp Network
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    certificate = get_object_or_404(Certificate, pk=certificate_pk, user=request.user)
    
    # TODO: Implement Camp Network blockchain minting
    # For now, just return a placeholder response
    
    return JsonResponse({
        'success': True,
        'message': 'NFT minting will be implemented with Camp Network integration',
        'certificate_id': certificate.certificate_id
    })