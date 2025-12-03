# certificates/urls.py - FIXED VERSION

from django.urls import path
from . import views

urlpatterns = [
    # Remove 'api/certificates/' prefix - it's already in main urls.py!
    path('', views.user_certificates, name='user_certificates'),
    path('<str:certificate_id>/', views.certificate_detail, name='certificate_detail'),
    path('verify/<str:certificate_id>/', views.verify_certificate, name='verify_certificate'),
    path('update-blockchain/', views.update_blockchain, name='update_blockchain'),
    path('mint/<int:certificate_pk>/', views.mint_nft, name='mint_nft'),
]