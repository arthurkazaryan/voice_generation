from django.db import models
from django.contrib.auth.models import User
import uuid


class AudioSamples(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Пользовательское название'
    )
    name = models.CharField(
        max_length=128,
        verbose_name='API название'
    )
    audio = models.FileField(
        upload_to='generation/audio_samples',
        blank=False,
        editable=True,
    )
    visible = models.BooleanField(
        verbose_name='Показать',
        default=True,
        editable=True,
    )

    def __str__(self):
        return f"Audiosample {self.name}"

    class Meta:
        verbose_name = 'Audiosample'
        verbose_name_plural = 'Audiosamples'


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
