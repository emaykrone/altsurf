from django.contrib import admin
from .models import PixelEvent # Импортируем модель PixelEvent

@admin.register(PixelEvent)
class PixelEventAdmin(admin.ModelAdmin):
    # Теперь используем 'event_timestamp' вместо 'created_at'
    list_display = ('event_name', 'project', 'client_id', 'client_timestamp', 'event_timestamp', 'url')
    list_filter = ('event_name', 'project', 'event_timestamp') # Фильтруем по event_timestamp
    search_fields = ('client_id', 'event_name', 'url', 'em', 'ph', 'lid', 'uid', 'data') # Добавил больше полей для поиска, включая поля из payload
    readonly_fields = ('event_timestamp',) # event_timestamp должен быть только для чтения, так как он auto_now_add=True