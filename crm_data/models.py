# tomi_ai_service/crm_data/models.py

from django.db import models
from projects.models import Project # Импортируем модель Project из приложения projects

class CRMQuotes(models.Model):
    """
    Модель для хранения данных о заявках (Quotes) из CRM.
    Соответствует разделу "Quotes" в документе Tomi.ai_Borzo_Integrations and access.docx.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")

    datetime = models.DateTimeField(verbose_name="Дата и время заявки") # Соответствует 'datetime'
    google_analytics_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Google Analytics ID") # Соответствует 'google_analytics_id'
    lead_id = models.CharField(max_length=255, db_index=True, verbose_name="CRM Lead ID") # Соответствует 'lead_id'
    user_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name="CRM User ID") # Соответствует 'user_id'
    email = models.EmailField(max_length=255, null=True, blank=True, db_index=True, verbose_name="Email") # Соответствует 'email'
    phone = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name="Телефон") # Соответствует 'phone'
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя") # Соответствует 'first_name'
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия") # Соответствует 'last_name'
    event_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="Тип события (источник)") # Соответствует 'event_type'
    soft_pull_result = models.TextField(null=True, blank=True, verbose_name="Результат Soft Pull") # Соответствует 'soft_pull_result'
    address = models.TextField(null=True, blank=True, verbose_name="Адрес") # Соответствует 'address'

    # 'any_value1', 'any_value2' и другие дополнительные произвольные поля
    # будут храниться в JSONField 'data'
    data = models.JSONField(default=dict, blank=True, verbose_name="Дополнительные данные")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления записи")

    class Meta:
        verbose_name = "Заявка из CRM"
        verbose_name_plural = "Заявки из CRM"
        indexes = [
            models.Index(fields=['project', 'lead_id']),
            models.Index(fields=['project', 'user_id']),
            models.Index(fields=['datetime']),
        ]

    def __str__(self):
        return f"Заявка {self.lead_id or 'N/A'} для проекта {self.project.name}"

class RealConversions(models.Model):
    """
    Модель для хранения данных о закрытых сделках (Closed Deals) из CRM.
    Соответствует разделу "Closed deals" в документе Tomi.ai_Borzo_Integrations and access.docx.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")

    datetime = models.DateTimeField(verbose_name="Дата и время закрытия сделки") # Соответствует 'datetime'
    order_id = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="ID заказа") # Соответствует 'order_id'
    user_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name="CRM User ID") # Соответствует 'user_id'
    lead_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name="CRM Lead ID") # Соответствует 'lead_id'
    google_analytics_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Google Analytics ID") # Соответствует 'google_analytics_id'
    email = models.EmailField(max_length=255, null=True, blank=True, db_index=True, verbose_name="Email") # Соответствует 'email'
    phone = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name="Телефон") # Соответствует 'phone'
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Ценность сделки") # Соответствует 'value'

    # utm_source, utm_medium, utm_campaign, utm_content, utm_term
    # будут храниться в JSONField 'data'
    data = models.JSONField(default=dict, blank=True, verbose_name="UTM и другие данные")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления записи")

    class Meta:
        verbose_name = "Закрытая сделка"
        verbose_name_plural = "Закрытые сделки"
        indexes = [
            models.Index(fields=['project', 'order_id']),
            models.Index(fields=['project', 'user_id']),
            models.Index(fields=['datetime']),
        ]

    def __str__(self):
        return f"Сделка {self.order_id} для проекта {self.project.name}"