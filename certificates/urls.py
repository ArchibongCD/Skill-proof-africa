# certificates/urls.py

from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.user_certificates, name='list'),
    path('<str:certificate_id>/', views.certificate_detail, name='detail'),
    path('verify/<str:certificate_id>/', views.verify_certificate, name='verify'),
    path('mint/<int:certificate_pk>/', views.mint_nft, name='mint'),
    path('update-blockchain/', views.update_blockchain, name='update_blockchain'),
]