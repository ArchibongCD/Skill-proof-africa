# certificates/models.py

from django.db import models
from django.conf import settings
from courses.models import Course

class Certificate(models.Model):
    """
    Represents a certificate issued to a user
    Will be linked to blockchain NFT
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField()
    issued_at = models.DateTimeField(auto_now_add=True)
    
    # Blockchain fields
    nft_token_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_hash = models.CharField(max_length=100, blank=True, null=True)
    blockchain_minted = models.BooleanField(default=False)
    
    # Certificate details
    certificate_id = models.CharField(max_length=50, unique=True)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-issued_at']
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_id:
            # Generate unique certificate ID
            import uuid
            self.certificate_id = f"SP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)