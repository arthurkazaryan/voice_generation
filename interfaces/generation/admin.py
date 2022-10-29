from django.contrib import admin
from generation.models import AudioSamples, AudioFile


@admin.register(AudioSamples)
class AudioSamplesAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'audio', 'visible')
    search_fields = ('title',)


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio', 'date', 'status', 'text')
    # readonly_fields = ('user', 'audiofile_uuid', 'api_task_id', 'audio', 'date', 'status', 'text')
    search_fields = ('user__username',)
