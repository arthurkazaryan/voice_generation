from django.db import models
from django.contrib.auth.models import User
import uuid


class AudioFile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    audiofile_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='Audiofile UUID',
        unique=True,
    )
    api_task_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name='API task UUID'
    )
    voice = models.CharField(
        max_length=32,
        verbose_name='Voice'
    )
    audio = models.FileField(
        default='',
        upload_to='generation/audio_created',
        null=True,
        blank=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Time added'
    )
    status = models.CharField(
        max_length=10,
        verbose_name='Status',
    )
    text = models.TextField(
        verbose_name='Text'
    )

    def __str__(self):
        return f"{self.user.username}'s audiofile"

    class Meta:
        verbose_name = 'Audiofile'
        verbose_name_plural = 'Audiofiles'
