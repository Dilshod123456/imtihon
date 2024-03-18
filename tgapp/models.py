from django.db import models

class BotData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    country_info = models.TextField()
    recipient_email = models.EmailField()

    def __str__(self):
        return self.recipient_email