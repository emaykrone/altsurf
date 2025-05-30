# pixel_data/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import PixelEvent
from .serializers import PixelEventSerializer
from django.conf import settings
import logging
from projects.models import Project # Добавь этот импорт, если его еще нет

logger = logging.getLogger(__name__)

class PixelEventCreateAPIView(generics.CreateAPIView):
    queryset = PixelEvent.objects.all()
    serializer_class = PixelEventSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')

        mutable_data = request.data.copy()
        mutable_data['ip_address'] = ip_address
        mutable_data['user_agent'] = user_agent
        mutable_data['referrer'] = referrer
        
        if 'pixel_id' not in mutable_data:
            # Для отладки, если пиксель еще не обновлен и pixel_id не передан
            # В продакшене это должна быть ошибка, если pixel_id не передан
            if settings.DEBUG: # Добавил проверку на DEBUG
                try:
                    # Берем первый проект, если он есть, для временной заглушки
                    first_project = Project.objects.first()
                    if first_project:
                        mutable_data['pixel_id'] = str(first_project.pixel_id)
                    else:
                        logger.error("No projects found, and pixel_id not provided in event.")
                        return Response({"detail": "No project found for pixel_id and no default project available."}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error(f"Error getting default project: {e}")
                    return Response({"detail": "Server error getting default project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else: # В продакшене без pixel_id не пропускаем
                return Response({"pixel_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)


        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if settings.DEBUG:
            logger.info(f"Received pixel event for project {serializer.instance.project.name}: {serializer.data}")

        return Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip