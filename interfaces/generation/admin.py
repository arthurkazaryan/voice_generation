from django.contrib import admin
from generation.models import AudioFile


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio', 'date', 'status', 'text')
    # readonly_fields = ('user', 'audiofile_uuid', 'api_task_id', 'audio', 'date', 'status', 'text')
    search_fields = ('user__username',)
