# pixel_data/serializers.py

from rest_framework import serializers
from .models import PixelEvent # Убедись, что PixelEvent импортирован
from projects.models import Project
import uuid

class PixelEventSerializer(serializers.ModelSerializer):
    pixel_id = serializers.UUIDField(write_only=True) # Поле только для записи, не соответствует модели напрямую

    class Meta:
        model = PixelEvent
        # Добавляем новые поля в fields
        fields = (
            'event_name', 'client_timestamp', 'session_id', 'client_id',
            'google_analytics_id', 'yandex_client_id', # <-- Новые поля
            'user_agent', 'ip_address', 'url', 'referrer',
            'em', 'ph', 'lid', 'uid', 'data', 'pixel_id'
        )
        read_only_fields = ('event_timestamp',) # event_timestamp генерируется автоматически

    def create(self, validated_data):
        pixel_uuid = validated_data.pop('pixel_id')
        try:
            project = Project.objects.get(pixel_id=pixel_uuid)
        except Project.DoesNotExist:
            raise serializers.ValidationError({"pixel_id": "Project with this pixel_id does not exist."})

        # Добавляем IP-адрес из запроса
        # NOTE: request доступен в контексте сериализатора, если он передан из View
        request = self.context.get('request')
        if request:
            validated_data['ip_address'] = request.META.get('REMOTE_ADDR')

        return PixelEvent.objects.create(project=project, **validated_data)

    def to_representation(self, instance):
        # Если нужно отображать pixel_id при чтении (хотя он write_only)
        # instance.pixel_id = instance.project.pixel_id
        return super().to_representation(instance)