# certificates/views.py - FIXED VERSION

from django.shortcuts import get_object_or_404, render
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
            'category': cert.course.category if hasattr(cert.course, 'category') else 'general',
            'difficulty': cert.course.difficulty if hasattr(cert.course, 'difficulty') else 'intermediate',
        },
        'score': cert.score,
        'issued_at': cert.issued_at.isoformat(),
        'blockchain_minted': cert.blockchain_minted,
        'transaction_hash': cert.transaction_hash,
        'nft_token_id': cert.nft_token_id,
    } for cert in certificates]
    
    return JsonResponse({'certificates': certs_data})

def certificate_detail(request, certificate_id):
    """Get certificate details - Returns HTML page OR JSON based on request"""
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)
    
    # Check if request wants JSON (API call)
    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        cert_data = {
            'certificate_id': certificate.certificate_id,
            'user': {
                'username': certificate.user.username,
                'wallet_address': getattr(certificate.user, 'wallet_address', None),
            },
            'course': {
                'title': certificate.course.title,
                'category': getattr(certificate.course, 'category', 'general'),
                'difficulty': getattr(certificate.course, 'difficulty', 'intermediate'),
            },
            'score': certificate.score,
            'issued_at': certificate.issued_at.isoformat(),
            'blockchain_minted': certificate.blockchain_minted,
            'transaction_hash': certificate.transaction_hash,
            'nft_token_id': certificate.nft_token_id,
        }
        return JsonResponse({'certificate': cert_data})
    
    # Otherwise return HTML page
    context = {
        'certificate': certificate,
    }
    return render(request, 'certificates/certificate_detail.html', context)

def verify_certificate(request, certificate_id):
    """Verify if a certificate is valid"""
    try:
        certificate = Certificate.objects.get(certificate_id=certificate_id)
        return JsonResponse({
            'valid': True,
            'certificate_id': certificate.certificate_id,
            'user': certificate.user.username,
            'course': certificate.course.title,
            'issued_at': certificate.issued_at.isoformat(),
            'blockchain_minted': certificate.blockchain_minted,
            'nft_token_id': certificate.nft_token_id,
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
    This endpoint is called after blockchain minting to update the database
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    certificate = get_object_or_404(Certificate, pk=certificate_pk, user=request.user)
    
    try:
        data = json.loads(request.body)
        tx_hash = data.get('transaction_hash')
        token_id = data.get('nft_token_id')
        
        if tx_hash and token_id:
            certificate.transaction_hash = tx_hash
            certificate.nft_token_id = token_id
            certificate.blockchain_minted = True
            certificate.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Certificate successfully minted as NFT',
                'certificate_id': certificate.certificate_id,
                'nft_token_id': token_id,
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Missing transaction hash or token ID'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)