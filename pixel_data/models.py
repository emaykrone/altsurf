# pixel_data/models.py

from django.db import models
from projects.models import Project # Импортируем нашу новую модель Project

class PixelEvent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")

    event_name = models.CharField(max_length=255, db_index=True)
    event_timestamp = models.DateTimeField(auto_now_add=True)
    client_timestamp = models.BigIntegerField(null=True, blank=True)

    session_id = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name="Tomi.ai Client ID") # Переименовал, чтобы было ясно, что это наш ID
    
    # Новые поля для GA и Yandex
    google_analytics_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Google Analytics Client ID")
    yandex_client_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Yandex Metrica Client ID")

    user_agent = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)

    em = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    ph = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    lid = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    uid = models.CharField(max_length=255, null=True, blank=True, db_index=True)

    data = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Пиксельное событие"
        verbose_name_plural = "Пиксельные события"
        indexes = [
            models.Index(fields=['event_name', 'project']),
            models.Index(fields=['event_timestamp']),
            models.Index(fields=['client_id']),
            models.Index(fields=['yandex_client_id']), # Добавляем индекс для нового поля
            models.Index(fields=['google_analytics_id']), # Добавляем индекс
        ]

    def __str__(self):
        return f"{self.event_name} from Project {self.project.name} ({self.client_id or 'N/A'})"