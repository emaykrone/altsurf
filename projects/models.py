# projects/models.py

from django.db import models
import uuid

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название проекта")
    domain = models.CharField(max_length=255, unique=True, verbose_name="Домен сайта")
    pixel_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Уникальный ID пикселя")
    yandex_metrica_counter_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID счетчика Яндекс.Метрики")
    yandex_metrica_access_token = models.TextField(blank=True, null=True, verbose_name="Токен Яндекс.Метрики")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name