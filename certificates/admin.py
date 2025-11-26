# certificates/admin.py

from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = [
        'certificate_id', 
        'user', 
        'course', 
        'score', 
        'blockchain_minted',
        'issued_at'
    ]
    list_filter = ['blockchain_minted', 'issued_at', 'course']
    search_fields = [
        'user__username', 
        'course__title', 
        'certificate_id',
        'transaction_hash'
    ]
    readonly_fields = ['certificate_id', 'issued_at']