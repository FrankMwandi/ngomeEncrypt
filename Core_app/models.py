from django.db import models

class EncryptionLog(models.Model):
    ip_address = models.CharField(max_length=45)
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} from {self.ip_address} at {self.timestamp}"
